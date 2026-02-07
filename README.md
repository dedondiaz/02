# AI Governance Core (Phase 0)

This repository contains the Phase 0 governance core for an autonomous AI-run company. It defines enforceable, machine-readable constraints, a policy engine to approve/deny actions, an objective scorer (NEV), and an append-only audit log.

## Contents
- `docs/AI_CONSTITUTION.md`: human-readable constitution summary.
- `docs/OBJECTIVE.md`: NEV objective definition and example.
- `docs/PHASE0_GATES.md`: explicit go/no-go checks for Phase 0.
- `aicorp/constitution.yaml`: authoritative machine-readable rules.
- `aicorp/constitution.py`: loader/validator for the constitution.
- `aicorp/policy.py`: policy engine enforcing constraints.
- `aicorp/scorer.py`: NEV scorer.
- `aicorp/audit.py`: append-only JSONL audit log.
- `aicorp/demo.py`: end-to-end demonstration.

## Quickstart
Run the demo to see one accepted and one rejected action, with audit logging:

```bash
python /workspace/02/aicorp/demo.py
```

The demo writes an append-only JSONL log to `aicorp/audit_log.jsonl`.

## Notes
- Humans may only submit AI agents or observe logs; any other action is denied by policy.
- This repository intentionally avoids UI or network integrations.
