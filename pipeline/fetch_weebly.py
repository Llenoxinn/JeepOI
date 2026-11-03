"""Download Cebu Jeepney Maps geometry from cebujeepneys.weebly.com.

Each route page embeds a classic Google My Map (an msid). Google returns a KMZ
when asked for KML. The file is stored as downloaded. The site licenses the
maps CC BY-NC 3.0, so the build step credits John Mercado Lee on every route
that uses this geometry. This does not touch Route7.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date

from common import RAW_WEEBLY, USER_AGENT, code_from_slug

SITEMAP = "https://cebujeepneys.weebly.com/sitemap.xml"
SKIP_SLUGS = {
    "index",
    "jeepney-routes",
    "about",
    "contact",
    "store",
    "sitemap",
}


def get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last: Exception | None = None
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            last = exc
            time.sleep(1 + attempt)
    raise last  # type: ignore[misc]


def map_ids(html: str) -> list[str]:
    found = re.findall(r"msid=([0-9]+\.[0-9A-Za-z]+)", html)
    found += re.findall(r"[?&]mid=([A-Za-z0-9_-]{8,})", html)
    unique = []
    for item in found:
        if item not in unique:
            unique.append(item)
    return unique


def kml_url(map_id: str) -> str:
    if re.fullmatch(r"[0-9]+\.[0-9A-Za-z]+", map_id):
        return f"https://maps.google.com/maps/ms?msa=0&output=kml&msid={map_id}"
    return f"https://www.google.com/maps/d/kml?mid={map_id}&forcekml=1"


def main() -> None:
    today = date.today().isoformat()
    kml_dir = RAW_WEEBLY / "kmz"
    kml_dir.mkdir(parents=True, exist_ok=True)

    print("Reading sitemap...")
    xml = get(SITEMAP).decode("utf-8", "replace")
    pages = re.findall(r"<loc>([^<]+)</loc>", xml)
    print(f"  {len(pages)} pages", flush=True)

    manifest = {
        "fetched": today,
        "license": "CC BY-NC 3.0",
        "attribution": "Cebu Jeepney Maps by John Mercado Lee",
        "source": "https://cebujeepneys.weebly.com/",
        "pages": [],
    }
    saved = 0
    out = RAW_WEEBLY / "manifest.json"

    for index, page in enumerate(pages, start=1):
        slug = page.rstrip("/").rsplit("/", 1)[-1].removesuffix(".html")
        entry = {"page": page, "slug": slug, "code": code_from_slug(slug), "maps": [], "error": None}
        if slug.lower() in SKIP_SLUGS:
            entry["skipped"] = "index page"
            manifest["pages"].append(entry)
            continue
        print(f"  {index}/{len(pages)} {slug}", flush=True)
        try:
            html = get(page).decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - keep going through the whole sitemap
            entry["error"] = f"page: {exc}"
            manifest["pages"].append(entry)
            print(f"  fail page {slug}: {exc}", flush=True)
            time.sleep(0.5)
            continue

        ids = map_ids(html)
        licensed = "creativecommons.org/licenses/by-nc/3.0" in html
        entry["license_badge"] = licensed
        if not ids:
            entry["error"] = "no map id"
            manifest["pages"].append(entry)
            print(f"  {index}/{len(pages)} {slug}: no map", flush=True)
            time.sleep(0.4)
            continue

        for nth, map_id in enumerate(ids, start=1):
            suffix = "" if nth == 1 else f"-{nth}"
            stem = f"{slug}{suffix}"
            target = kml_dir / f"{stem}.kmz"
            url = kml_url(map_id)
            record = {"id": map_id, "url": url, "file": str(target.relative_to(RAW_WEEBLY))}
            if target.exists() and target.stat().st_size > 200:
                record["bytes"] = target.stat().st_size
                record["reused"] = True
                entry["maps"].append(record)
                saved += 1
                continue
            try:
                blob = get(url, timeout=40)
            except Exception as exc:  # noqa: BLE001
                record["error"] = str(exc)
                entry["maps"].append(record)
                print(f"  fail kml {stem}: {exc}")
                time.sleep(0.8)
                continue
            if blob[:1] == b"<" or blob[:15].lower().startswith(b"<!doctype"):
                record["error"] = "response was HTML, not a map"
                entry["maps"].append(record)
                continue
            target.write_bytes(blob)
            record["bytes"] = len(blob)
            entry["maps"].append(record)
            saved += 1
            time.sleep(0.6)

        manifest["pages"].append(entry)
        out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"    saved {len(entry['maps'])}", flush=True)
        time.sleep(0.4)

    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {saved} map files. Manifest: {out}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
