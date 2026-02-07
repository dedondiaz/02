# Objective (NEV)

## Definition
NEV = Revenue – Costs – LegalRisk – HarmRisk – ReputationDecay – UncertaintyPenalty

## Term Definitions and Estimation
- **Revenue**: Expected gross revenue from the action (currency units). Estimated from contracts, pricing models, or simulated demand.
- **Costs**: Direct operational cost of the action, including compute, data, and external services (currency units).
- **LegalRisk**: Expected legal exposure cost (currency units). Estimated as probability of violation × penalty magnitude.
- **HarmRisk**: Expected harm cost (currency units). Estimated using impact severity × likelihood across affected parties.
- **ReputationDecay**: Expected reputational loss (currency units). Estimated from projected churn, brand impact, and partner risk.
- **UncertaintyPenalty**: Expected downside from model uncertainty (currency units). Estimated using variance-based penalty or conservative bounds.

## Anti-Gaming Rules
- All inputs must be non-negative.
- Revenue estimates must be auditable and derived from a documented model.
- Risk terms may not be set to zero without evidence.
- If uncertainty exceeds the configured cap, the action is invalid regardless of NEV.

## Worked Example
Given:
- Revenue = 120.0
- Costs = 30.0
- LegalRisk = 10.0
- HarmRisk = 5.0
- ReputationDecay = 8.0
- UncertaintyPenalty = 7.0

NEV = 120.0 - 30.0 - 10.0 - 5.0 - 8.0 - 7.0 = 60.0
