from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class NEVComponents:
    revenue: float
    costs: float
    legal_risk: float
    harm_risk: float
    reputation_decay: float
    uncertainty_penalty: float

    @classmethod
    def from_action(cls, action: Dict[str, float]) -> "NEVComponents":
        return cls(
            revenue=float(action.get("revenue", 0.0)),
            costs=float(action.get("cost", 0.0)),
            legal_risk=float(action.get("legal_risk", 0.0)),
            harm_risk=float(action.get("harm_risk", 0.0)),
            reputation_decay=float(action.get("reputation_decay", 0.0)),
            uncertainty_penalty=float(action.get("uncertainty_penalty", 0.0)),
        )


def calculate_nev(components: NEVComponents) -> float:
    values = [
        components.revenue,
        components.costs,
        components.legal_risk,
        components.harm_risk,
        components.reputation_decay,
        components.uncertainty_penalty,
    ]
    if any(value < 0 for value in values):
        raise ValueError("NEV components must be non-negative.")
    return (
        components.revenue
        - components.costs
        - components.legal_risk
        - components.harm_risk
        - components.reputation_decay
        - components.uncertainty_penalty
    )
