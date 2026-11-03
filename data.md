# Data

How JeepOI's data should look, and the rules it must follow. The pipeline is in `architecture.md`. The full reasoning is in `plan.md` section 7.

## Folders

| Path | What | Edit by hand? |
|---|---|---|
| `data/raw/osm/` | Overpass downloads, dated (`puj-2026-11-03.json`) with a `.meta.json` (query, endpoint, OSM timestamp) | Never |
| `data/raw/weebly/` | KMZ maps + `manifest.json` (page, map id, errors) | Never |
| `data/raw/rides/` | GPX from our rides: `<code>_<outbound/inbound>_<YYYY-MM-DD>_<AM/PM>_<person>.gpx` (planned) | Never, after upload |
| `data/overrides.yaml` | Status, note, or geometry choice per code | **Yes, the only route file you edit** |
| `data/fares.json` | Dated fare rules | Yes |
| `data/processed/` | Generated outputs | Never. Rebuild instead. |

## Rules (`plan.md` section 7.8)

1. **Nothing goes on the map without a source.** Every feature has at least one entry in `sources`.
2. **Every route shows its status and date.** `status` is required, and `verification.last_verified` stays `null` until someone has actually checked it.
3. **Unverified is labeled, never hidden, and never dressed up.** Only a GPS ride, a dated official document, or a team decision in `overrides.yaml` moves a route to `verified`.
4. **Every feature carries its license and credit.** OSM geometry: ODbL, "© OpenStreetMap contributors". Weebly geometry: CC BY-NC 3.0, Cebu Jeepney Maps by John Mercado Lee. Do not sell the dataset.
5. **Never use** Route7's data or 3D Universal's code tables.
6. **Freshness:** flag routes with no sighting in 60 days, re-ride core routes every 6 months, and show "fare may be outdated" when a fare rule is more than 6 months unchecked.

`python pipeline/check_data.py` enforces rules 1, 2 and 4 plus the field values below.

## `routes.geojson`: one feature per route per direction

```jsonc
{
  "type": "Feature",
  "geometry": { "type": "LineString", "coordinates": [[123.89, 10.33], "..."] },
  "properties": {
    "id": "13C-osm-21251275",          // <code>-<osm|weebly>-<relation id or index>
    "code": "13C",
    "direction": "outbound",            // outbound | inbound
    "headsign": "Talamban-Ayala-Colon", // the source's own name for this direction
    "name": "Talamban-Ayala-Colon",
    "from": "Colon", "to": "Talamban",
    "mode": "jeep",                     // jeep | modern_jeep | brt | bus
    "family": "13",
    "stops": ["Colon Obelisk", "..."],  // named stops in order seen; may be empty
    "status": "unconfirmed",            // verified | reported | disputed | unconfirmed | discontinued | planned
    "years_active": [null, null],       // [first year, last year]; null last = still running
    "verification": {
      "last_verified": null,            // YYYY-MM-DD, only after a real check
      "method": "osm_crosscheck",       // ridden_gps | osm_crosscheck | weebly_kml | dated_guide | document | none
      "by": null,                       // team member
      "imported": "2026-11-03"
    },
    "last_seen": null,                  // latest sighting, YYYY-MM-DD
    "headway_min": null,
    "lptrp": { "in_plan": "unconfirmed", "plan_route": null },
    "sources": ["osm:relation/21251275", "https://cebujeepneys.weebly.com/13c.html"],
    "geometry_source": "osm",           // osm | weebly | ride
    "license": "ODbL",
    "attribution": "© OpenStreetMap contributors (ODbL)",
    "overlap": { "osm_on_weebly": 1.0, "weebly_on_osm": 1.0 },
    "note": null,
    "length_km": 9.1
  }
}
```

- Prefer one `LineString` per direction. A `MultiLineString` means the source line has holes: draw it, but don't route on it until it's fixed or ridden.
- Coordinates are `[lon, lat]`, WGS84, 6 decimals.
- A code with only an `outbound` feature has one source line covering both ways, or is a loop.

## `routes.json`: one record per code, no coordinates

For lists and the trust ledger: `code`, `name`, `from`, `to`, `family`, `status`, `auto_status`, `method`, `geometry_source`, `license`, `length_km`, `directions[]` (id, direction, name, from, to, length_km), `stops`, `overlap`, `osm_relations`, `weebly_pages`, `sources`, `note`. The top level also has `generated`, `counts` and `attribution`.

## `stops.geojson`: named stops (Points)

```jsonc
{ "name": "Gaisano Capital South", "type": "stop", "routes": ["01B", "09G"],
  "osm_ids": [123, 456], "source": "osm", "license": "ODbL", "attribution": "..." }
```

- Same name within 200 m = one stop (both sides of the road).
- Still to add by hand: `type: terminal | hub`, `aliases` ("Fuente rotunda"), and about 50 landmark stops from rides.

## `fares.json`: dated rules

```jsonc
{ "effective_from": "2026-09-28", "effective_to": "2026-12-31", "label": "...",
  "traditional": { "base": 14, "base_km": 4, "per_km": 2.0 },
  "modern": { "base": 17, "base_km": 4, "per_km": 2.4 },
  "discount": 0.20, "source": "https://...", "verified": false }
```

Never edit an old rule. Add a new one with new dates and keep the old ones for history.

## `overrides.yaml`

```yaml
routes:
  04I:
    status: disputed        # any status above
    geometry: osm           # osm | weebly; omit to let the builder choose
    note: "One line, no '#' character."
```

## Planned files

| File | Holds | Comes from |
|---|---|---|
| `speeds.json` | Speed per route segment per time band | GPS rides |
| `spots.json` | Tourist spots: codes, `alight_at`, `walk_min`, `last_mile`, `confidence`, `last_verified`, `sources` | Research + field checks (`plan.md` section 7.6) |
| `route_history.json` | Dated events per code (`reported_missing`, `confirmed_running`, `discontinued`) with sources | Dated guides, OSM history (`plan.md` section 7.7) |
| `graph.<hash>.json` | Planner nodes and edges | `build_graph.py` |

## Where the data stands (3 Nov 2026)

70 codes, 69 with a line (46 OSM, 23 weebly), 140 direction lines, 352 named stops, **0 verified**. Four lines still have holes (44, 52, 60, MY01). 26 codes have no named stops. See `data/processed/ROUTES.md` for the per-code list.
