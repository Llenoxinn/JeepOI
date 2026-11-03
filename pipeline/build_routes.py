"""Merge the raw OSM and weebly downloads into the files the app reads.

Outputs, all regenerated from scratch:
  data/processed/routes.geojson   one feature per direction, map geometry
  data/processed/routes.json      one record per code, no coordinates
  data/processed/stops.geojson    named stops found on the OSM relations
  data/processed/ROUTES.md        human list, for review

Edit data/overrides.yaml and run this again. Do not hand-edit the outputs.
"""

from __future__ import annotations

import html
import io
import re
import zipfile
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

from common import (
    OSM_ATTRIBUTION,
    OVERRIDES,
    PRIORITY_CODES,
    PROCESSED,
    RAW_OSM,
    RAW_WEEBLY,
    STATUSES,
    WEEBLY_ATTRIBUTION,
    as_geometry,
    code_from_slug,
    coverage,
    family_of,
    flatten_geometry,
    haversine_m,
    line_length_m,
    load_overrides,
    norm_code,
    sample_line,
    write_json,
)

NEAR_M = 35


def latest_raw(kind: str) -> Path | None:
    files = sorted(RAW_OSM.glob(f"{kind}-*.json"))
    files = [p for p in files if not p.name.endswith(".meta.json")]
    return files[-1] if files else None


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_kml_coords(text: str) -> list[tuple[float, float]]:
    points = []
    for token in text.split():
        parts = token.split(",")
        if len(parts) < 2:
            continue
        try:
            lon, lat = float(parts[0]), float(parts[1])
        except ValueError:
            continue
        if not points or points[-1] != (lon, lat):
            points.append((lon, lat))
    return points


def read_kml_bytes(blob: bytes) -> str:
    if blob[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            name = "doc.kml" if "doc.kml" in archive.namelist() else archive.namelist()[0]
            return archive.read(name).decode("utf-8", "replace")
    return blob.decode("utf-8", "replace")


def kml_lines(blob: bytes) -> tuple[str, list[dict]]:
    text = read_kml_bytes(blob)
    root = ET.fromstring(text)
    title = ""
    for node in root.iter():
        if local(node.tag) == "name" and node.text:
            title = node.text.strip()
            break
    lines = []
    for placemark in root.iter():
        if local(placemark.tag) != "Placemark":
            continue
        name = ""
        for child in list(placemark):
            if local(child.tag) == "name" and child.text:
                name = " ".join(child.text.split())
                break
        for node in placemark.iter():
            if local(node.tag) not in {"LineString", "LinearRing"}:
                continue
            coords = []
            for child in node.iter():
                if local(child.tag) == "coordinates" and child.text:
                    coords = parse_kml_coords(child.text)
            if len(coords) >= 2:
                lines.append({"name": name or title, "coords": coords})
    return title, lines


def stitch(ways: list[list[tuple[float, float]]]) -> list[list[tuple[float, float]]]:
    parts: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] | None = None
    for line in ways:
        if len(line) < 2:
            continue
        if current is None:
            current = line[:]
            continue
        candidates = (
            (haversine_m(current[-1], line[0]), "append"),
            (haversine_m(current[-1], line[-1]), "append_rev"),
            (haversine_m(current[0], line[-1]), "prepend"),
            (haversine_m(current[0], line[0]), "prepend_rev"),
        )
        dist, how = min(candidates, key=lambda item: item[0])
        if dist > NEAR_M:
            parts.append(current)
            current = line[:]
            continue
        if how == "append":
            current.extend(line[1:])
        elif how == "append_rev":
            current.extend(reversed(line[:-1]))
        elif how == "prepend":
            current = line[:-1] + current
        else:
            current = list(reversed(line))[:-1] + current
    if current:
        parts.append(current)
    return parts


