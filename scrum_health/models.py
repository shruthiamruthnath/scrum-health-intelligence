from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Literal

Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class WorkItem:
    key: str
    title: str
    status: str
    owner: str | None
    team: str
    goal_critical: bool = False
    blocked_hours: float = 0
    age_days: float = 0
    expected_cycle_days: float = 5
    changed_after_start: bool = False
    reopened: bool = False
    evidence_url: str | None = None


@dataclass(frozen=True)
class Dependency:
    source: str
    target: str
    owner: str | None
    required_by: date
    forecast_date: date
    impact: float = 0.5
    confirmed: bool = True
    mitigation_coverage: float = 0
    evidence: tuple[str, ...] = ()

    @property
    def slack_days(self) -> int:
        return (self.required_by - self.forecast_date).days


@dataclass(frozen=True)
class ProductGoal:
    key: str
    name: str
    release: str
    target_date: date
    work_item_keys: tuple[str, ...]


@dataclass
class Signal:
    name: str
    risk: float
    weight: float
    evidence: list[str] = field(default_factory=list)


@dataclass
class HealthDimension:
    name: str
    health: float
    confidence: float
    trend: Literal["up", "flat", "down"]
    signals: list[Signal]


@dataclass
class RiskFinding:
    id: str
    title: str
    severity: Severity
    exposure: float
    confidence: float
    affected_outcome: str
    evidence: list[str]
    suggested_action: str
    owner: str | None = None

