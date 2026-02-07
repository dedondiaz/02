from __future__ import annotations

import sys
from pathlib import Path

base_dir = Path(__file__).resolve().parent
sys.path.append(str(base_dir.parent))

from aicorp.audit import AuditLog, build_record
from aicorp.policy import load_policy
from aicorp.scorer import NEVComponents, calculate_nev


def run_demo() -> None:
    constitution_path = base_dir / "constitution.yaml"
    audit_path = base_dir / "audit_log.jsonl"

    policy = load_policy(constitution_path)
    audit_log = AuditLog(audit_path)

    accepted_action = {
        "actor_type": "ai",
        "action_type": "optimize_supply",
        "domain": "operations",
        "cost": 100.0,
        "revenue": 300.0,
        "legal_risk": 5.0,
        "harm_risk": 2.0,
        "reputation_decay": 3.0,
        "uncertainty_penalty": 4.0,
    }

    rejected_action = {
        "actor_type": "human",
        "action_type": "override_policy",
        "domain": "human_override",
        "cost": 50.0,
        "revenue": 10.0,
        "legal_risk": 1.0,
        "harm_risk": 1.0,
        "reputation_decay": 1.0,
        "uncertainty_penalty": 1.0,
    }

    for label, action in [("ACCEPTED", accepted_action), ("REJECTED", rejected_action)]:
        decision = policy.evaluate(action)
        components = NEVComponents.from_action(action)
        nev = calculate_nev(components)
        record = build_record(action, decision.allowed, decision.reasons, nev)
        audit_log.append(record)
        print(f"{label} action -> allowed={decision.allowed}, reasons={decision.reasons}, nev={nev:.2f}")


if __name__ == "__main__":
    run_demo()
