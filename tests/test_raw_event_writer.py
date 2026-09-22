from __future__ import annotations

import base64
import json
import sys
import unittest
from pathlib import Path

SOURCE_DIR = Path(__file__).parents[1] / "lambdas" / "raw-event-writer" / "src"
sys.path.insert(0, str(SOURCE_DIR))

from handler import decode_kinesis_record, object_key, validate_event  # noqa: E402


class RawEventWriterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw_event = {
            "event_id": "event-1",
            "event_type": "initial_drain",
            "event_timestamp": "2026-09-22T12:00:00+00:00",
            "run_id": "run-1",
            "session_id": "session-1",
            "device_id": "claria-sim-001",
            "patient_id": "patient-synthetic-001",
            "payload": {"drained_volume_ml": 420},
        }

    def test_decodes_kinesis_transport_data_to_plain_json(self) -> None:
        record = {
            "kinesis": {
                "data": base64.b64encode(json.dumps(self.raw_event).encode("utf-8")).decode("utf-8")
            }
        }

        self.assertEqual(decode_kinesis_record(record), self.raw_event)

    def test_uses_partitioned_immutable_object_key(self) -> None:
        self.assertEqual(
            object_key(self.raw_event),
            "raw/run_id=run-1/dt=2026-09-22/device_id=claria-sim-001/2026-09-22T12-00-00+00-00_event-1.json",
        )

    def test_rejects_missing_contract_fields(self) -> None:
        with self.assertRaises(ValueError):
            validate_event({"event_id": "event-1", "payload": {}})


if __name__ == "__main__":
    unittest.main()
