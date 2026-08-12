from __future__ import annotations

from .dependencies import ranked_dependencies
from .models import HealthDimension, ProductGoal, RiskFinding


def build_findings(dimensions: list[HealthDimension], dependencies, goal: ProductGoal) -> list[RiskFinding]:
    findings: list[RiskFinding] = []
    for dep in ranked_dependencies(dependencies):
        if dep["exposure"] < 18: continue
        findings.append(RiskFinding(
            f"dep-{dep['source']}-{dep['target']}",
            f"{dep['source']} may delay {dep['target']}",
            "high" if dep["exposure"] >= 45 else "medium",
            dep["exposure"], .88 if dep["confirmed"] else .66,
            f"{goal.name} / {goal.release}",
            dep["evidence"] + [f"Slack: {dep['slackDays']} days"],
            "Confirm owner and required-by date; evaluate decoupling or parallel validation.",
            dep["owner"],
        ))
    for d in dimensions:
        if d.health >= 60: continue
        evidence = [item for s in d.signals for item in s.evidence][:5]
        findings.append(RiskFinding(
            f"health-{d.name.lower().replace(' ', '-')}", f"{d.name} is below the action threshold",
            "high" if d.health < 45 else "medium", round(100-d.health, 1), d.confidence,
            f"{goal.name} / {goal.release}", evidence,
            "Review the top contributing signals and assign a time-bound mitigation.",
        ))
    return sorted(findings, key=lambda f: f.exposure, reverse=True)

