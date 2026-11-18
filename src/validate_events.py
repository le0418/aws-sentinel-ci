
from datetime import datetime


REQUIRED_FIELDS = {
    "event_id",
    "timestamp",
    "event_type",
    "severity",
    "location",
    "simulation",
}

ALLOWED_SEVERITIES = {
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
}


def validate_event(event):
    if not isinstance(event, dict):
        return False

    if not REQUIRED_FIELDS.issubset(event.keys()):
        return False

    for field in (
        "event_id",
        "timestamp",
        "event_type",
        "severity",
        "location",
    ):
        if not isinstance(event[field], str):
            return False

        if not event[field].strip():
            return False

    if event["severity"] not in ALLOWED_SEVERITIES:
        return False

    if not isinstance(event["simulation"], bool):
        return False

    try:
        timestamp = datetime.fromisoformat(
            event["timestamp"].replace("Z", "+00:00")
        )

        if timestamp.tzinfo is None:
            return False

    except (ValueError, TypeError, OverflowError):
        return False

    return True
