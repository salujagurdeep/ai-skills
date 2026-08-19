---
name: shipwright
description: End-to-end software delivery orchestration for Codex. Use when the user wants to implement a feature, module, product change, behavior-changing refactor, defect correction, or other bounded software outcome from a short requirement through requirement completeness, architecture, GPT-5.6-optimized dependency-aware implementation, independent review, verification, and Git completion. Shipwright persists durable run state outside the product repository so long-running work does not depend on conversational memory.
---

# Shipwright

Shipwright takes a software intent from **request to reviewed delivery**.

Use it for:

- `NEW_IMPLEMENTATION` — a new capability, feature, module, integration, or substantial implementation;
- `CHANGE` — an intentional change to existing behavior, workflow, API, UI, data flow, architecture, or technical capability;
- `CHANGE_WITH_DIAGNOSIS` — a requested correction where the actual cause must be established before the desired outcome can be implemented.

A one-sentence request is valid input. Do not require the user to supply an implementation plan.

## Core lifecycle

```text
INTENT
  -> repository orientation
  -> requirement completeness
  -> resolved Requirement Authority
  -> architecture assessment / resolution
  -> dependency-first execution plan
  -> bounded implementation
  -> integration
  -> independent review
  -> corrections + fresh re-review
  -> verification
  -> exact Git completion
```

The run workspace is execution memory. The controller follows persisted state; conversation is only the interface.

Read these references as needed:

- `references/model-routing.md`
- `references/run-state.md`
- `references/requirements.md`
- `references/architecture.md`
- `references/execution.md`
- `references/review-and-completion.md`

## GPT-5.6 optimized topology

Preferred routes:

```text
Controller / long-running orchestration
  shipwright-controller -> gpt-5.6-luna / xhigh

Repository orientation
  shipwright-scout -> gpt-5.6-luna / medium

Requirement Authority
  shipwright-analyst -> gpt-5.6-sol / high

Architecture
  shipwright-architect -> gpt-5.6-sol / high

Dependency decomposition
  shipwright-decomposer -> gpt-5.6-sol / high

Diagnosis
  shipwright-investigator -> gpt-5.6-luna / max
  shipwright-investigator-hard -> gpt-5.6-terra / high

Implementation
  SIMPLE -> shipwright-builder-simple -> gpt-5.6-luna / medium
  MEDIUM -> shipwright-builder -> gpt-5.6-luna / max
  HARD -> shipwright-builder-hard -> gpt-5.6-terra / high

Independent review
  STANDARD -> shipwright-reviewer -> gpt-5.6-sol / medium
  DEEP -> shipwright-reviewer-deep -> gpt-5.6-sol / high
```

Do not silently replace an intended route with another model/effort. If a bundled route cannot launch, emit `MODEL_ROUTE_UNAVAILABLE`, state the requested route and known alternatives, and ask whether to continue with an explicit fallback. Persist requested and actual routes.

For best token efficiency, the parent Shipwright session should run on `gpt-5.6-luna` with `xhigh` reasoning. If it does not, record `CONTROLLER_ROUTE_FALLBACK`; do not let the controller compensate by taking substantive reasoning work from designated agents.

## Controller decision firewall

The controller may inspect state, create/maintain the run workspace, dispatch/wait/resume agents, apply deterministic routing, integrate non-conflicting completed work, run verification, record evidence/state, perform authorized Git handoff, and escalate blockers.

The controller must not invent, silently default, or reinterpret substantive product behavior, acceptance, architecture, technology, ownership, data semantics, public contracts, security/privacy policy, migration strategy, material UX, or scope.

Requirements, architecture, diagnosis, decomposition, implementation and review belong to their designated agents.

## Durable run workspace

Before material work, create or resume a run workspace outside the product repository. Use `$SHIPWRIGHT_RUN_ROOT` when set; otherwise use the platform writable temporary directory:

```text
<temp>/shipwright/<repository-fingerprint>/<run-id>/
```

Minimum state:

```text
state.json
requirements.md
architecture.md
plan.md
evidence/
review/
workspaces/        # only when separate writable lanes are needed
```

Rules:

1. Never commit Shipwright run artifacts to the product repository.
2. Re-read `state.json` before every material transition or dispatch.
3. Persist immediately after each phase, blocker, agent/lane result, review, correction, verification and Git transition.
4. Do not infer progress from conversation when persisted state exists.
5. Preserve non-terminal run state if interrupted or blocked.
6. Clean only run-owned temporary workspaces after terminal completion.
7. `$shipwright resume` resumes the newest non-terminal run for the current repository; `$shipwright resume <run-id>` selects a run explicitly.

## Phase 1 — Orientation

Use the smallest useful evidence first:

1. repository instructions;
2. Graphify query when Graphify is installed and current enough;
3. `shipwright-scout` for bounded confirmation;
4. native relationship/search tooling when graph evidence is unavailable.

Graphify is recommended for large repositories but is never required. Prefer scoped graph queries over broad source loading for relationship/orientation questions when available.

Record baseline branch/SHA, working-tree state, relevant durable authority, relevant code/tests/contracts, current behavior for `CHANGE`, and observed failure evidence for `CHANGE_WITH_DIAGNOSIS`.

