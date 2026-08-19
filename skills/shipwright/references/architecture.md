# Architecture Assessment and Resolution

Architecture is a reasoning stage, not a controller responsibility.

## Architect role

Use a fresh reasoning context after requirement authority is resolved enough to design against.

The Architect may make technical architecture decisions inside resolved product authority. It must preserve product intent and must not silently fill missing product decisions.

## Step 1 — Assess sufficiency

Inspect relevant existing architecture, code relationships, data ownership, integration boundaries, runtime/deployment patterns, and repository precedent.

Return:

```text
ARCHITECTURE ASSESSMENT
Status: SUFFICIENT | RESOLUTION_REQUIRED | BLOCKED_ON_REQUIREMENT
```

### SUFFICIENT

Use when the requested implementation can follow an established architecture without creating a new material technical choice.

Record the patterns/contracts that implementation must preserve. Do not redesign a working architecture merely because another design is possible.

### RESOLUTION_REQUIRED

Use when implementation genuinely requires a new or changed technical decision, for example:

- responsibility/service boundary;
- persistence/data ownership model;
- synchronization/concurrency strategy;
- API/event interaction pattern;
- authentication/authorization mechanism inside already-resolved security requirements;
- migration/rollout mechanism;
- significant framework/runtime integration;
- failure/recovery model.

The Architect selects and records the technical design.

Prefer, in order:

1. explicit repository architecture authority;
2. established repository patterns that satisfy the requirement;
3. the smallest coherent new design that satisfies the requirement and constraints.

Evaluate alternatives only when the choice is material. Avoid speculative future-proofing.

### BLOCKED_ON_REQUIREMENT

Return to the requirement loop when architecture would otherwise decide a missing product matter, including:

- externally visible behavior;
- acceptance meaning;
- security/privacy policy rather than implementation mechanism;
- public API compatibility that was not authorized to change;
- irreversible business/data semantics;
- material vendor/cost/operational commitment not implicit in the repository/request;
- material user experience or scope.

## Architecture output

Write `architecture.md`:

```text
# Architecture

Status: READY

## Existing architecture used
- ...

## Decisions
### A-001 — <decision>
Decision: ...
Rationale: ...
Constraints preserved: ...
Affected surfaces: ...

## Contracts / boundaries
- ...

## Data / state
- ...

## Failure / migration / rollout
- ...

## Implementation implications
- ...

Open architecture decisions: NONE
```

Omit sections that are not applicable. Keep the artifact concise enough for implementers to consume.

## Change requests

For a `CHANGE`, architecture should preserve existing technical contracts unless the requested outcome or necessary implementation explicitly requires changing them. If a change can be implemented safely within the current architecture, report `SUFFICIENT` and avoid architectural churn.

## Gate

No material decomposition/writer dispatch until:

```text
requirements: RESOLVED
architecture: READY
```
