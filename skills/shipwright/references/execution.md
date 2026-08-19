# Dependency-First Execution

The controller tracks execution. A fresh Decomposer context creates or refreshes the execution plan.

## Dependency model first

Before creating implementation lanes, map the relevant:

- hard dependencies;
- ordering/predecessors;
- data/state dependencies;
- API/event/shared-contract dependencies;
- migration/schema ordering;
- reverse dependencies/direct consumers;
- shared hotspots/shared-write risks;
- verification hotspots;
- independent subgraphs.

Different files do not automatically mean independent work.

## Lane objective

Create the smallest coherent lanes that are independently implementable and independently verifiable without breaking behavioral cohesion.

Optimize in this order:

1. preserve resolved requirements and architecture;
2. respect hard dependencies;
3. maximize safe parallelism;
4. minimize shared-write contention;
5. minimize context per writer;
6. use the least expensive capable coding agent;
7. keep work together when splitting would increase coordination, merge, or verification risk.

## Complexity

### SIMPLE

Local/deterministic behavior, strong precedent, limited state/dependency complexity, focused verification.

Use an efficient available coding agent.

### MEDIUM

Several coordinated changes, moderate state/dependency complexity, but architecture and behavior are clear.

Use a stronger available coding configuration when useful.

### HARD

Irreducible complexity remains after decomposition: difficult concurrency/recovery, complex persistence, fragile cross-layer integration, non-trivial state machines, migration/rollback, or sustained reasoning across coupled components.

Use the strongest appropriate coding/reasoning capability available.

Shipwright never requires a specific named model.

## Plan format

Write `plan.md`:

```text
# Execution Plan

## Dependency model
- ...

## Parallel waves
Wave 1: L1, L2
Wave 2: L3
...

## L1 — <name>
Objective: ...
Depends on: NONE | <lane IDs>
Owned scope: ...
Shared/prohibited hotspots: ...
Verification boundary: ...
Complexity: SIMPLE | MEDIUM | HARD
Reason: ...
Status: READY
```

Every material lane must have bounded ownership and a verification boundary before dispatch.

## Writer packet

Provide a writer only:

- lane objective;
- applicable requirements;
- applicable architecture decisions/contracts;
- bounded code/test/config scope;
- dependency/predecessor assumptions;
- prohibited/shared hotspots;
- verification expectations.

Do not pass unrelated project context or prior debugging narrative.

## Parallel execution

Fan out only lanes that are both dependency-independent and write-safe.

When writers need filesystem separation, use run-owned temporary worktrees/workspaces. One lane has one accountable writer for its writable scope.

The controller records each dispatch and completion in `state.json`.

## Integration

Integrate only into the exact candidate tracked by run state.

If integration exposes a product/architecture ambiguity, do not resolve it in the controller. Return to the appropriate reasoning stage.

If integration materially changes dependency assumptions or lane ownership, mark the plan `STALE` and run the Decomposer again.

## Corrections

A reviewer identifies findings; it does not choose the correction route.

Reuse a writer lane only when its objective, dependencies, hotspots, verification boundary, authority, and complexity remain unchanged. Otherwise re-plan the affected scope before correction writes.
