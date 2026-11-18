import json
import logging

from src.detect_threats import detect_threat
from src.finding_persistence import persist_finding
from src.validate_events import validate_event


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    if not validate_event(event):
        logger.warning(json.dumps({
            "action": "EVENT_REJECTED",
            "reason": "INVALID_EVENT",
            "simulation": True
        }))

        return {
            "statusCode": 400,
            "body": {
                "message": "Invalid security event",
                "simulation": True
            }
        }

    finding = detect_threat(event)

    if finding:
        logger.warning(json.dumps({
            "action": "SECURITY_FINDING",
            "event_id": event["event_id"],
            "finding": finding["finding"],
            "severity": finding["severity"],
            "simulation": event["simulation"]
        }))

        try:
            evidence = persist_finding(event, finding)

        except Exception:
            logger.exception(json.dumps({
                "action": "EVIDENCE_PERSISTENCE_FAILED",
                "event_id": event["event_id"],
                "simulation": True
            }))
            raise

        logger.info(json.dumps({
            "action": "EVIDENCE_PERSISTED",
            "event_id": event["event_id"],
            "evidence_key": evidence["key"],
            "sha256": evidence["sha256"],
            "simulation": True
        }))

        return {
            "statusCode": 200,
            "body": {
                "message": "Security finding generated and persisted",
                "finding": finding,
                "evidence": evidence
            }
        }

    logger.info(json.dumps({
        "action": "NO_FINDING",
        "event_id": event["event_id"],
        "simulation": event["simulation"]
    }))

    return {
        "statusCode": 200,
        "body": {
            "message": "No high-risk activity detected",
            "simulation": event["simulation"]
        }
    }
