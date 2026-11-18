import unittest
from unittest.mock import patch

from src.lambda_handler import lambda_handler


class LambdaHandlerTests(unittest.TestCase):
    def setUp(self):
        self.event = {
            "event_id": "lambda-test-001",
            "timestamp": "2026-11-17T12:00:00Z",
            "event_type": "RF_ANOMALY",
            "severity": "HIGH",
            "location": "SIMULATED_SECURE_FACILITY",
            "simulation": True,
        }

    @patch("src.lambda_handler.persist_finding")
    def test_high_risk_finding_persisted(self, mock_persist):
        mock_persist.return_value = {
            "bucket": "test-evidence-bucket",
            "key": "findings/lambda-test-001/test.json",
            "sha256": "test-sha256",
            "simulation": True,
        }

        result = lambda_handler(self.event, None)

        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(
            result["body"]["message"],
            "Security finding generated and persisted",
        )
        self.assertEqual(
            result["body"]["evidence"]["key"],
            "findings/lambda-test-001/test.json",
        )
        mock_persist.assert_called_once()

    @patch("src.lambda_handler.persist_finding")
    def test_s3_failure_raises_exception(self, mock_persist):
        mock_persist.side_effect = RuntimeError("Simulated S3 failure")

        with self.assertRaisesRegex(RuntimeError, "Simulated S3 failure"):
            lambda_handler(self.event, None)

        mock_persist.assert_called_once()


    @patch("src.lambda_handler.persist_finding")
    def test_invalid_event_rejected(self, mock_persist):
        invalid_event = dict(self.event)
        invalid_event.pop("event_id")

        result = lambda_handler(invalid_event, None)

        self.assertEqual(result["statusCode"], 400)
        mock_persist.assert_not_called()

    @patch("src.lambda_handler.persist_finding")
    def test_low_severity_event_not_persisted(self, mock_persist):
        low_event = dict(self.event)
        low_event["severity"] = "LOW"

        result = lambda_handler(low_event, None)

        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(
            result["body"]["message"],
            "No high-risk activity detected",
        )
        mock_persist.assert_not_called()


if __name__ == "__main__":
    unittest.main()
