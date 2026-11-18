import hashlib
import json
import os
from datetime import datetime, timezone

import boto3


def build_finding_record(event, finding):
    if event.get("simulation") is not True:
        raise ValueError("Only simulated events may be persisted")

    severity = finding["severity"]

    response = {
        "mode": "SIMULATION_ONLY",
        "action": (
            "SIMULATED_ESCALATION"
            if severity in ("HIGH", "CRITICAL")
            else "SIMULATED_MONITORING"
        ),
        "executed": False
    }

    return {
        "schema_version": "1.0",
        "record_type": "SECURITY_FINDING",
        "event_id": event["event_id"],
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "source_event": event,
        "finding": finding,
        "incident_response": response,
        "simulation": True
    }


def persist_finding(event, finding, s3_client=None):
    bucket = os.environ.get("SENTINEL_EVIDENCE_BUCKET")

    if not bucket:
        raise RuntimeError("SENTINEL_EVIDENCE_BUCKET is not configured")

    record = build_finding_record(event, finding)

    payload = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")

    digest = hashlib.sha256(payload).hexdigest()

    key = f"findings/{event['event_id']}/{digest}.json"

    client = s3_client if s3_client is not None else boto3.client("s3")

    client.put_object(
        Bucket=bucket,
        Key=key,
        Body=payload,
        ContentType="application/json",
        Metadata={
            "sha256": digest,
            "simulation": "true"
        }
    )

    return {
        "bucket": bucket,
        "key": key,
        "sha256": digest,
        "simulation": True
    }
