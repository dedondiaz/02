# Phase 0 Gates

Proceed only if all checks pass:

1. **Machine-Readable Constitution**
   - constitution.yaml exists and validates against required schema.
2. **Policy Enforcement**
   - policy engine denies prohibited domains/actions.
   - policy engine denies actions exceeding budget or risk caps.
3. **Objective Scoring**
   - NEV scoring computes deterministically from inputs.
4. **Audit Logging**
   - Every decision is appended to an immutable JSONL log.
5. **Human Non-Intervention**
   - Human actors can only submit agents or observe logs.
   - Any other human action is denied.
6. **Demo Execution**
   - demo.py runs end-to-end and shows at least one accepted and one rejected action.
