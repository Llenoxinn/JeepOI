# Architecture

**One rule:** do everything heavy offline in Python, ship static files, and run the trip search in the browser. Cebu has no live jeep feed, so there is nothing a server would add yet (`plan.md` section 8.7).

```
 OpenStreetMap (Overpass)      cebujeepneys.weebly (KMZ)      our GPS rides (later)
          │                              │                            │
   fetch_osm.py                   fetch_weebly.py                 (not built)
          ▼                              ▼                            ▼
   data/raw/osm/*.json          data/raw/weebly/kmz + manifest   data/raw/rides/*.gpx
          └──────────────┬───────────────┘
                         ▼
   data/overrides.yaml ─► build_routes.py ─► check_data.py
                         ▼
   data/processed/  routes.geojson · routes.json · stops.geojson · ROUTES.md
                         ▼
                  build_graph.py (not built) ─► graph.<hash>.json
                         ▼
   Browser app:  MapLibre map · route explorer · Dijkstra planner · fares.json
```

## 1. Ingestion

Run everything with `python pipeline/run.py` (or `pipeline/run.ps1` on Windows). It runs the four steps in order and stops at the first failure.

| Step | Script | Reads | Writes | Notes |
|---|---|---|---|---|
| 1 | `fetch_osm.py` | Overpass API (de → fr → kumi fallback) | `data/raw/osm/puj-YYYY-MM-DD.json` + `.meta.json`, `bus-…` | Query: `network=LTFRB Region VII` + `route=bus` inside the Metro Cebu box, plus the old `PH:PUJ:Metro Cebu` tag. The meta file keeps the exact query, endpoint and OSM timestamp. |
| 2 | `fetch_weebly.py` | weebly sitemap, then each page's Google My Map | `data/raw/weebly/kmz/*.kmz`, `manifest.json` | Pages with no map, or a map Google won't serve, are logged in the manifest with an `error`. |
| 3 | `build_routes.py` | newest raw OSM file, weebly manifest, `overrides.yaml` | everything in `data/processed/` | Regenerates from scratch. Never hand-edit outputs. |
| 4 | `check_data.py` | `data/processed/` | console report | Fails on rule breaks (`data.md`). Lists lines with gaps and codes with no named stops. |

**Raw files are never edited.** Each download is dated in its filename, so an old build can be reproduced and route changes can be diffed over time (ghost routes, `plan.md` section 7.7).

To rebuild without downloading again, run only `python pipeline/build_routes.py` and then `python pipeline/check_data.py`.

## 2. How `build_routes.py` decides

1. **Group by code.** OSM `ref`/`name` and the weebly page slug are normalized to one code (`13C`, `MI-01A`, `MY01`).
2. **Join OSM road pieces.** Each relation's ways are joined to the nearest remaining piece (under 35 m), whatever order OSM lists them in. Then the line is turned so that the relation's first way is at the start, because way node order means nothing in OSM.
3. **Compare the two sources.** Points every 120 m on one line are checked against the other (80 m tolerance). Low overlap both ways → `disputed`.
4. **Pick the geometry.** Use `overrides.yaml` if it names one. Otherwise use OSM, unless the OSM line has a hole over 300 m and weebly has the route, in which case use weebly.
5. **Drop scraps.** Any line shorter than a quarter of the code's longest line is a drawing leftover.
6. **Set direction.** The first line is `outbound`. A later line that starts where the first one ended is `inbound`.
7. **Stops.** Named stop nodes on OSM relations only. Same name within 200 m = one stop.
8. **Apply overrides** (status, note, geometry choice), then write the outputs and `ROUTES.md`.

## 3. Serving the data to the app

| App part | Loads | When |
|---|---|---|
| Map layers | `routes.geojson`, `stops.geojson` | On app start, as MapLibre GeoJSON sources |
| Route explorer, trust ledger | `routes.json` | On app start (small, no coordinates) |
| Fares | `data/fares.json` | On app start; the rule whose dates cover today wins |
| Trip planner | `graph.<hash>.json` | First search, then cached by the browser and CDN |

## 4. The planner graph (next to build)

`pipeline/build_graph.py` will read `routes.geojson` + `stops.geojson` and:

- place a stop every 150–200 m along each line, and snap named stops onto it;
- make a street node per stop and an on-board node per (stop, route) pair;
- add ride, board (wait), alight, and walk (≤ 300 m, 1.2 m/s, straight line × 1.3) edges;
- weight ride edges by segment length ÷ speed. Until `speeds.json` exists, use one flat speed and label times as estimates;
- skip lines that `check_data.py` reports with gaps;
- write `graph.<content-hash>.json`.

The browser finds the nearest stops with `kdbush` and runs Dijkstra with a binary heap. That's about 10,000 nodes, a few milliseconds on a phone. Move the search to a serverless function only past 100,000 nodes, 300 ms on a phone, or live data (`plan.md` section 8.7).

## 5. Stack

React + TypeScript + Vite, MapLibre GL JS on an OpenFreeMap/Protomaps basemap, deck.gl `TripsLayer` for animated jeeps, Turf.js, GSAP ScrollTrigger, Tailwind. Data pipeline in Python. Hosting on Vercel or Netlify. Reports via Google Form (v1), Supabase (v2). Full reasoning in `plan.md` section 10.

## 6. Not built yet

- `build_graph.py` and `graph.json`
- GPS ride ingestion (GPX → map-matched line → `ridden_gps` verification)
- `speeds.json`, `spots.json`, `route_history.json`
- A GitHub Action that rebuilds and runs the 20 test trips on every `data/` change
- The bus file (`bus-*.json`) is downloaded but not read by `build_routes.py`. MyBus lines currently come through the jeep query.
