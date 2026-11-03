"""Download Metro Cebu jeepney route relations from the Overpass API.

Saves the response untouched in data/raw/osm/. Run build_routes.py afterwards.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

from common import RAW_OSM, USER_AGENT, write_json

# de is kept first: on 3 Nov 2026 kumi was still serving a 15 July extract,
# which omitted routes mapped since then (including 13C and 17B).
ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.openstreetmap.fr/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

# The wiki still mentions network=PH:PUJ:Metro Cebu. Live data (Nov 2026) uses
# network=LTFRB Region VII and route=bus for the numbered jeepney codes.
# The old tag is kept so a future remap is still picked up.
JEEP_QUERY = """
[out:json][timeout:180];
(
  relation["network"="LTFRB Region VII"]["route"="bus"](10.05,123.55,10.60,124.15);
  relation["network"="PH:PUJ:Metro Cebu"];
)->.routes;
.routes out geom;
(
  node(r.routes:"stop");
  node(r.routes:"platform");
  node(r.routes:"stop_entry_only");
  node(r.routes:"stop_exit_only");
  node(r.routes:"platform_entry_only");
  node(r.routes:"platform_exit_only");
);
out;
""".strip()

# Separate file so a bus-tag experiment cannot drown the jeepney pull.
BUS_QUERY = """
[out:json][timeout:120];
(
  relation["type"="route"]["network"~"CEBRT|CBRT|MyBus",i](10.10,123.60,10.55,124.10);
);
out geom;
""".strip()


def fetch(query: str) -> tuple[str, dict]:
    body = urllib.parse.urlencode({"data": query}).encode("utf-8")
    last_error = "no endpoint tried"
    freshest: tuple[str, dict, str] | None = None
    for url in ENDPOINTS:
        req = urllib.request.Request(
            url,
            data=body,
            headers={"User-Agent": USER_AGENT, "Content-Type": "application/x-www-form-urlencoded"},
        )
        try:
            with urllib.request.urlopen(req, timeout=200) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = f"{url}: {exc}"
            print(last_error, file=sys.stderr)
            continue
        if "elements" not in payload:
            last_error = f"{url} returned no elements: {str(payload)[:240]}"
            print(last_error, file=sys.stderr)
            continue
        stamp = (payload.get("osm3s") or {}).get("timestamp_osm_base") or ""
        print(f"  {url} osm timestamp {stamp or 'unknown'}")
        if freshest is None or stamp > freshest[2]:
            freshest = (url, payload, stamp)
        if stamp >= "2026-10-01":
            return url, payload
    if freshest:
        print(f"warning: freshest extract is still {freshest[2]}", file=sys.stderr)
        return freshest[0], freshest[1]
    raise SystemExit(f"Overpass download failed. {last_error}")


def save(kind: str, query: str) -> None:
    print(f"Fetching {kind} routes...")
    url, payload = fetch(query)
    elements = payload.get("elements", [])
    relations = [el for el in elements if el.get("type") == "relation"]
    today = date.today().isoformat()
    RAW_OSM.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_OSM / f"{kind}-{today}.json"
    raw_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    write_json(
        RAW_OSM / f"{kind}-{today}.meta.json",
        {
            "fetched": today,
            "endpoint": url,
            "query": query,
            "relation_count": len(relations),
            "osm_timestamp": (payload.get("osm3s") or {}).get("timestamp_osm_base"),
            "license": "ODbL",
            "attribution": "© OpenStreetMap contributors",
        },
    )
    print(f"  {len(relations)} relations -> {raw_path}")


def main() -> None:
    save("puj", JEEP_QUERY)
    try:
        save("bus", BUS_QUERY)
    except SystemExit as exc:
        print(f"Bus pull skipped: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
