"""Shared helpers for the JeepOI route import.

The processed files are generated. Hand edits belong in data/overrides.yaml.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW_OSM = DATA / "raw" / "osm"
RAW_WEEBLY = DATA / "raw" / "weebly"
PROCESSED = DATA / "processed"
OVERRIDES = DATA / "overrides.yaml"

OSM_ATTRIBUTION = "© OpenStreetMap contributors (ODbL)"
WEEBLY_ATTRIBUTION = (
    "Cebu Jeepney Maps by John Mercado Lee, CC BY-NC 3.0 "
    "(https://creativecommons.org/licenses/by-nc/3.0/). "
    "Source: https://cebujeepneys.weebly.com/"
)
USER_AGENT = "JeepOI-data/0.1 (student project; Cebu jeepney map)"

STATUSES = {
    "verified",
    "reported",
    "disputed",
    "unconfirmed",
    "discontinued",
    "planned",
}

# Routes the plan already says matter most for tourism or a field check.
PRIORITY_CODES = [
    "17B",
    "04L",
    "01K",
    "14D",
    "12G",
    "04B",
    "13C",
    "06H",
    "23",
    "MI-01A",
    "03Q",
    "04M",
    "04A",
    "04I",
]


def code_from_slug(slug: str) -> str | None:
    s = slug.lower().removesuffix(".html").strip("/")
    if re.fullmatch(r"mi-\d+[a-z]?", s) or re.fullmatch(r"\d+[a-z]?", s):
        return s.upper()
    return None


_CODE = re.compile(r"^(?:MI-\d+[A-Z]{0,2}|MY\d+[A-Z]{0,2}|\d+[A-Z]{0,2})$")
_LETTERED = re.compile(r"^(?:MI-\d+[A-Z]{1,2}|MY\d+[A-Z]{1,2}|\d+[A-Z]{1,2})$")


def norm_code(value: str | None) -> str | None:
    """Pull a route code out of a ref, a slug, or a title.

    A bare number such as 23 counts only when it is the whole text or it
    follows "route no.". That keeps "Pier 3" and "23 (Mandaue...)" from
    turning into codes 3 and 23M.
    """
    if not value:
        return None
    raw = " ".join(value.strip().upper().split())
    if _CODE.fullmatch(raw):
        return raw
    numbered = re.search(r"(?:ROUTE\s*)?NO\.?\s*([A-Z]{0,3}-?\d+[A-Z]?)\b", raw)
    if numbered and _CODE.fullmatch(numbered.group(1)):
        return numbered.group(1)
    for token in re.split(r"[\s:()/,.]+", raw):
        token = token.strip("-")
        if _LETTERED.fullmatch(token):
            return token
    return None


def family_of(code: str) -> str:
    match = re.match(r"^(MI|\d+)", code)
    return match.group(1) if match else code


def load_overrides(path: Path = OVERRIDES) -> dict[str, dict[str, str]]:
    """Read the small overrides file. Notes may contain colons; '#' starts a comment."""
    routes: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    if not path.exists():
        return routes
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split(" #", 1)[0].rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.fullmatch(r"routes:\s*", line.strip()):
            continue
        if line.startswith("  ") and not line.startswith("    "):
            key = norm_code(line.strip().rstrip(":")) or line.strip().rstrip(":")
            current = {}
            routes[key] = current
            continue
        if line.startswith("    ") and current is not None and ":" in line:
            key, value = line.strip().split(":", 1)
            current[key.strip()] = value.strip().strip('"').strip("'")
    return routes


def haversine_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    lon1, lat1, lon2, lat2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    dlon, dlat = lon2 - lon1, lat2 - lat1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * 6371000 * math.atan2(math.sqrt(h), math.sqrt(1 - h))


def line_length_m(coords: list[tuple[float, float]]) -> float:
    return sum(haversine_m(a, b) for a, b in zip(coords, coords[1:]))


def _xy(lon: float, lat: float, lon0: float, lat0: float) -> tuple[float, float]:
    x = math.radians(lon - lon0) * math.cos(math.radians(lat0)) * 6371000
    y = math.radians(lat - lat0) * 6371000
    return x, y


def _segment_distance(p, a, b) -> float:
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    den = dx * dx + dy * dy
    if den == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / den))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def sample_line(coords: list[tuple[float, float]], step_m: float = 120, limit: int = 250):
    if len(coords) < 2:
        return list(coords)
    samples = [coords[0]]
    carry = 0.0
    for a, b in zip(coords, coords[1:]):
        dist = haversine_m(a, b)
        if dist == 0:
            continue
        pos = step_m - carry
        while pos <= dist and len(samples) < limit:
            t = pos / dist
            samples.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            pos += step_m
        carry = dist - (pos - step_m)
        if carry < 0:
            carry = 0
    if samples[-1] != coords[-1] and len(samples) < limit:
        samples.append(coords[-1])
    return samples


def coverage(points: list[tuple[float, float]], lines: list[list[tuple[float, float]]], threshold_m: float = 80) -> float | None:
    """Fraction of points that fall within threshold_m of any line."""
    if not points or not lines:
        return None
    segs = []
    for line in lines:
        segs.extend(zip(line, line[1:]))
    if not segs:
        return None
    lon0 = points[0][0]
    lat0 = points[0][1]
    xy_points = [_xy(lon, lat, lon0, lat0) for lon, lat in points]
    xy_segs = [(_xy(a[0], a[1], lon0, lat0), _xy(b[0], b[1], lon0, lat0)) for a, b in segs]
    inside = 0
    for p in xy_points:
        if any(_segment_distance(p, a, b) <= threshold_m for a, b in xy_segs):
            inside += 1
    return inside / len(xy_points)


def round_coords(coords: list[tuple[float, float]]) -> list[list[float]]:
    return [[round(lon, 6), round(lat, 6)] for lon, lat in coords]


def as_geometry(parts: list[list[tuple[float, float]]]) -> dict | None:
    parts = [p for p in parts if len(p) >= 2]
    if not parts:
        return None
    if len(parts) == 1:
        return {"type": "LineString", "coordinates": round_coords(parts[0])}
    return {"type": "MultiLineString", "coordinates": [round_coords(p) for p in parts]}


def flatten_geometry(geometry: dict | None) -> list[list[tuple[float, float]]]:
    if not geometry:
        return []
    if geometry["type"] == "LineString":
        return [[(lon, lat) for lon, lat in geometry["coordinates"]]]
    if geometry["type"] == "MultiLineString":
        return [[(lon, lat) for lon, lat in line] for line in geometry["coordinates"]]
    return []


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
