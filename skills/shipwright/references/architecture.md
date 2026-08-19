# Architecture Assessment and Resolution

Architecture is a dedicated reasoning stage, not a controller responsibility.

## Agent route

```text
Profile: shipwright-architect
Model: gpt-5.6-sol
Reasoning: high
Mode: read-only
```

Use a fresh architect context after Requirement Authority is sufficiently resolved.

The Architect may make technical architecture decisions inside resolved product authority. It must preserve product intent and must not silently fill missing product decisions.

## Assess sufficiency

Inspect relevant architecture, code relationships, data ownership, integration boundaries, runtime/deployment patterns and repository precedent. Prefer Graphify relationship evidence when available/current enough.

Return:

```text
ARCHITECTURE ASSESSMENT
Status: SUFFICIENT | RESOLUTION_REQUIRED | BLOCKED_ON_REQUIREMENT
```

### SUFFICIENT

Implementation can follow established architecture without a new material technical choice. Record patterns/contracts to preserve; do not redesign merely because another design is possible.

### RESOLUTION_REQUIRED

Use when implementation requires a new/changed technical decision such as responsibility/service boundary, persistence/data ownership mechanism, synchronization/concurrency, API/event interaction, authentication/authorization mechanism inside resolved security requirements, migration/rollout, framework/runtime integration, or failure/recovery.

Prefer explicit repository architecture, then established patterns satisfying Requirement Authority, then the smallest coherent new design satisfying requirements/constraints. Evaluate alternatives only when material; avoid speculative future-proofing.

### BLOCKED_ON_REQUIREMENT

Return to Analyst/user when architecture would otherwise decide externally visible behavior, acceptance meaning, security/privacy policy, unauthorized public compatibility, irreversible business/data semantics, material vendor/cost commitment, or material UX/scope.

## Architecture output

Write concise `architecture.md` with `Status: READY`, existing architecture used, numbered decisions/rationale, affected contracts/boundaries, data/state, failure/migration/rollout implications, implementation implications, and `Open architecture decisions: NONE`.

For `CHANGE`, preserve existing technical contracts unless the requested outcome or necessary implementation requires change. If current architecture safely supports the delta, report `SUFFICIENT` and avoid churn.

No material decomposition/writer dispatch until `requirements: RESOLVED` and `architecture: READY`.
