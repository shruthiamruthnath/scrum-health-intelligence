from __future__ import annotations

from .models import RiskFinding


def generate_brief(release: str, health_index: float, findings: list[RiskFinding]) -> dict:
    """Deterministic fallback. Replace through BriefGenerator for a grounded LLM."""
    confidence = round(sum(f.confidence for f in findings[:3]) / max(1, len(findings[:3])), 2)
    label = "HIGH" if health_index >= 80 else "MEDIUM" if health_index >= 60 else "LOW"
    primary = findings[0] if findings else None
    summary = f"{release} is {label} confidence with a health index of {health_index:.0f}."
    if primary:
        summary += f" The primary exposure is {primary.title.lower()} ({primary.exposure:.0f}/100 exposure)."
    return {
        "release": release, "confidenceLabel": label, "modelConfidence": confidence,
        "summary": summary,
        "decisions": [f.suggested_action for f in findings[:2]],
        "evidence": [e for f in findings[:3] for e in f.evidence][:6],
        "disclaimer": "Decision support only. Verify evidence and accountable owners before acting.",
    }

