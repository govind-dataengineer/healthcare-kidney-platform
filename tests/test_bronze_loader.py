from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

SOURCE_DIR = Path(__file__).parents[1] / "warehouse" / "loader"
sys.path.insert(0, str(SOURCE_DIR))

import duckdb  # noqa: E402

from loader import initialise_database, load_object, write_status  # noqa: E402


class BronzeLoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = duckdb.connect(":memory:")
        initialise_database(self.connection)
        self.client = Mock()
        self.object_metadata = {"Key": "raw/run_id=run-1/event-1.json", "ETag": "etag-1"}
        raw_event = {"event_id": "event-1", "event_type": "initial_drain", "event_timestamp": "2026-09-22T12:00:00+00:00", "schema_version": "1.0", "run_id": "run-1", "session_id": "session-1", "device_id": "claria-sim-001", "patient_id": "patient-synthetic-001", "payload": {"drained_volume_ml": 420}}
        body = Mock()
        body.read.return_value = json.dumps(raw_event).encode("utf-8")
        self.client.get_object.return_value = {"Body": body}

    def test_loads_each_s3_object_only_once(self) -> None:
        self.assertTrue(load_object(self.connection, self.client, "raw-bucket", self.object_metadata))
        self.assertFalse(load_object(self.connection, self.client, "raw-bucket", self.object_metadata))
        self.assertEqual(self.connection.execute("SELECT count(*) FROM bronze.raw_therapy_event").fetchone()[0], 1)
        self.assertEqual(self.connection.execute("SELECT count(*) FROM bronze.ingest_log").fetchone()[0], 1)

    def test_writes_live_status_without_a_second_database_connection(self) -> None:
        self.connection.execute(
            "INSERT INTO bronze.ingest_log VALUES ('raw/event.json', 'etag', 1, current_timestamp)"
        )
        self.connection.execute(
            """INSERT INTO bronze.raw_therapy_event VALUES
            ('event-1', 'initial_drain', current_timestamp, '1.0', 'run-1', 'session-1',
             'device-1', 'patient-1', '{}', 'raw/event.json', current_timestamp)"""
        )
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            database_path = str(Path(directory) / "analytics.duckdb")
            write_status(self.connection, database_path)
            status = json.loads(Path(f"{database_path}.status.json").read_text())

        self.assertEqual(status["bronze_events"], 1)
        self.assertEqual(status["raw_s3_objects_ingested"], 1)


if __name__ == "__main__":
    unittest.main()
