from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


class ConstitutionError(ValueError):
    pass


LIST_KEYS = {
    "prohibited_domains",
    "allowed_actor_types",
    "human_allowed_actions",
    "hard_constraints",
}


def _parse_value(raw: str) -> Any:
    value = raw.strip()
    if value.startswith("\"") and value.endswith("\""):
        return value[1:-1]
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _minimal_yaml_load(text: str) -> Dict[str, Any]:
    root: Dict[str, Any] = {}
    stack: List[tuple[int, Any]] = [(0, root)]

    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        content = line.strip()

        while stack and indent < stack[-1][0]:
            stack.pop()
        current = stack[-1][1]

        if content.startswith("- "):
            item = content[2:]
            if isinstance(current, list):
                current.append(_parse_value(item))
            else:
                raise ConstitutionError("List item found outside list context.")
            continue

        if ":" not in content:
            raise ConstitutionError(f"Unsupported line: {content}")

        key, raw_value = content.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if raw_value == "":
            container: Any = [] if key in LIST_KEYS else {}
            if isinstance(current, dict):
                current[key] = container
            else:
                raise ConstitutionError("Nested mapping found in non-dict context.")
            stack.append((indent + 2, container))
        else:
            value = _parse_value(raw_value)
            if isinstance(current, dict):
                current[key] = value
            else:
                raise ConstitutionError("Key-value found in non-dict context.")

    return root


@dataclass(frozen=True)
class Constitution:
    objective: Dict[str, Any]
    constraints: Dict[str, Any]
    prohibited_domains: List[str]
    permissions: Dict[str, Any]
    budgets: Dict[str, float]
    rate_limits: Dict[str, int]
    risk_caps: Dict[str, float]
    circuit_breakers: Dict[str, int]
    amendments: Dict[str, Any]
    transparency: Dict[str, Any]


REQUIRED_KEYS = {
    "objective",
    "constraints",
    "prohibited_domains",
    "permissions",
    "budgets",
    "rate_limits",
    "risk_caps",
    "circuit_breakers",
    "amendments",
    "transparency",
}


def load_constitution(path: Path) -> Constitution:
    text = path.read_text(encoding="utf-8")
    data = _minimal_yaml_load(text)
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise ConstitutionError(f"Missing required keys: {sorted(missing)}")

    return Constitution(
        objective=data["objective"],
        constraints=data["constraints"],
        prohibited_domains=data["prohibited_domains"],
        permissions=data["permissions"],
        budgets=data["budgets"],
        rate_limits=data["rate_limits"],
        risk_caps=data["risk_caps"],
        circuit_breakers=data["circuit_breakers"],
        amendments=data["amendments"],
        transparency=data["transparency"],
    )