def osm_routes(path: Path) -> tuple[list[dict], list[dict]]:
    import json

    payload = json.loads(path.read_text(encoding="utf-8"))
    nodes = {el["id"]: el for el in payload.get("elements", []) if el.get("type") == "node"}
    routes = []
    stops = []
    for element in payload.get("elements", []):
        if element.get("type") != "relation":
            continue
        tags = element.get("tags") or {}
        code = norm_code(tags.get("ref")) or norm_code(tags.get("name"))
        ways = []
        for member in element.get("members") or []:
            if member.get("type") == "node":
                full = nodes.get(member.get("ref"), {})
                member_tags = full.get("tags") or member.get("tags") or {}
                role = member.get("role") or ""
                lat = member.get("lat", full.get("lat"))
                lon = member.get("lon", full.get("lon"))
                named = member_tags.get("name")
                if lat is not None and lon is not None and ("stop" in role or "platform" in role or named):
                    stops.append(
                        {
                            "name": named or "Unnamed stop",
                            "lon": lon,
                            "lat": lat,
                            "code": code,
                            "osm_id": member.get("ref"),
                            "role": role or "stop",
                        }
                    )
            geom = member.get("geometry") or []
            if member.get("type") != "way" or len(geom) < 2:
                continue
            coords = [(p["lon"], p["lat"]) for p in geom]
            role = (member.get("role") or "").lower()
            if "backward" in role or "reverse" in role:
                coords.reverse()
            ways.append(coords)
        parts = stitch(ways)
        routes.append(
            {
                "code": code,
                "osm_id": element.get("id"),
                "name": tags.get("name") or "",
                "from": tags.get("from") or "",
                "to": tags.get("to") or "",
                "ref": tags.get("ref") or "",
                "network": tags.get("network") or "",
                "route": tags.get("route") or "",
                "parts": parts,
            }
        )
    return routes, stops


def weebly_routes() -> list[dict]:
    manifest_path = RAW_WEEBLY / "manifest.json"
    if not manifest_path.exists():
        return []
    import json

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    found = []
    for page in manifest.get("pages", []):
        code = page.get("code") or code_from_slug(page.get("slug") or "")
        for item in page.get("maps") or []:
            if item.get("error") or not item.get("file"):
                continue
            blob_path = RAW_WEEBLY / item["file"]
            if not blob_path.exists():
                continue
            title, lines = kml_lines(blob_path.read_bytes())
            parsed = code or norm_code(title)
            if not parsed:
                continue
            for line in lines:
                found.append(
                    {
                        "code": parsed,
                        "page_code": parsed,
                        "name": line["name"] or title,
                        "title": title,
                        "page": page.get("page"),
                        "file": item["file"],
                        "parts": [line["coords"]],
                    }
                )
    return found


def choose_geometry(code: str, osm_items: list[dict], weebly_items: list[dict], override: dict) -> str:
    preference = (override.get("geometry") or "").lower()
    if preference == "weebly" and weebly_items:
        return "weebly"
    if preference == "osm" and any(item["parts"] for item in osm_items):
        return "osm"
    if any(item["parts"] for item in osm_items):
        return "osm"
    if weebly_items:
        return "weebly"
    return "none"


def pooled(items: list[dict]) -> list[list[tuple[float, float]]]:
    lines = []
    for item in items:
        lines.extend(part for part in item["parts"] if len(part) >= 2)
    return lines


def feature_from_parts(code: str, parts, props: dict) -> dict | None:
    geometry = as_geometry(parts)
    if geometry is None:
        return None
    return {"type": "Feature", "geometry": geometry, "properties": props}


def md_cell(value) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "/").replace("\n", " ")


