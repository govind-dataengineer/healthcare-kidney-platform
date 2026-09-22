#!/usr/bin/env python3
"""Emit a synthetic APD therapy lifecycle to a Kinesis stream."""

from __future__ import annotations

import argparse
import json
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Iterable

import boto3

DEFAULT_STREAM_NAME = "therapy-events"


@dataclass(frozen=True)
class TherapyContext:
    """Identifiers shared by all events in one synthetic therapy session."""

    run_id: str
    session_id: str
    device_id: str
    patient_id: str


def timestamp() -> str:
    """Return a timezone-aware timestamp in a portable JSON format."""
    return datetime.now(UTC).isoformat()


def event(context: TherapyContext, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Build one versioned event envelope."""
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "event_timestamp": timestamp(),
        "schema_version": "1.0",
        **asdict(context),
        "payload": payload,
    }


def build_session_events(context: TherapyContext, cycle_count: int) -> list[dict[str, Any]]:
    """Return a complete synthetic APD therapy lifecycle in clinical order."""
    if cycle_count < 1:
        raise ValueError("cycle_count must be at least 1")

    events = [
        event(
            context,
            "therapy_started",
            {
                "therapy_modality": "APD",
                "prescribed_cycle_count": cycle_count,
                "prescribed_fill_volume_ml": 2000,
                "prescribed_dwell_minutes": 90,
            },
        ),
        event(
            context,
            "initial_drain",
            {"drained_volume_ml": 420, "drain_duration_seconds": 310},
        ),
    ]

    total_ultrafiltration_ml = 420
    for cycle_number in range(1, cycle_count + 1):
        fill_volume_ml = 2000
        drain_volume_ml = 2130 + (cycle_number * 15)
        total_ultrafiltration_ml += drain_volume_ml - fill_volume_ml
        events.extend(
            [
                event(
                    context,
                    "cycle_fill",
                    {
                        "cycle_number": cycle_number,
                        "prescribed_fill_volume_ml": fill_volume_ml,
                        "actual_fill_volume_ml": fill_volume_ml,
                        "fill_duration_seconds": 245,
                    },
                ),
                event(
                    context,
                    "cycle_dwell_completed",
                    {
                        "cycle_number": cycle_number,
                        "prescribed_dwell_minutes": 90,
                        "actual_dwell_minutes": 89,
                    },
                ),
                event(
                    context,
                    "cycle_drain",
                    {
                        "cycle_number": cycle_number,
                        "drained_volume_ml": drain_volume_ml,
                        "drain_duration_seconds": 330,
                    },
                ),
            ]
        )

    events.extend(
        [
            event(
                context,
                "last_fill",
                {"last_fill_volume_ml": 1800, "fill_duration_seconds": 230},
            ),
            event(
                context,
                "therapy_completed",
                {
                    "cycle_count_completed": cycle_count,
                    "total_therapy_minutes": (cycle_count * 96) + 15,
                    "total_ultrafiltration_ml": total_ultrafiltration_ml,
                    "therapy_status": "completed",
                },
            ),
        ]
    )
    return events


def publish_events(
    events: Iterable[dict[str, Any]], *, endpoint_url: str, stream_name: str, interval_seconds: float
) -> int:
    """Publish events in order, using device_id to preserve device ordering."""
    client = boto3.client(
        "kinesis",
        endpoint_url=endpoint_url,
        region_name="us-east-1",
        aws_access_key_id="local",
        aws_secret_access_key="local",
    )
    published = 0
    for record in events:
        client.put_record(
            StreamName=stream_name,
            PartitionKey=record["device_id"],
            Data=json.dumps(record).encode("utf-8"),
        )
        published += 1
        print(
            f"published {record['event_type']:<24} "
            f"session={record['session_id']} device={record['device_id']}"
        )
        if interval_seconds > 0:
            time.sleep(interval_seconds)
    return published


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint-url", default="http://localhost:4567")
    parser.add_argument("--stream-name", default=DEFAULT_STREAM_NAME)
    parser.add_argument("--device-id", default="claria-sim-001")
    parser.add_argument("--patient-id", default="patient-synthetic-001")
    parser.add_argument("--cycle-count", type=int, default=3)
    parser.add_argument("--interval-seconds", type=float, default=2.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.interval_seconds < 0:
        raise ValueError("interval_seconds cannot be negative")

    context = TherapyContext(
        run_id=str(uuid.uuid4()),
        session_id=str(uuid.uuid4()),
        device_id=args.device_id,
        patient_id=args.patient_id,
    )
    events = build_session_events(context, args.cycle_count)
    count = publish_events(
        events,
        endpoint_url=args.endpoint_url,
        stream_name=args.stream_name,
        interval_seconds=args.interval_seconds,
    )
    print(f"completed run={context.run_id}; published {count} events")


if __name__ == "__main__":
    main()
