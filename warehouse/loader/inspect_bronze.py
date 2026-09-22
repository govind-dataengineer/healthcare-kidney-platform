"""Print concise Bronze-layer counts for the local learning environment."""

from __future__ import annotations

import os

import json
from pathlib import Path

status_path = Path(f"{os.environ['DUCKDB_PATH']}.status.json")
if not status_path.exists():
    raise SystemExit("Bronze status is not available yet. Wait for the loader's first polling cycle.")

status = json.loads(status_path.read_text(encoding="utf-8"))
print(f"Bronze events: {status['bronze_events']}")
print(f"Raw S3 objects ingested: {status['raw_s3_objects_ingested']}")
print(f"Updated at: {status['updated_at']}")
