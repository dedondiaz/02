from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class AuditRecord:
    timestamp: str
    action: Dict[str, Any]
    allowed: bool
    reasons: List[str]
    nev: float


class AuditLog:
    def __init__(self, path: Path) -> None:
        self.path = path

    def append(self, record: AuditRecord) -> None:
        payload = json.dumps(asdict(record), sort_keys=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(payload + "\n")


def build_record(action: Dict[str, Any], allowed: bool, reasons: List[str], nev: float) -> AuditRecord:
    timestamp = datetime.now(timezone.utc).isoformat()
    return AuditRecord(timestamp=timestamp, action=action, allowed=allowed, reasons=reasons, nev=nev)
