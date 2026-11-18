
import json
from pathlib import Path

from src.validate_events import validate_event

HIGH_RISK_EVENTS = {
    "RF_ANOMALY",
    "UNAUTHORIZED_DEVICE",
    "SUSPICIOUS_NETWORK_CONNECTION",
}

def detect_threat(event):
    if not validate_event(event):
        return None

    event_type = event.get("event_type")
    severity = event.get("severity")

    if event_type in HIGH_RISK_EVENTS and severity == "HIGH":
        return {
            "event_id": event.get("event_id"),
            "finding": "HIGH_RISK_ACTIVITY_DETECTED",
            "severity": "HIGH",
            "source_event_type": event_type,
            "simulation": True,
        }

    return None


def main():
    evidence_path = Path(
        "evidence/milestone-02/synthetic-rf-event.json"
    )

    with evidence_path.open("r", encoding="utf-8") as file:
        event = json.load(file)

    finding = detect_threat(event)

    if finding:
        print("SECURITY FINDING GENERATED")
        print(json.dumps(finding, indent=2))
    else:
        print("No high-risk activity detected.")


if __name__ == "__main__":
    main()
