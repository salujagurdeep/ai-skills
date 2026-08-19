# GPT-5.6 Model Routing

Shipwright is optimized around one principle:

> Spend expensive reasoning tokens only where additional intelligence can materially change the delivery outcome.

The `gpt-5.6` alias is GPT-5.6 Sol. Shipwright uses explicit model IDs so routing is visible and predictable.

## Optimized routes

| Role | Profile | Model | Effort |
|---|---|---|---|
| Controller | `shipwright-controller` | `gpt-5.6-luna` | `xhigh` |
| Scout | `shipwright-scout` | `gpt-5.6-luna` | `medium` |
| Requirements Analyst | `shipwright-analyst` | `gpt-5.6-sol` | `high` |
| Architect | `shipwright-architect` | `gpt-5.6-sol` | `high` |
| Decomposer | `shipwright-decomposer` | `gpt-5.6-sol` | `high` |
| Investigator | `shipwright-investigator` | `gpt-5.6-luna` | `max` |
| Hard Investigator | `shipwright-investigator-hard` | `gpt-5.6-terra` | `high` |
| Simple Builder | `shipwright-builder-simple` | `gpt-5.6-luna` | `medium` |
| Medium Builder | `shipwright-builder` | `gpt-5.6-luna` | `max` |
| Hard Builder | `shipwright-builder-hard` | `gpt-5.6-terra` | `high` |
| Standard Reviewer | `shipwright-reviewer` | `gpt-5.6-sol` | `medium` |
| Deep Reviewer | `shipwright-reviewer-deep` | `gpt-5.6-sol` | `high` |

## Why Luna xhigh for the controller

The controller is long-running. Its work is mainly durable state tracking, deterministic transitions, dispatch, waiting, evidence routing, integration control, verification and Git handoff. Luna xhigh gives the control plane reasoning headroom without spending Sol on every orchestration turn.

The controller must not compensate for a cheaper model by taking substantive requirement, architecture, decomposition, implementation or review decisions itself.

## Implementation complexity

### SIMPLE

Local/deterministic behavior, strong precedent, limited state/dependency complexity and focused verification.

```text
shipwright-builder-simple / gpt-5.6-luna / medium
```

### MEDIUM

Several coordinated changes or moderate state/dependency complexity, with clear requirements/architecture and no hard indicator.

```text
shipwright-builder / gpt-5.6-luna / max
```

### HARD

After decomposition the lane remains tightly coupled or contains strong indicators such as complex concurrency/idempotency/recovery, difficult persistence/migration semantics, fragile external integration, non-trivial state machines, rollback/recovery, or broad runtime verification.

```text
shipwright-builder-hard / gpt-5.6-terra / high
```

Do not route implementation to Sol merely because the overall request is large. Decompose first; use Sol for high-leverage reasoning that makes bounded implementation clear.

## Review routing

Use `STANDARD` unless the integrated candidate materially involves security/privacy/permissions, data integrity or migration/rollback, public/shared contracts, concurrency/idempotency/recovery, architecture-sensitive cross-layer behavior, broad blast radius, repeated correction history, or another high consequence. Those use `DEEP`.

## Route fallback

Do not silently substitute model/effort. If an exact route cannot run, emit `MODEL_ROUTE_UNAVAILABLE`, identify the requested route/reason, and require explicit fallback authorization. Persist requested and actual routes in `state.json`.
