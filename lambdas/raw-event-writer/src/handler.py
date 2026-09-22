"""Kinesis Lambda handler that validates events and stores raw JSON in S3."""

from __future__ import annotations

import base64
import json
import os
from datetime import datetime
from typing import Any

import boto3

REQUIRED_FIELDS = {"event_id", "event_type", "event_timestamp", "run_id", "session_id", "device_id", "patient_id", "payload"}


def decode_kinesis_record(record: dict[str, Any]) -> dict[str, Any]:
    """Decode Kinesis transport Base64 into the project's plain JSON event."""
    encoded_data = record["kinesis"]["data"]
    decoded = base64.b64decode(encoded_data)
    return json.loads(decoded.decode("utf-8"))


def validate_event(event: dict[str, Any]) -> None:
    """Validate the minimum contract needed to safely persist a raw event."""
    missing_fields = REQUIRED_FIELDS.difference(event)
    if missing_fields:
        raise ValueError(f"event is missing required fields: {sorted(missing_fields)}")
    if not isinstance(event["payload"], dict):
        raise ValueError("event payload must be a JSON object")


def object_key(event: dict[str, Any]) -> str:
    """Create an immutable, query-friendly S3 location for one raw event."""
    event_date = datetime.fromisoformat(event["event_timestamp"].replace("Z", "+00:00")).date().isoformat()
    return (
        f"raw/run_id={event['run_id']}/dt={event_date}/device_id={event['device_id']}/"
        f"{event['event_timestamp'].replace(':', '-')}_{event['event_id']}.json"
    )


def s3_client() -> Any:
    """Use Floci from inside the Lambda container or AWS in a deployed environment."""
    endpoint_url = os.getenv("FLOCI_ENDPOINT_URL")
    return boto3.client("s3", endpoint_url=endpoint_url) if endpoint_url else boto3.client("s3")


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, int]:
    """Persist each Kinesis record as an immutable JSON object in the raw bucket."""
    bucket = os.environ["RAW_BUCKET"]
    s3 = s3_client()
    written = 0

    for record in event.get("Records", []):
        raw_event = decode_kinesis_record(record)
        validate_event(raw_event)
        s3.put_object(
            Bucket=bucket,
            Key=object_key(raw_event),
            Body=json.dumps(raw_event, separators=(",", ":")).encode("utf-8"),
            ContentType="application/json",
        )
        written += 1

    return {"written": written}
