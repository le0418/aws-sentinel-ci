import hashlib
import json
import os
import unittest
from unittest.mock import patch

from src.finding_persistence import (
    build_finding_record,
    persist_finding,
)


class FakeS3Client:
    def __init__(self):
        self.calls = []

    def put_object(self, **kwargs):
        self.calls.append(kwargs)
        return {"ETag": '"simulated-etag"'}


class FindingPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.event = {
            "event_id": "test-rf-event-001",
            "timestamp": "2026-11-17T12:00:00Z",
            "event_type": "RF_ANOMALY",
            "severity": "HIGH",
            "location": "SIMULATED_SECURE_FACILITY",
            "simulation": True,
        }

        self.finding = {
            "finding": "HIGH_RISK_ACTIVITY_DETECTED",
            "severity": "HIGH",
        }

        self.fake_s3 = FakeS3Client()

    def test_record_contains_simulated_response(self):
        record = build_finding_record(self.event, self.finding)

        self.assertEqual(record["record_type"], "SECURITY_FINDING")
        self.assertEqual(record["event_id"], self.event["event_id"])
        self.assertEqual(
            record["incident_response"]["action"],
            "SIMULATED_ESCALATION",
        )
        self.assertFalse(record["incident_response"]["executed"])
        self.assertTrue(record["simulation"])

    def test_critical_finding_uses_simulated_escalation(self):
        finding = {
            "finding": "CORRELATED_RF_NETWORK_ACTIVITY",
            "severity": "CRITICAL",
        }

        record = build_finding_record(self.event, finding)

        self.assertEqual(
            record["incident_response"]["action"],
            "SIMULATED_ESCALATION",
        )

    def test_lower_severity_uses_simulated_monitoring(self):
        finding = {
            "finding": "LOW_RISK_ACTIVITY",
            "severity": "LOW",
        }

        record = build_finding_record(self.event, finding)

        self.assertEqual(
            record["incident_response"]["action"],
            "SIMULATED_MONITORING",
        )

    def test_non_simulated_event_is_rejected(self):
        event = dict(self.event)
        event["simulation"] = False

        with self.assertRaises(ValueError):
            build_finding_record(event, self.finding)

    @patch.dict(
        os.environ,
        {"SENTINEL_EVIDENCE_BUCKET": "test-evidence-bucket"},
    )
    def test_s3_upload_and_sha256_integrity(self):
        result = persist_finding(
            self.event,
            self.finding,
            s3_client=self.fake_s3,
        )

        self.assertEqual(len(self.fake_s3.calls), 1)

        upload = self.fake_s3.calls[0]
        payload = upload["Body"]
        calculated_digest = hashlib.sha256(payload).hexdigest()

        self.assertEqual(upload["Bucket"], "test-evidence-bucket")
        self.assertEqual(upload["ContentType"], "application/json")
        self.assertEqual(upload["Metadata"]["sha256"], calculated_digest)
        self.assertEqual(result["sha256"], calculated_digest)
        self.assertEqual(
            upload["Key"],
            f"findings/test-rf-event-001/{calculated_digest}.json",
        )

        saved_record = json.loads(payload.decode("utf-8"))

        self.assertEqual(
            saved_record["finding"]["finding"],
            "HIGH_RISK_ACTIVITY_DETECTED",
        )
        self.assertFalse(
            saved_record["incident_response"]["executed"],
        )

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_bucket_configuration_is_rejected(self):
        with self.assertRaises(RuntimeError):
            persist_finding(
                self.event,
                self.finding,
                s3_client=self.fake_s3,
            )

        self.assertEqual(len(self.fake_s3.calls), 0)


if __name__ == "__main__":
    unittest.main()
