
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

event = {
    "event_id": str(uuid.uuid4()),
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "source": "sentinel-ci-simulator",
    "sensor_id": "TSCM-SIM-001",
    "event_type": "RF_ANOMALY",
    "severity": "HIGH",
    "frequency_mhz": 915.0,
    "signal_strength_dbm": -42,
    "location": "SIMULATED_SECURE_FACILITY",
    "description": "Synthetic unauthorized RF transmission detected",
    "simulation": True
}

output = Path(
    "evidence/milestone-02/synthetic-rf-event.json"
)

output.parent.mkdir(parents=True, exist_ok=True)

output.write_text(
    json.dumps(event, indent=2),
    encoding="utf-8"
)

print(f"Generated synthetic evidence: {output}")
print(json.dumps(event, indent=2))
