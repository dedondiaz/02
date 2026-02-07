from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

from aicorp.constitution import Constitution, ConstitutionError, load_constitution


@dataclass
class PolicyDecision:
    allowed: bool
    reasons: List[str]


class PolicyEngine:
    def __init__(self, constitution_path: Path) -> None:
        self.constitution = load_constitution(constitution_path)
        self._violations: List[datetime] = []
        self._actions: List[datetime] = []
        self._daily_costs: Dict[str, float] = {}

    def evaluate(self, action: Dict[str, Any]) -> PolicyDecision:
        reasons: List[str] = []
        now = datetime.now(timezone.utc)
        self._prune_actions(now)
        self._prune_violations(now)

        actor_type = action.get("actor_type")
        action_type = action.get("action_type")
        domain = action.get("domain")
        cost = float(action.get("cost", 0.0))

        if actor_type not in self.constitution.permissions.get("allowed_actor_types", []):
            reasons.append("actor_type_not_allowed")

        if actor_type == "human" and action_type not in self.constitution.permissions.get(
            "human_allowed_actions", []
        ):
            reasons.append("human_action_not_permitted")

        if domain in self.constitution.prohibited_domains:
            reasons.append("prohibited_domain")

        if cost > float(self.constitution.budgets.get("per_action_cost_cap", 0.0)):
            reasons.append("per_action_cost_cap_exceeded")

        day_key = now.date().isoformat()
        total_cost = self._daily_costs.get(day_key, 0.0) + cost
        if total_cost > float(self.constitution.budgets.get("daily_cost_cap", 0.0)):
            reasons.append("daily_cost_cap_exceeded")

        if len(self._actions) >= int(self.constitution.rate_limits.get("max_actions_per_hour", 0)):
            reasons.append("rate_limit_exceeded")

        self._check_risk_caps(action, reasons)

        if reasons:
            self._violations.append(now)
        else:
            self._actions.append(now)
            self._daily_costs[day_key] = total_cost

        if len(self._violations) > int(
            self.constitution.circuit_breakers.get("max_violations_per_hour", 0)
        ):
            reasons.append("circuit_breaker_triggered")

        return PolicyDecision(allowed=len(reasons) == 0, reasons=reasons)

    def _check_risk_caps(self, action: Dict[str, Any], reasons: List[str]) -> None:
        for key, cap in self.constitution.risk_caps.items():
            value = float(action.get(key, 0.0))
            if value > float(cap):
                reasons.append(f"risk_cap_exceeded:{key}")

    def _prune_actions(self, now: datetime) -> None:
        cutoff = now - timedelta(hours=1)
        self._actions = [ts for ts in self._actions if ts > cutoff]

    def _prune_violations(self, now: datetime) -> None:
        cutoff = now - timedelta(hours=1)
        self._violations = [ts for ts in self._violations if ts > cutoff]


def load_policy(constitution_path: Path) -> PolicyEngine:
    if not constitution_path.exists():
        raise ConstitutionError(f"Missing constitution at {constitution_path}")
    return PolicyEngine(constitution_path)