def build() -> None:
    osm_path = latest_raw("puj")
    osm_items, raw_stops = osm_routes(osm_path) if osm_path else ([], [])
    wee_items = weebly_routes()
    overrides = load_overrides()

    by_code: dict[str, dict] = {}

    def bucket(code: str) -> dict:
        return by_code.setdefault(code, {"osm": [], "weebly": []})

    for item in osm_items:
        if item["code"]:
            bucket(item["code"])["osm"].append(item)
    for item in wee_items:
        code = item["page_code"] or item["code"]
        if code:
            bucket(code)["weebly"].append(item)

    for code in overrides:
        bucket(code)

    features = []
    catalog = []
    today = date.today().isoformat()

    for code in sorted(by_code, key=lambda c: (family_of(c), c)):
        group = by_code[code]
        override = overrides.get(code, {})
        osm_lines = pooled(group["osm"])
        wee_lines = pooled(group["weebly"])
        osm_cov = coverage(_samples(osm_lines), wee_lines) if osm_lines and wee_lines else None
        wee_cov = coverage(_samples(wee_lines), osm_lines) if osm_lines and wee_lines else None

        auto_status = "unconfirmed"
        if osm_cov is not None and wee_cov is not None:
            lo, hi = sorted((osm_cov, wee_cov))
            if hi < 0.55 or (lo < 0.35 and hi < 0.80):
                auto_status = "disputed"

        status = override.get("status") or auto_status
        if status not in STATUSES:
            print(f"Ignoring unknown status for {code}: {status}")
            status = auto_status

        source_kind = choose_geometry(code, group["osm"], group["weebly"], override)
        if source_kind == "osm":
            method = "osm_crosscheck"
            license_name = "ODbL"
            attribution = OSM_ATTRIBUTION
        elif source_kind == "weebly":
            method = "weebly_kml"
            license_name = "CC BY-NC 3.0"
            attribution = WEEBLY_ATTRIBUTION
        else:
            method = "none"
            license_name = None
            attribution = None

        sources = []
        for item in group["osm"]:
            sources.append(f"osm:relation/{item['osm_id']}")
        pages = []
        for item in group["weebly"]:
            if item.get("page") and item["page"] not in pages:
                pages.append(item["page"])
        sources.extend(pages)
        if source_kind == "weebly":
            sources.append(WEEBLY_ATTRIBUTION)
        elif source_kind == "osm":
            sources.append(OSM_ATTRIBUTION)
            if pages:
                sources.append("cross-check: " + WEEBLY_ATTRIBUTION)

        names = [item["name"] for item in group["osm"] if item.get("name")]
        if not names:
            names = [item["name"] for item in group["weebly"] if item.get("name")]
        from_name = next((item["from"] for item in group["osm"] if item.get("from")), "")
        to_name = next((item["to"] for item in group["osm"] if item.get("to")), "")
        label = names[0] if names else (f"{from_name} – {to_name}".strip(" –") or code)

        stop_names = []
        for stop in raw_stops:
            if stop.get("code") == code and stop["name"] not in stop_names and stop["name"] != "Unnamed stop":
                stop_names.append(stop["name"])

        directions = []
        chosen = group["osm"] if source_kind == "osm" else group["weebly"] if source_kind == "weebly" else []
        item_lengths = [
            sum(line_length_m(part) for part in item["parts"]) for item in chosen if item["parts"]
        ]
        has_real_line = any(length >= 1000 for length in item_lengths)
        mode = "bus" if code.startswith("MY") else "jeep"
        for index, item in enumerate(chosen, start=1):
            if not item["parts"]:
                continue
            this_m = sum(line_length_m(part) for part in item["parts"])
            # Drop map-glitch stubs once a real line exists for the code.
            if this_m < 150 and has_real_line:
                continue
            if source_kind == "osm":
                feature_id = f"{code}-osm-{item['osm_id']}"
                direction_name = item["name"] or f"{item['from']} – {item['to']}".strip(" –") or f"relation {item['osm_id']}"
                origin = item.get("from") or ""
                dest = item.get("to") or ""
            else:
                feature_id = f"{code}-weebly-{index}"
                direction_name = item["name"] or label
                origin, dest = _split_via(direction_name)
            props = {
                "id": feature_id,
                "code": code,
                "direction": direction_name,
                "name": label,
                "from": origin,
                "to": dest,
                "mode": mode,
                "family": family_of(code),
                "stops": stop_names,
                "status": status,
                "years_active": [None, None],
                "verification": {
                    "last_verified": None,
                    "method": method,
                    "by": None,
                    "imported": today,
                },
                "last_seen": None,
                "headway_min": None,
                "lptrp": {"in_plan": "unconfirmed", "plan_route": None},
                "sources": sources,
                "geometry_source": source_kind,
                "license": license_name,
                "attribution": attribution,
                "overlap": {
                    "osm_on_weebly": _round_ratio(osm_cov),
                    "weebly_on_osm": _round_ratio(wee_cov),
                },
                "note": override.get("note") or None,
                "length_km": round(this_m / 1000, 2),
            }
            feature = feature_from_parts(code, item["parts"], props)
            if feature:
                features.append(feature)
                directions.append(
                    {
                        "id": feature_id,
                        "name": direction_name,
                        "from": origin,
                        "to": dest,
                        "length_km": props["length_km"],
                    }
                )

        catalog.append(
            {
                "code": code,
                "name": label,
                "from": from_name or (directions[0]["from"] if directions else ""),
                "to": to_name or (directions[0]["to"] if directions else ""),
                "family": family_of(code),
                "status": status,
                "auto_status": auto_status,
                "method": method,
                "geometry_source": source_kind,
                "license": license_name,
                "length_km": round(max(d["length_km"] for d in directions), 2) if directions else None,
                "directions": directions,
                "stops": stop_names,
                "overlap": {
                    "osm_on_weebly": _round_ratio(osm_cov),
                    "weebly_on_osm": _round_ratio(wee_cov),
                    "threshold_m": 80,
                },
                "osm_relations": [item["osm_id"] for item in group["osm"]],
                "weebly_pages": pages,
                "sources": sources,
                "note": override.get("note") or None,
            }
        )

    stop_features = _stop_features(raw_stops)
    write_outputs(features, catalog, stop_features, today, osm_path)
    _print_summary(catalog)