## Phase 2 — Requirement completeness

Launch fresh `shipwright-analyst` (`gpt-5.6-sol`, high).

The analyst consumes intent plus bounded evidence, builds a private completeness map, separates resolved facts from material unknowns, challenges vague/inconsistent requirements, and asks only compact questions that materially affect observable behavior, acceptance, scope, security/privacy, compatibility, migration or material UX.

For `CHANGE`, establish:

```text
current accepted behavior
+
requested delta
+
preservation envelope
```

Unspecified behavior remains preserved.

Output `requirements.md` with `Open decisions: NONE` before architecture/implementation continues.

## Phase 3 — Architecture

Launch fresh `shipwright-architect` (`gpt-5.6-sol`, high).

First assess whether existing architecture is sufficient. Preserve it when it is. When a technical decision is required, the architect may resolve technical architecture inside approved Requirement Authority, including responsibility boundaries, persistence mechanics, concurrency/recovery, integrations, migrations, runtime/deployment mechanics and failure handling.

Return to the analyst/user rather than decide missing product behavior, public compatibility, security/privacy policy, irreversible business semantics, material vendor/cost commitments, or material UX/scope.

No material writer dispatch until `requirements: RESOLVED` and `architecture: READY`.

## Phase 4 — Diagnosis when needed

Ordinary `NEW_IMPLEMENTATION` and intentional `CHANGE` do not require diagnosis.

For `CHANGE_WITH_DIAGNOSIS`, launch `shipwright-investigator` / Luna max for bounded diagnosis, or `shipwright-investigator-hard` / Terra high when cross-layer/stateful/concurrency/recovery-sensitive or still difficult after one bounded investigation.

Investigators are read-only. If diagnosis changes Requirement Authority or architecture assumptions, return to Analyst/Architect before planning.

## Phase 5 — Dependency-first planning

Launch fresh `shipwright-decomposer` (`gpt-5.6-sol`, high).

Build the dependency model before cutting lanes. Each lane must include objective, predecessors, owned scope, shared/prohibited hotspots, verification boundary, parallel wave, `SIMPLE | MEDIUM | HARD`, and exact writer route.

Optimize for correctness, dependency order, maximum safe parallelism, minimal shared-write contention, minimal writer context, lowest-cost capable route, and behavioral/verification cohesion.

Persist `plan.md` and lane routes before dispatch.

## Phase 6 — Implementation and integration

Dispatch only the decomposer-selected writer:

```text
SIMPLE -> shipwright-builder-simple -> Luna medium
MEDIUM -> shipwright-builder -> Luna max
HARD   -> shipwright-builder-hard -> Terra high
```

Give each writer only lane objective, applicable Requirement Authority, applicable architecture, owned scope, dependencies, shared/prohibited hotspots, and focused verification expectations.

Writers may make local implementation choices inside established authority and architecture; they must not redesign product/architecture/scope.

Fan out only dependency-independent and write-safe lanes. Use run-owned temporary worktrees/workspaces when separation is needed. Persist requested/actual route and result after each lane.

If integration changes material dependencies, authority, architecture assumptions, hotspots or verification boundaries, mark plan stale and re-run the appropriate reasoning stage.

## Phase 7 — Independent review

Every material candidate gets a fresh reviewer that did not implement/correct it.

```text
STANDARD -> shipwright-reviewer -> gpt-5.6-sol / medium
DEEP     -> shipwright-reviewer-deep -> gpt-5.6-sol / high
```

Use DEEP for high-consequence security/privacy, migrations/data integrity, public/shared contracts, concurrency/recovery, architecture-sensitive or broad cross-layer changes, or difficult correction history.

Review is blind-first. First provide candidate diff/state, relevant relationships and evidence without Requirement Authority, architecture rationale or implementer narrative. Persist `BLIND_RECONSTRUCTION_RECORDED`. Then reveal requirements/architecture and reconcile actual behavior against authority.

Material mismatch blocks acceptance. Every corrected candidate gets a new reviewer context and new blind phase. External audit is optional, never required.

## Phase 8 — Verification and Git completion

After review acceptance, run risk-proportional repository-native verification: focused tests, integration/runtime checks, regression proportional to blast radius, build/lint/type/static checks, visual evidence when material, and migration/deployment checks when changed.

Only commit the exact reviewed and verified candidate. Push only when authorized/required and verify remote equality when pushed.

Before `COMPLETE`, verify changed paths remain in scope, required review/verification passed, final SHA is recorded, repository cleanliness is established excluding unrelated pre-existing state, and run-owned temporary workspaces are cleaned.

## Terminal report

```text
SHIPWRIGHT COMPLETE
Request: <short outcome>
Mode: NEW_IMPLEMENTATION | CHANGE | CHANGE_WITH_DIAGNOSIS
Requirements: RESOLVED
Architecture: READY
Implementation: COMPLETE
Independent review: PASS
Verification: PASS
Final commit: <sha>
Remote: <ref/sha | NOT_PUSHED — reason>
Run state: <path>
Model routes: <summary>
```

For blocked work, persist the run and report exact phase, blocker, decision/dependency needed, run path and next legal action.
