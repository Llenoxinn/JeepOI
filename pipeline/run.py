"""Download OSM and weebly, then rebuild the route files.

    python pipeline/run.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    py = sys.executable
    for script in ("fetch_osm.py", "fetch_weebly.py", "build_routes.py"):
        print(f"\n== {script} ==")
        subprocess.check_call([py, str(HERE / script)])


if __name__ == "__main__":
    main()
