from __future__ import annotations

from collections import defaultdict, deque

from .models import Dependency


def exposure(dep: Dependency, downstream_reach: int = 1) -> float:
    delay_probability = min(1.0, max(0.15, 0.5 + (-dep.slack_days * .12)))
    criticality = min(1.0, .55 + .1 * downstream_reach)
    return round(100 * delay_probability * dep.impact * criticality * (1 - dep.mitigation_coverage), 1)


def downstream_counts(dependencies: list[Dependency]) -> dict[str, int]:
    graph: dict[str, list[str]] = defaultdict(list)
    for d in dependencies: graph[d.source].append(d.target)
    result = {}
    for node in set(graph) | {d.target for d in dependencies}:
        seen, queue = set(), deque(graph[node])
        while queue:
            nxt = queue.popleft()
            if nxt in seen: continue
            seen.add(nxt); queue.extend(graph[nxt])
        result[node] = len(seen)
    return result


def ranked_dependencies(dependencies: list[Dependency]) -> list[dict]:
    reach = downstream_counts(dependencies)
    ranked = []
    for dep in dependencies:
        ranked.append({
            "source": dep.source, "target": dep.target, "owner": dep.owner or "Unassigned",
            "requiredBy": dep.required_by.isoformat(), "forecastDate": dep.forecast_date.isoformat(),
            "slackDays": dep.slack_days, "confirmed": dep.confirmed,
            "mitigationCoverage": dep.mitigation_coverage,
            "exposure": exposure(dep, reach.get(dep.source, 1)), "evidence": list(dep.evidence),
        })
    return sorted(ranked, key=lambda x: x["exposure"], reverse=True)

