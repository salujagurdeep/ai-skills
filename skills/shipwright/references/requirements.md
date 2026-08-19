# Requirement Completeness Method

Shipwright accepts a short request, but implementation must not begin while material product intent remains ambiguous.

## Requirements Analyst role

Use a fresh reasoning context. The analyst is allowed to reason about product requirements, challenge the request, and ask the user for missing product decisions. The controller is not.

## Step 1 — Evidence first

Before asking questions, inspect the smallest relevant repository evidence:

- existing behavior and tests;
- product/specification documentation when present;
- current UI/API/data contracts relevant to the request;
- repository instructions and compatibility constraints;
- neighboring features that establish precedent.

Do not ask the user for facts that can be established from the repository.

## Step 2 — Classify the request

Exactly one:

```text
NEW_IMPLEMENTATION
CHANGE
```

For `CHANGE`, identify:

```text
current accepted behavior
+
explicit requested delta
```

Everything unspecified remains preserved unless the requirement loop explicitly changes it.

## Step 3 — Private completeness map

Evaluate only applicable dimensions:

- objective/outcome;
- actors/roles/permissions;
- primary happy path;
- states and lifecycle;
- validation and error behavior;
- persistence/session behavior;
- cross-module/system interactions;
- externally visible API/event/data behavior;
- destructive/money/security/privacy implications;
- compatibility/migration expectations;
- materially important UX behavior;
- non-functional constraints that affect implementation;
- acceptance evidence.

Mark each `RESOLVED | N/A | OPEN` privately.

## Step 4 — Focused challenge loop

Ask only `OPEN` decisions that could materially change implementation or acceptance.

Questions should:

- be compact;
- expose tradeoffs when useful;
- prefer concrete choices over broad prompts;
- challenge vague words such as "fast", "secure", "simple", "same", or "support" when observable behavior depends on them;
- group related questions into a small batch;
- avoid reopening settled decisions without contradictory evidence.

Example:

```text
The request is clear except for two decisions:
1. Should saved drafts survive sign-out, or only browser/session restart?
2. When a referenced record is deleted, should the draft fail to reopen or reopen with the missing item removed?
```

Do not manufacture questions for a small explicit change whose behavior and blast radius are already clear.

## Step 5 — Requirement authority output

Write `requirements.md` in the run workspace:

```text
# Requirement Authority

Mode: NEW_IMPLEMENTATION | CHANGE

## Objective
<observable outcome>

## Current behavior
<CHANGE only; concise>

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

Do not copy large requirement documents into the run workspace. Reference repository paths/IDs where existing durable authority already exists.

If product intent cannot be resolved without the user, set requirement state to `BLOCKED` and persist the exact decision request.
