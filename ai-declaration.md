# AI declaration

JeepOI is a student side project. We use AI coding tools, and we say where, so anyone reading the code or the data knows what a person checked and what a tool wrote.

## Tools

| Tool | What it did | Where it shows |
|---|---|---|
| **Cursor** (agent mode) | Wrote the first version of the data and pipeline: the OSM and weebly downloaders, the route builder, the overrides file and the generated route files. | Commit `a31b971`|
| **Claude Code** | Reviewed the processed data against `plan.md`, then fixed the builder: joins OSM road pieces in any order, sets real outbound/inbound directions, drops drawing scraps, merges duplicate stops, keeps credits out of `sources`. Added `pipeline/check_data.py`. Drafted this file, `architecture.md`, `design.md`, `data.md` and the GitHub issue templates. | Commit `23b75f9` and the commits that add these docs |

## What AI did not do

- **It verified nothing on the road.** Every route says `unconfirmed` until one of us rides it with GPS. A tool can't change that status, and only a ride, a dated document or a team decision in `data/overrides.yaml` can.
- **It did not choose data sources or licenses.** The team chose OpenStreetMap and cebujeepneys.weebly, and decided not to use Route7 or 3D Universal (`plan.md` section 7.1).
- **It does not answer riders.** If Jepoy (the chat helper, v2) ships, it only repeats what our own planner and route files return (`plan.md` section 5.6).

## Our rules for using AI here

1. A person reads every AI change before it is committed, and the commit says when a tool co-wrote it.
2. Generated data is checked by `pipeline/check_data.py`, and `data/processed/ROUTES.md` is reviewed by eye before a push.
3. No AI-made facts in the data: every route, stop, fare and spot needs a real source in `sources`.
4. New AI use (new tool, or AI in a new part of the project) gets a row in the table above.
