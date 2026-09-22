"""Continuously load immutable raw APD JSON events from S3 into DuckDB Bronze."""

from __future__ import annotations

import json
import os
import time
from datetime import UTC, datetime
from typing import Any, Iterable

import boto3
import duckdb


def s3_client() -> Any:
    return boto3.client(
        "s3",
        endpoint_url=os.environ["FLOCI_ENDPOINT_URL"],
        region_name="us-east-1",
        aws_access_key_id="local",
        aws_secret_access_key="local",
    )


def initialise_database(connection: duckdb.DuckDBPyConnection) -> None:
    connection.execute("CREATE SCHEMA IF NOT EXISTS bronze")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS bronze.raw_therapy_event (
            event_id VARCHAR PRIMARY KEY,
            event_type VARCHAR NOT NULL,
            event_timestamp TIMESTAMPTZ NOT NULL,
            schema_version VARCHAR NOT NULL,
            run_id VARCHAR NOT NULL,
            session_id VARCHAR NOT NULL,
            device_id VARCHAR NOT NULL,
            patient_id VARCHAR NOT NULL,
            payload JSON NOT NULL,
            source_s3_key VARCHAR NOT NULL UNIQUE,
            ingested_at TIMESTAMPTZ NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS bronze.ingest_log (
            source_s3_key VARCHAR PRIMARY KEY,
            source_etag VARCHAR,
            rows_loaded INTEGER NOT NULL,
            loaded_at TIMESTAMPTZ NOT NULL
        )
        """
    )


def list_raw_objects(client: Any, bucket: str) -> Iterable[dict[str, Any]]:
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix="raw/"):
        yield from page.get("Contents", [])


def already_loaded(connection: duckdb.DuckDBPyConnection, key: str) -> bool:
    return connection.execute(
        "SELECT EXISTS(SELECT 1 FROM bronze.ingest_log WHERE source_s3_key = ?)", [key]
    ).fetchone()[0]


def load_object(
    connection: duckdb.DuckDBPyConnection, client: Any, bucket: str, object_metadata: dict[str, Any]
) -> bool:
    key = object_metadata["Key"]
    if already_loaded(connection, key):
        return False

    response = client.get_object(Bucket=bucket, Key=key)
    raw_event = json.loads(response["Body"].read().decode("utf-8"))
    required_fields = {
        "event_id", "event_type", "event_timestamp", "schema_version", "run_id", "session_id", "device_id", "patient_id", "payload"
    }
    missing = required_fields.difference(raw_event)
    if missing:
        raise ValueError(f"raw object {key} is missing event fields: {sorted(missing)}")

    now = datetime.now(UTC)
    connection.execute(
        """INSERT INTO bronze.raw_therapy_event VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [raw_event["event_id"], raw_event["event_type"], raw_event["event_timestamp"], raw_event["schema_version"], raw_event["run_id"], raw_event["session_id"], raw_event["device_id"], raw_event["patient_id"], json.dumps(raw_event["payload"]), key, now],
    )
    connection.execute(
        "INSERT INTO bronze.ingest_log VALUES (?, ?, ?, ?)", [key, object_metadata.get("ETag"), 1, now]
    )
    print(f"loaded bronze event={raw_event['event_type']} key={key}", flush=True)
    return True


def run_once(connection: duckdb.DuckDBPyConnection, client: Any, bucket: str) -> int:
    return sum(int(load_object(connection, client, bucket, object_metadata)) for object_metadata in list_raw_objects(client, bucket))


def write_status(connection: duckdb.DuckDBPyConnection, database_path: str) -> None:
    """Publish counts outside DuckDB so another process can inspect a live loader."""
    status = {
        "bronze_events": connection.execute("SELECT count(*) FROM bronze.raw_therapy_event").fetchone()[0],
        "raw_s3_objects_ingested": connection.execute("SELECT count(*) FROM bronze.ingest_log").fetchone()[0],
        "updated_at": datetime.now(UTC).isoformat(),
    }
    status_path = f"{database_path}.status.json"
    temporary_path = f"{status_path}.tmp"
    with open(temporary_path, "w", encoding="utf-8") as status_file:
        json.dump(status, status_file)
    os.replace(temporary_path, status_path)


def main() -> None:
    database_path = os.environ["DUCKDB_PATH"]
    connection = duckdb.connect(database_path)
    bucket = os.environ["RAW_BUCKET"]
    interval_seconds = float(os.environ.get("POLL_INTERVAL_SECONDS", "5"))
    initialise_database(connection)
    client = s3_client()
    print(f"Bronze loader started: bucket={bucket}", flush=True)
    while True:
        try:
            loaded = run_once(connection, client, bucket)
            write_status(connection, database_path)
            if loaded:
                print(f"Bronze batch complete: loaded={loaded}", flush=True)
        except Exception as error:
            print(f"Bronze loader retrying after error: {error}", flush=True)
        time.sleep(interval_seconds)


if __name__ == "__main__":
    main()
