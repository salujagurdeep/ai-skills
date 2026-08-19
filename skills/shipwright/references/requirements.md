# Requirement Completeness Method

Shipwright accepts a short request, but implementation must not begin while material product intent remains ambiguous.

## Agent route

```text
Profile: shipwright-analyst
Model: gpt-5.6-sol
Reasoning: high
Mode: read-only
```

Use a fresh analyst context. The analyst may reason about product requirements, challenge the request and ask the user for missing product decisions. The controller may not.

## Evidence first

Inspect the smallest relevant repository evidence before asking questions: existing behavior/tests, product/specification documentation, relevant UI/API/data contracts, repository instructions/compatibility constraints, and neighboring precedent. Use Graphify relationship queries when available and useful.

Do not ask the user for facts that repository evidence can establish.

## Classify

Exactly one:

```text
NEW_IMPLEMENTATION
CHANGE
CHANGE_WITH_DIAGNOSIS
```

For `CHANGE` modes identify current accepted behavior, explicit requested delta and preservation envelope. Everything unspecified remains preserved unless the requirement loop explicitly changes it.

`CHANGE_WITH_DIAGNOSIS` additionally records observed symptom/evidence; causal diagnosis happens later in an investigator lane.

## Private completeness map

Evaluate only applicable dimensions: objective/outcome, actors/permissions, happy path, states/lifecycle, validation/error behavior, persistence/session behavior, cross-system interaction, public API/event/data behavior, destructive/money/security/privacy implications, compatibility/migration, material UX, non-functional constraints affecting implementation, and acceptance evidence.

Mark each privately `RESOLVED | N/A | OPEN`.

## Focused challenge loop

Ask only `OPEN` decisions that can materially change implementation or acceptance. Keep questions compact, expose tradeoffs when useful, prefer concrete choices, challenge vague observable terms, group related questions into small batches, and do not reopen settled decisions without contradictory evidence.

Do not manufacture questions for a small explicit change whose behavior/blast radius are already clear.

## Requirement Authority

Write concise `requirements.md`:

```text
# Requirement Authority
Mode: NEW_IMPLEMENTATION | CHANGE | CHANGE_WITH_DIAGNOSIS

## Objective
...
## Current behavior
<CHANGE modes only>
## Requested delta
<CHANGE modes only>
## Preservation envelope
...
## Required behavior
- ...
## States / edge cases
- ...
## Constraints / compatibility
- ...
## Acceptance
- ...
## Explicitly out of scope
- ...

Open decisions: NONE
```

Reference durable repository authority rather than duplicating large documents. If product intent cannot be resolved without the user, set requirements `BLOCKED` and persist the exact decision request.
