# Dependency-First Execution

The controller tracks execution. `shipwright-decomposer` creates or refreshes the material plan.

## Decomposer route

```text
Profile: shipwright-decomposer
Model: gpt-5.6-sol
Reasoning: high
Mode: read-only
```

## Dependency model first

Before lanes, map hard dependencies, ordering/predecessors, data/state dependencies, API/event/shared contracts, migration/schema ordering, reverse consumers, shared-write risks, verification hotspots and independent subgraphs. Use Graphify when available/current enough, then confirm bounded facts as necessary. Different files do not automatically mean independent work.

## Lane objective

Create the smallest coherent independently implementable/verifiable lanes. Optimize for Requirement Authority/architecture correctness, hard dependency order, safe parallelism, minimal shared-write contention, minimal context per writer, lowest-cost capable GPT-5.6 route, and behavioral/verification cohesion.

## Exact writer routes

```text
SIMPLE -> shipwright-builder-simple / gpt-5.6-luna / medium
MEDIUM -> shipwright-builder        / gpt-5.6-luna / max
HARD   -> shipwright-builder-hard   / gpt-5.6-terra / high
```

SIMPLE means local/deterministic behavior with strong precedent and focused verification. MEDIUM means coordinated/moderate state/dependency complexity with clear authority. HARD is irreducible after decomposition: difficult concurrency/recovery, persistence/migration, fragile cross-layer integration, non-trivial state machines, rollback/recovery, or sustained reasoning across coupled components.

Do not classify by file count or use Sol as a coding worker merely because total scope is large.

## Diagnosis routes

For `CHANGE_WITH_DIAGNOSIS`:

```text
ordinary -> shipwright-investigator      / gpt-5.6-luna / max
hard     -> shipwright-investigator-hard / gpt-5.6-terra / high
```

Investigators are read-only and establish cause/evidence before correction planning.

## Plan

`plan.md` must include dependency model, parallel waves, and for each lane: objective, dependencies, owned scope, shared/prohibited hotspots, verification boundary, complexity/reason, exact profile/model/reasoning, and status.

Every material lane needs bounded ownership, exact route and verification boundary before dispatch.

## Writer packet

Give each writer only lane objective, applicable requirements/architecture, bounded code/test/config scope, dependency assumptions, prohibited/shared hotspots and verification expectations. Do not pass unrelated project context or reasoning narratives.

## Parallel execution and integration

Fan out only dependency-independent and write-safe lanes. Use run-owned temporary worktrees/workspaces where useful. Record each requested/actual route and completion in state.

Integrate only into the exact candidate tracked by run state. Product/architecture ambiguity returns to the applicable reasoning stage. Material dependency/ownership change marks plan `STALE` and re-runs decomposition.

Review findings do not choose correction routing. Reuse a writer lane only when objective, dependencies/order, hotspots, verification boundary, authority, architecture and complexity remain unchanged; otherwise re-plan affected scope.
