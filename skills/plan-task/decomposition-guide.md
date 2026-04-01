# Decomposition Guide

Break the task into sub-tasks. For each:

| Field | Description |
|-------|------------|
| **Name** | Short description |
| **Dependencies** | Which sub-tasks must complete first |
| **Agent type** | Research, Implementation, or Review |
| **Parallelizable** | Can this run concurrently with other sub-tasks? |
| **Estimated complexity** | trivial / moderate / complex |
| **Confidence** | Numeric score 0.0-1.0 (see calibration anchors below) |
| **Test scenarios** | 1-3 verification checks per sub-task (see Test Scenarios below) |

Present as a table.

## Confidence Scoring

Score each sub-task on a 0.0-1.0 scale using these calibration anchors:

| Score | Meaning | Example |
|-------|---------|---------|
| **0.9+** | Well-understood, done before, clear spec | "Add a column to an existing table" |
| **0.7-0.9** | Understood but some unknowns | "Build a standard CRUD endpoint with an unfamiliar ORM" |
| **0.5-0.7** | Significant unknowns, research needed | "Integrate a third-party API with sparse docs" |
| **< 0.5** | Speculative, plan might be wrong | "Design a novel algorithm for an ill-defined problem" |

### Deepening Pass

After initial decomposition, review all sub-tasks with confidence below 0.7. For each:

1. **Can a targeted research agent raise confidence?** If yes, insert a research sub-task before the implementation sub-task. The research sub-task's deliverable is a concrete spec that raises the implementation sub-task's confidence above 0.7.
2. **Should the sub-task split into research + conditional implementation?** If the research might reveal the sub-task is unnecessary or needs a different approach, make the implementation sub-task conditional on the research output.

**Plan-level gate:** If the average confidence across all sub-tasks is below 0.7, the plan needs more research before proceeding to implementation. Do not start implementation agents against a low-confidence plan.

## Test Scenarios

Each sub-task must include 1-3 verification checks across these categories:

| Category | What to specify | Example |
|----------|----------------|---------|
| **Happy path** | Expected behavior with good input | "Given a valid user ID, returns the user's profile with all fields populated" |
| **Edge case** | Boundary conditions, empty data, unusual values | "Given an empty dataset, returns an empty result without errors" |
| **Error path** | What happens when things go wrong | "Given an invalid API key, returns a clear error message and does not retry" |

Not every sub-task needs all three categories — use judgment. But every sub-task needs at least one. These become the verification checklist for `/verify` after implementation.

## Decomposition Heuristics
- If a sub-task has no clear success criterion, it's underspecified — split it or add criteria
- If a sub-task crosses concern boundaries (e.g., "build the pipeline and analyze the results"), split it
- Sequential dependencies should be minimized — look for ways to parallelize
- Each sub-task should be completable by a single agent in a single session
