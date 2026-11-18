
import unittest
from datetime import datetime, timedelta, timezone

from src.correlate_events import correlate_events


class TestEventCorrelation(unittest.TestCase):

    def setUp(self):
        self.base_time = datetime(
            2026, 11, 17, 12, 0, tzinfo=timezone.utc
        )

    def make_event(
        self, event_id, event_type,
        minutes=0, location="FACILITY_A",
        severity="HIGH"
    ):
        return {
            "event_id": event_id,
            "event_type": event_type,
            "severity": severity,
            "location": location,
            "timestamp": (
                self.base_time + timedelta(minutes=minutes)
            ).isoformat(),
            "simulation": True,
        }

    def test_matching_events(self):
        rf = self.make_event("rf-001", "RF_ANOMALY")
        network = self.make_event(
            "net-001",
            "SUSPICIOUS_NETWORK_CONNECTION",
            minutes=3
        )

        findings = correlate_events([rf, network])

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity"], "CRITICAL")

    def test_outside_time_window(self):
        rf = self.make_event("rf-002", "RF_ANOMALY")
        network = self.make_event(
            "net-002",
            "SUSPICIOUS_NETWORK_CONNECTION",
            minutes=10
        )

        findings = correlate_events([rf, network])

        self.assertEqual(len(findings), 0)

    def test_different_locations(self):
        rf = self.make_event(
            "rf-003", "RF_ANOMALY",
            location="FACILITY_A"
        )
        network = self.make_event(
            "net-003",
            "SUSPICIOUS_NETWORK_CONNECTION",
            location="FACILITY_B"
        )

        findings = correlate_events([rf, network])

        self.assertEqual(len(findings), 0)

    def test_low_severity_event(self):
        rf = self.make_event(
            "rf-004", "RF_ANOMALY",
            severity="LOW"
        )
        network = self.make_event(
            "net-004",
            "SUSPICIOUS_NETWORK_CONNECTION"
        )

        findings = correlate_events([rf, network])

        self.assertEqual(len(findings), 0)

    def test_exact_window_boundary(self):
        rf = self.make_event("rf-005", "RF_ANOMALY")
        network = self.make_event(
            "net-005",
            "SUSPICIOUS_NETWORK_CONNECTION",
            minutes=5
        )

        findings = correlate_events([rf, network])

        self.assertEqual(len(findings), 1)

    def test_missing_timestamp(self):
        rf = self.make_event("rf-006", "RF_ANOMALY")
        network = self.make_event(
            "net-006",
            "SUSPICIOUS_NETWORK_CONNECTION"
        )

        del network["timestamp"]

        findings = correlate_events([rf, network])

        self.assertEqual(len(findings), 0)

    def test_invalid_timestamp(self):
        rf = self.make_event("rf-007", "RF_ANOMALY")
        network = self.make_event(
            "net-007",
            "SUSPICIOUS_NETWORK_CONNECTION"
        )

        network["timestamp"] = "invalid-date"

        findings = correlate_events([rf, network])

        self.assertEqual(len(findings), 0)

    def test_non_dictionary_event(self):
        rf = self.make_event("rf-008", "RF_ANOMALY")
        network = self.make_event(
            "net-008",
            "SUSPICIOUS_NETWORK_CONNECTION"
        )

        findings = correlate_events([
            rf,
            "malformed-event",
            network
        ])

        self.assertEqual(len(findings), 1)


if __name__ == "__main__":
    unittest.main()
