# Getting Started and Next Steps

This guide begins after the sample dashboard is running at [http://127.0.0.1:8080](http://127.0.0.1:8080).

## 1. Validate the sample experience

Explore each part of the dashboard before connecting live systems:

- **Health dimensions:** understand how goal confidence, flow, dependency exposure, and quality readiness contribute to the overall assessment.
- **Material-risk queue:** verify that every surfaced risk identifies an affected outcome, supporting evidence, confidence, and suggested action.
- **Dependency exposure:** review negative slack, missing ownership, unconfirmed relationships, and mitigation coverage.
- **Executive brief:** assess whether the narrative explains what changed, why it matters, and which decision is required.
- **Evidence:** confirm that statements can be traced to their underlying Jira or Confluence-style sources.

The objective is to evaluate whether the product supports better decisions—not simply whether it displays more metrics.

## 2. Run the automated tests

From the repository directory, run:

```powershell
python -m unittest discover -s tests -v
```

On Windows, if `python` is unavailable but the Python launcher is installed:

```powershell
py -m unittest discover -s tests -v
```

The tests cover the health model, dependency-exposure ordering, API contract, service health endpoint, and dashboard delivery.

## 3. Review the product white paper

Open either version under `docs/`:

- `Scrum_Health_Intelligence_White_Paper.pdf`
- `Scrum_Health_Intelligence_White_Paper.docx`

The paper explains the product opportunity, health model, AI architecture, trust controls, analytics, market positioning, and MVP roadmap.

## 4. Move from sample data to a live pilot

The current implementation uses synthetic Jira/Confluence-style data. Use a Jira sandbox or test project containing non-sensitive information for the first integration. Do not begin with production data.

### Recommended implementation sequence

1. Create or configure an Atlassian developer application.
2. Use OAuth and least-privilege scopes; do not store usernames or passwords in source code.
3. Retrieve one Jira project's sprints, issues, links, blockers, and changelog data.
4. Normalize the Jira payload into the domain models in `scrum_health/models.py`.
5. Preserve source identifiers and evidence links for every calculated signal.
6. Add only approved Confluence spaces and pages after the Jira-only workflow is reliable.
7. Retrieve the minimum relevant Confluence context and preserve source permissions.
8. Store local configuration in environment variables excluded by `.gitignore`.
9. Add refresh status, ingestion-health monitoring, and permission controls.
10. Validate alerts against historical sprint outcomes and user feedback.
11. Introduce retrieval-grounded AI summaries only after the evidence pipeline is dependable.
12. Require human confirmation for inferred dependencies and material actions.

## 5. Recommended first milestone

Connect **one Jira sandbox project** and generate a real sprint-health assessment while keeping Confluence retrieval and model-generated summaries optional.

A successful milestone should:

- ingest at least one completed sprint and one active sprint;
- map goal-critical work, status history, blockers, issue links, and ownership;
- calculate transparent health dimensions from real work data;
- produce a risk finding with source evidence and confidence;
- generate a deterministic leadership brief;
- complete a refresh without exposing credentials;
- pass the existing automated tests plus connector-specific tests.

This milestone validates the central product hypothesis with the least complexity: the system can detect an important delivery risk early enough for a team or leader to act.

## 6. Measure pilot value

Establish a baseline before using the dashboard. Track:

- material risks identified before the mitigation cutoff;
- time from risk detection to an owned action;
- dependency-driven misses;
- unplanned sprint carryover;
- executive reporting preparation time;
- alert precision and dismissal rate;
- evidence coverage;
- team trust and perceived usefulness.

Avoid using velocity or individual activity as performance measures.

## 7. Production-readiness gates

Before using production customer or employee data, complete:

- security and privacy review;
- OAuth and source-permission propagation;
- tenant isolation;
- encryption and retention controls;
- audit logging;
- rate-limit and retry handling;
- model and prompt version tracking;
- alert calibration;
- human override and correction workflows;
- incident-response and rollback procedures.

The reference implementation is a product-concept MVP, not a production Atlassian application.