def _samples(lines: list[list[tuple[float, float]]]) -> list[tuple[float, float]]:
    points = []
    for line in lines:
        points.extend(sample_line(line))
    return points


def _round_ratio(value: float | None):
    return None if value is None else round(value, 3)


def _split_via(name: str) -> tuple[str, str]:
    clean = html.unescape(name)
    match = re.split(r"\s+to\s+|\s+[–—-]\s+", clean, maxsplit=1, flags=re.I)
    if len(match) == 2:
        return match[0].strip(), match[1].strip()
    return "", ""


def _stop_features(stops: list[dict]) -> list[dict]:
    merged: dict[tuple, dict] = {}
    for stop in stops:
        if not stop.get("code"):
            continue
        key = (round(stop["lon"], 5), round(stop["lat"], 5), stop["name"].strip().lower())
        row = merged.setdefault(
            key,
            {
                "name": stop["name"],
                "lon": stop["lon"],
                "lat": stop["lat"],
                "osm_ids": [],
                "routes": [],
            },
        )
        if stop["code"] not in row["routes"]:
            row["routes"].append(stop["code"])
        if stop.get("osm_id") and stop["osm_id"] not in row["osm_ids"]:
            row["osm_ids"].append(stop["osm_id"])
    features = []
    for row in merged.values():
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [round(row["lon"], 6), round(row["lat"], 6)],
                },
                "properties": {
                    "name": row["name"],
                    "type": "stop",
                    "routes": sorted(row["routes"]),
                    "osm_ids": row["osm_ids"],
                    "source": "osm",
                    "license": "ODbL",
                    "attribution": OSM_ATTRIBUTION,
                },
            }
        )
    features.sort(key=lambda f: f["properties"]["name"])
    return features


def write_outputs(features, catalog, stops, today, osm_path: Path | None) -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    geo = {
        "type": "FeatureCollection",
        "properties": {
            "generated": today,
            "about": "Generated by pipeline/build_routes.py. Edit data/overrides.yaml, then rebuild.",
            "osm": OSM_ATTRIBUTION,
            "weebly": WEEBLY_ATTRIBUTION,
            "osm_file": str(osm_path.relative_to(PROCESSED.parents[1])) if osm_path else None,
        },
        "features": features,
    }
    # FeatureCollection extra "properties" is harmless but some tools warn.
    # Keep the license block inside a foreign member named "jeepoi".
    geo = {
        "type": "FeatureCollection",
        "jeepoi": geo["properties"],
        "features": features,
    }
    write_json(PROCESSED / "routes.geojson", geo)
    write_json(
        PROCESSED / "routes.json",
        {
            "generated": today,
            "edit": "data/overrides.yaml",
            "rebuild": "python pipeline/build_routes.py",
            "counts": _counts(catalog),
            "attribution": {"osm": OSM_ATTRIBUTION, "weebly": WEEBLY_ATTRIBUTION},
            "routes": catalog,
        },
    )
    write_json(
        PROCESSED / "stops.geojson",
        {
            "type": "FeatureCollection",
            "jeepoi": {
                "generated": today,
                "attribution": OSM_ATTRIBUTION,
                "note": "Stops present on OSM route relations only. Hail-and-ride streets are not listed.",
            },
            "features": stops,
        },
    )
    (PROCESSED / "ROUTES.md").write_text(_markdown(catalog, today), encoding="utf-8")


def _counts(catalog: list[dict]) -> dict:
    with_geom = [r for r in catalog if r["directions"]]
    return {
        "codes": len(catalog),
        "with_geometry": len(with_geom),
        "from_osm": sum(1 for r in with_geom if r["geometry_source"] == "osm"),
        "from_weebly_only": sum(1 for r in with_geom if r["geometry_source"] == "weebly"),
        "disputed": sum(1 for r in catalog if r["status"] == "disputed"),
        "no_geometry": sum(1 for r in catalog if not r["directions"]),
    }


