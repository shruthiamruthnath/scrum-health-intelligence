from datetime import date

from .models import Dependency, ProductGoal, WorkItem


def sample_dataset():
    items = [
        WorkItem("ATL-142", "Stabilize Identity API contract", "Blocked", "Platform EM", "Platform", True, 61, 9, 5, evidence_url="https://jira.example/ATL-142"),
        WorkItem("ATL-151", "Delegated administration flow", "In Progress", "App Team", "Experience", True, 0, 8, 6, True, evidence_url="https://jira.example/ATL-151"),
        WorkItem("ATL-155", "Contract integration tests", "To Do", "QA Lead", "Quality", True, 0, 5, 4, evidence_url="https://jira.example/ATL-155"),
        WorkItem("ATL-160", "Admin analytics", "In Progress", "Data Team", "Data", False, 0, 3, 6, True, evidence_url="https://jira.example/ATL-160"),
        WorkItem("ATL-164", "Accessibility review", "Done", "Design Ops", "Experience", False, 0, 4, 5, evidence_url="https://jira.example/ATL-164"),
        WorkItem("ATL-167", "Release telemetry", "In Review", "SRE", "Platform", True, 0, 7, 5, reopened=True, evidence_url="https://jira.example/ATL-167"),
    ]
    dependencies = [
        Dependency("ATL-142", "ATL-155", "Platform EM", date(2026, 8, 18), date(2026, 8, 21), .95, True, .25, ("Jira link blocks", "Launch plan §4.2")),
        Dependency("ATL-155", "ATL-151", "QA Lead", date(2026, 8, 25), date(2026, 8, 26), .85, True, .15, ("Release plan",)),
        Dependency("ATL-142", "ATL-151", None, date(2026, 8, 20), date(2026, 8, 21), .75, False, 0, ("AI proposal: shared Identity API",)),
        Dependency("ATL-167", "ATL-151", "SRE", date(2026, 8, 27), date(2026, 8, 25), .55, True, .7, ("Readiness checklist",)),
    ]
    goal = ProductGoal("GOAL-ATLAS", "Enterprise administration ready for controlled launch", "Atlas 1.0", date(2026, 8, 28), tuple(i.key for i in items if i.goal_critical))
    return items, dependencies, goal

