from __future__ import annotations

import sys
import unittest
from pathlib import Path

SOURCE_DIR = Path(__file__).parents[1] / "services" / "device-simulator" / "src"
sys.path.insert(0, str(SOURCE_DIR))

from simulator import TherapyContext, build_session_events  # noqa: E402


class DeviceSimulatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.context = TherapyContext(
            run_id="run-1",
            session_id="session-1",
            device_id="claria-sim-001",
            patient_id="patient-synthetic-001",
        )

    def test_builds_ordered_lifecycle_with_initial_drain_and_last_fill(self) -> None:
        events = build_session_events(self.context, cycle_count=2)

        self.assertEqual(
            [record["event_type"] for record in events],
            [
                "therapy_started",
                "initial_drain",
                "cycle_fill",
                "cycle_dwell_completed",
                "cycle_drain",
                "cycle_fill",
                "cycle_dwell_completed",
                "cycle_drain",
                "last_fill",
                "therapy_completed",
            ],
        )
        self.assertTrue(all(record["device_id"] == "claria-sim-001" for record in events))
        self.assertEqual(events[-1]["payload"]["cycle_count_completed"], 2)

    def test_requires_at_least_one_cycle(self) -> None:
        with self.assertRaises(ValueError):
            build_session_events(self.context, cycle_count=0)


if __name__ == "__main__":
    unittest.main()
