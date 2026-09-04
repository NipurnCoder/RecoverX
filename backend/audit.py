import json
from datetime import datetime
from pathlib import Path


AUDIT_FILE = Path("data/audit_log.jsonl")


def log_event(event_type, transaction_id, data):

    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "transaction_id": transaction_id,
        "data": data
    }

    AUDIT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        AUDIT_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(event) + "\n"
        )