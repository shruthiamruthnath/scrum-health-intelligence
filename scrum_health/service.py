from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone

from .briefing import generate_brief
from .dependencies import ranked_dependencies
from .findings import build_findings
from .fixtures import sample_dataset
from .scoring import health_index, score_health


def snapshot() -> dict:
    items, dependencies, goal = sample_dataset()
    dimensions = score_health(items, dependencies, goal)
    index = health_index(dimensions)
    findings = build_findings(dimensions, dependencies, goal)
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "goal": asdict(goal), "healthIndex": index,
        "confidenceLabel": "High" if index >= 80 else "Medium" if index >= 60 else "Low",
        "dimensions": [asdict(d) for d in dimensions],
        "risks": [asdict(f) for f in findings],
        "dependencies": ranked_dependencies(dependencies),
        "brief": generate_brief(goal.release, index, findings),
        "meta": {"source": "sample", "workItems": len(items), "evidenceCoverage": 1.0},
    }