def _print_summary(catalog: list[dict]) -> None:
    counts = _counts(catalog)
    print(
        "Built {codes} codes, {with_geometry} with a line "
        "({from_osm} from OSM, {from_weebly_only} from weebly only), "
        "{disputed} disputed, {no_geometry} without geometry.".format(**counts)
    )
    print(f"  {PROCESSED / 'routes.geojson'}")
    print(f"  {PROCESSED / 'routes.json'}")
    print(f"  {PROCESSED / 'ROUTES.md'}")


def _markdown(catalog: list[dict], today: str) -> str:
    counts = _counts(catalog)
    lines = [
        "# JeepOI routes",
        "",
        f"Generated {today} by `pipeline/build_routes.py`. This file is an output. "
        "Change a route by editing `data/overrides.yaml`, or replace a bad line by riding it, then rebuild.",
        "",
        "The map reads `routes.geojson`. Lists and the trust ledger read `routes.json`. "
        "Nothing here is marked verified: verification still means a GPS ride.",
        "",
        f"- {counts['codes']} codes",
        f"- {counts['with_geometry']} with geometry ({counts['from_osm']} drawn from OpenStreetMap, {counts['from_weebly_only']} drawn from weebly because OSM had no line)",
        f"- {counts['disputed']} disputed",
        f"- {counts['no_geometry']} still need a waypoint list or a ride",
        "",
        "OpenStreetMap routes were read with `network=LTFRB Region VII` and `route=bus`. "
        "The older wiki tag `PH:PUJ:Metro Cebu` matched nothing on 3 Nov 2026.",
        "",
        "Licenses, per feature: OpenStreetMap geometry is ODbL (© OpenStreetMap contributors). "
        "Weebly geometry is CC BY-NC 3.0, Cebu Jeepney Maps by John Mercado Lee. "
        "Keep both credits. Do not sell the dataset. Route7 was not used.",
        "",
        "## Priority routes",
        "",
        "| Code | On the map | Status | Geometry | Note |",
        "|---|---|---|---|---|",
    ]
    by_code = {row["code"]: row for row in catalog}
    for code in PRIORITY_CODES:
        row = by_code.get(code)
        if row is None:
            lines.append(f"| {code} | missing | — | — | Not in OSM or weebly yet. Add waypoints or ride it. |")
            continue
        present = "yes" if row["directions"] else "no line"
        lines.append(
            f"| {code} | {present} | {row['status']} | {row['geometry_source']} | {md_cell(row.get('note') or '')} |"
        )

    lines += [
        "",
        "## Disputed or worth a look",
        "",
        "Disputed means the two maps disagree, or `overrides.yaml` says so. A ride settles it.",
        "",
        "| Code | Overlap OSM inside weebly | Overlap weebly inside OSM | Note |",
        "|---|---|---|---|",
    ]
    flagged = [
        row for row in catalog
        if row["status"] == "disputed" or (row.get("note"))
    ]
    if not flagged:
        lines.append("| — | — | — | None flagged. |")
    for row in flagged:
        overlap = row["overlap"]
        lines.append(
            "| {code} | {a} | {b} | {note} |".format(
                code=row["code"],
                a=overlap["osm_on_weebly"] if overlap["osm_on_weebly"] is not None else "—",
                b=overlap["weebly_on_osm"] if overlap["weebly_on_osm"] is not None else "—",
                note=md_cell(row.get("note") or row["status"]),
            )
        )

    lines += [
        "",
        "## All codes",
        "",
        "| Code | Name | Status | Geometry | Longest km | Stops named | Sources |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in catalog:
        source_bits = []
        if row["osm_relations"]:
            source_bits.append("OSM " + ", ".join(str(n) for n in row["osm_relations"]))
        if row["weebly_pages"]:
            source_bits.append("weebly")
        lines.append(
            "| {code} | {name} | {status} | {geom} | {length} | {stops} | {sources} |".format(
                code=row["code"],
                name=md_cell(row["name"])[:80],
                status=row["status"],
                geom=row["geometry_source"],
                length=row["length_km"] if row["length_km"] is not None else "—",
                stops=len(row["stops"]),
                sources=md_cell("; ".join(source_bits)),
            )
        )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    build()
