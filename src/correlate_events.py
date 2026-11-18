
import json
from src.validate_events import validate_event
from datetime import datetime, timedelta, timezone
from pathlib import Path


def parse_timestamp(value):

    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    ).astimezone(timezone.utc)


def correlate_events(events, window_minutes=5):

    if not isinstance(events, list):
        return []

    valid_events = [
        event for event in events
        if validate_event(event)
    ]

    events = valid_events

    rf_events = [
        event for event in events
        if event.get("event_type") == "RF_ANOMALY"
        and event.get("severity") == "HIGH"
    ]

    network_events = [
        event for event in events
        if event.get("event_type")
        == "SUSPICIOUS_NETWORK_CONNECTION"
        and event.get("severity") == "HIGH"
    ]

    findings = []

    for rf_event in rf_events:
        for network_event in network_events:
            if rf_event.get("location") != network_event.get("location"):
                continue

            rf_time = parse_timestamp(rf_event["timestamp"])
            network_time = parse_timestamp(
                network_event["timestamp"]
            )

            if abs(rf_time - network_time) <= timedelta(
                minutes=window_minutes
            ):
                findings.append({
                    "finding": "CORRELATED_RF_NETWORK_ACTIVITY",
                    "severity": "CRITICAL",
                    "location": rf_event["location"],
                    "related_event_ids": [
                        rf_event["event_id"],
                        network_event["event_id"]
                    ],
                    "simulation": True
                })

    return findings


def main():
    evidence_path = Path(
        "evidence/milestone-02/synthetic-rf-event.json"
    )

    with evidence_path.open("r", encoding="utf-8") as file:
        rf_event = json.load(file)

    network_event = {
        "event_id": "simulated-network-001",
        "timestamp": rf_event["timestamp"],
        "source": "sentinel-ci-network-simulator",
        "sensor_id": "CYBER-SIM-001",
        "event_type": "SUSPICIOUS_NETWORK_CONNECTION",
        "severity": "HIGH",
        "location": rf_event["location"],
        "simulation": True
    }

    findings = correlate_events([rf_event, network_event])

    print(json.dumps(findings, indent=2))


if __name__ == "__main__":
    main()
