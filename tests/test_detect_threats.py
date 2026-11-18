
import unittest
from datetime import datetime, timezone

from src.detect_threats import detect_threat


class TestThreatDetection(unittest.TestCase):

    def make_event(self, event_id, event_type, severity):
        return {
            "event_id": event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "severity": severity,
            "location": "SIMULATED_SECURE_FACILITY",
            "simulation": True,
        }

    def test_high_severity_rf_anomaly(self):
        event = self.make_event(
            "test-001", "RF_ANOMALY", "HIGH"
        )
        finding = detect_threat(event)

        self.assertIsNotNone(finding)
        self.assertEqual(
            finding["finding"],
            "HIGH_RISK_ACTIVITY_DETECTED"
        )

    def test_low_severity_rf_anomaly(self):
        event = self.make_event(
            "test-002", "RF_ANOMALY", "LOW"
        )
        self.assertIsNone(detect_threat(event))

    def test_high_severity_unknown_event(self):
        event = self.make_event(
            "test-003", "NORMAL_ACTIVITY", "HIGH"
        )
        self.assertIsNone(detect_threat(event))

    def test_high_severity_network_connection(self):
        event = self.make_event(
            "test-004",
            "SUSPICIOUS_NETWORK_CONNECTION",
            "HIGH"
        )
        finding = detect_threat(event)

        self.assertIsNotNone(finding)
        self.assertEqual(
            finding["source_event_type"],
            "SUSPICIOUS_NETWORK_CONNECTION"
        )

    def test_missing_timestamp_rejected(self):
        event = self.make_event(
            "test-005", "RF_ANOMALY", "HIGH"
        )
        del event["timestamp"]

        self.assertIsNone(detect_threat(event))

    def test_invalid_timestamp_rejected(self):
        event = self.make_event(
            "test-006", "RF_ANOMALY", "HIGH"
        )
        event["timestamp"] = "not-a-date"

        self.assertIsNone(detect_threat(event))


if __name__ == "__main__":
    unittest.main()
