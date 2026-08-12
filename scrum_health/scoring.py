from __future__ import annotations

from collections import defaultdict

from .models import Dependency, HealthDimension, ProductGoal, Signal, WorkItem


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def dimension(name: str, signals: list[Signal], coverage: float = 1.0) -> HealthDimension:
    total_weight = sum(s.weight for s in signals) or 1
    risk = sum(s.risk * s.weight for s in signals) / total_weight
    health = round(100 - clamp(risk), 1)
    confidence = round(clamp(55 + 40 * coverage - 8 * sum(not s.evidence for s in signals)) / 100, 2)
    trend = "down" if health < 65 else "up" if health > 82 else "flat"
    return HealthDimension(name, health, confidence, trend, signals)


def score_health(items: list[WorkItem], dependencies: list[Dependency], goal: ProductGoal) -> list[HealthDimension]:
    critical = [i for i in items if i.key in goal.work_item_keys]
    completed = sum(i.status.lower() == "done" for i in critical)
    blocked = sum(i.blocked_hours for i in critical)
    goal_signals = [
        Signal("goal-critical completion", 100 * (1 - completed / max(1, len(critical))), .35, [f"{completed}/{len(critical)} goal-critical items done"]),
        Signal("goal-critical blocking", clamp(blocked / 72 * 100), .4, [f"{blocked:.0f} blocked hours"] if blocked else []),
        Signal("goal scope volatility", clamp(sum(i.changed_after_start for i in critical) / max(1, len(critical)) * 100), .25, [i.key for i in critical if i.changed_after_start]),
    ]
    aged = [i for i in items if i.age_days > i.expected_cycle_days]
    flow_signals = [
        Signal("cycle-time deviation", clamp(sum(max(0, i.age_days / max(1, i.expected_cycle_days) - 1) for i in items) / max(1, len(items)) * 80), .5, [i.key for i in aged]),
        Signal("blocked duration", clamp(sum(i.blocked_hours for i in items) / 72 * 100), .3, [i.key for i in items if i.blocked_hours]),
        Signal("scope change", clamp(sum(i.changed_after_start for i in items) / max(1, len(items)) * 100), .2, [i.key for i in items if i.changed_after_start]),
    ]
    exposed = [d for d in dependencies if d.slack_days < 0]
    dependency_signals = [
        Signal("negative slack", clamp(sum(abs(d.slack_days) for d in exposed) * 18), .5, [f"{d.source} → {d.target}: {d.slack_days}d" for d in exposed]),
        Signal("unconfirmed dependencies", clamp(sum(not d.confirmed for d in dependencies) / max(1, len(dependencies)) * 100), .3, [f"{d.source} → {d.target}" for d in dependencies if not d.confirmed]),
        Signal("missing ownership", clamp(sum(not d.owner for d in dependencies) / max(1, len(dependencies)) * 100), .2, [f"{d.source} → {d.target}" for d in dependencies if not d.owner]),
    ]
    quality_signals = [
        Signal("reopened work", clamp(sum(i.reopened for i in items) / max(1, len(items)) * 120), .55, [i.key for i in items if i.reopened]),
        Signal("unfinished critical work", clamp((len(critical) - completed) / max(1, len(critical)) * 85), .45, [i.key for i in critical if i.status.lower() != "done"]),
    ]
    coverage = sum(bool(i.evidence_url) for i in items) / max(1, len(items))
    return [
        dimension("Goal confidence", goal_signals, coverage),
        dimension("Flow health", flow_signals, coverage),
        dimension("Dependency exposure", dependency_signals, coverage),
        dimension("Quality readiness", quality_signals, coverage),
    ]


def health_index(dimensions: list[HealthDimension]) -> float:
    weights = {"Goal confidence": .35, "Flow health": .2, "Dependency exposure": .3, "Quality readiness": .15}
    return round(sum(d.health * weights.get(d.name, 0) for d in dimensions), 1)

