"""Fail loudly if the processed files break the plan's data rules (plan.md 7.6, 7.8).

    python pipeline/check_data.py
"""

from __future__ import annotations

from build_routes import GAP_M, max_gap_m
from common import PROCESSED, STATUSES, read_json


def main() -> None:
    routes = read_json(PROCESSED / "routes.geojson")["features"]
    stops = read_json(PROCESSED / "stops.geojson")["features"]
    broken = []
    for f in routes:
        p = f["properties"]
        assert p["direction"] in {"outbound", "inbound"}, p["id"]
        assert p["status"] in STATUSES, p["id"]
        assert p["sources"], f"{p['id']}: nothing goes on the map without a source"
        assert p["attribution"], p["id"]
        g = f["geometry"]
        parts = [g["coordinates"]] if g["type"] == "LineString" else g["coordinates"]
        if max_gap_m([[tuple(c) for c in part] for part in parts]) > GAP_M:
            broken.append(p["id"])
    names = [s["properties"]["name"] for s in stops]
    assert all(n and n != "Unnamed stop" for n in names)
    no_stops = sorted({f["properties"]["code"] for f in routes if not f["properties"]["stops"]})
    print(f"OK: {len(routes)} route lines, {len(stops)} named stops.")
    print(f"Lines with gaps over {GAP_M} m (draw only, don't route on them): {len(broken)} {broken}")
    print(f"Codes with no named stops yet: {len(no_stops)} {no_stops}")


if __name__ == "__main__":
    main()
