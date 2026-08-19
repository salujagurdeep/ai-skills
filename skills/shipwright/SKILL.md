---
name: shipwright
description: End-to-end software delivery orchestration for Codex. Use when the user wants to implement a feature, module, product change, refactor with changed behavior, or other bounded software outcome from a short requirement through requirement completeness, architecture, dependency-aware implementation, independent review, verification, and Git completion. Shipwright maintains durable run state outside the product repository so long-running work can continue without relying on conversational memory.
---

# Shipwright

Shipwright takes a software intent from **request to reviewed delivery**.

Use it for both:

- `NEW_IMPLEMENTATION` — a new capability, feature, module, integration, or substantial implementation;
- `CHANGE` — an intentional change to an existing product, behavior, workflow, API, UI, data flow, or technical capability.

A one-sentence request is valid input. Do not require the user to provide an implementation plan.

## Core contract

Run the following lifecycle to completion:

```text
INTENT
  -> repository orientation
  -> requirement completeness
  -> resolved requirement authority
  -> architecture assessment / resolution
  -> dependency-first execution plan
  -> bounded implementation
  -> integration
  -> independent review
  -> corrections + re-review when needed
  -> verification
  -> exact Git completion
```

The primary Codex session is the **controller**. It owns execution state and coordination, not substantive product or architecture decisions.

## Controller decision firewall

The controller may:

- inspect repository and run state;
- create and maintain the run workspace;
- dispatch fresh reasoning, implementation, and review contexts;
- wait for dependencies and resume ready work;
- apply deterministic routing rules;
- integrate non-conflicting completed work;
- run verification commands;
- record evidence and state transitions;
- commit/push when authorized;
- escalate blocked decisions.

The controller must **not** invent, silently default, or reinterpret substantive decisions about product behavior, acceptance, architecture, technology, ownership boundaries, data semantics, public contracts, security/privacy policy, migration strategy, material UX, or scope.

Use specialized reasoning stages for those decisions and persist their outputs before implementation continues.

## Durable run workspace

Before material work, create a run workspace outside the product repository.

Default root:

```text
$SHIPWRIGHT_RUN_ROOT
```

If unset, use the platform's writable temporary directory and create:

```text
shipwright/<repository-fingerprint>/<run-id>/
```

The run workspace must contain at least:

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
3. Persist state immediately after every completed phase, blocker, lane result, review result, correction, verification result, and Git transition.
4. Do not rely on conversational memory for execution progress.
5. Preserve non-terminal run state if interrupted or blocked.
6. Clean run-owned temporary workspaces only after terminal completion and required evidence has been recorded.
7. `$shipwright resume` means locate the newest non-terminal run for the current repository and continue from its persisted state. `$shipwright resume <run-id>` selects an explicit run.

Read `references/run-state.md` before creating or resuming a run.

## Phase 1 — Orient before asking questions

Inspect the smallest useful repository surface first:

- repository instructions such as `AGENTS.md`;
- relevant product/specification/design documentation when present;
- current code and tests around the requested behavior;
- dependency relationships and shared contracts;
- current Git branch/SHA and working-tree state.

Use repository graph/index tools when available and useful, but Shipwright must not depend on a specific graph product.

For a `CHANGE`, establish the current accepted behavior and treat the user's requested delta as intentional. Preserve unspecified behavior unless later authority explicitly changes it.

Record the orientation evidence in the run state without copying large source excerpts.

## Phase 2 — Requirement completeness

Use a fresh **Requirements Analyst** reasoning context.

The Requirements Analyst:

1. consumes the user's intent plus bounded repository evidence;
2. builds a private completeness map;
3. separates already-resolved facts from material unknowns;
4. challenges vague or internally inconsistent requirements;
5. asks the user only for decisions that materially affect observable behavior, acceptance, scope, security/privacy, compatibility, migration, or user experience;
6. asks questions in compact decision-oriented batches rather than conducting an open-ended interview;
7. repeats until no material requirement decision remains unresolved.

Do not ask the user to restate repository facts that can be discovered.

Small, explicit changes may pass this phase without questions.

The phase output is `requirements.md`, containing concise resolved authority and `Open decisions: NONE` before architecture/implementation begins.

Read `references/requirements.md` for the exact method and output contract.

## Phase 3 — Architecture assessment and resolution

Use a fresh **Architect** reasoning context after requirement authority is complete enough to design against.

The Architect must first determine whether the repository's existing architecture is sufficient.

If sufficient:

- preserve it;
- identify the applicable patterns/contracts;
- avoid architecture churn.

If insufficient:

- make the technical architecture decisions required to implement the resolved requirements;
- prefer consistency with established repository patterns unless they are demonstrably unsuitable;
- document alternatives only when the choice is material;
- record the selected architecture and rationale in `architecture.md`.

The Architect may autonomously make **technical architecture decisions** that stay inside resolved product authority.

It must not silently decide a missing product requirement or materially change externally visible behavior, acceptance meaning, security/privacy policy, irreversible data semantics, public contracts, material vendor/operational commitments, or user scope. Those return to the Requirements Analyst/user decision loop.

No implementation lane may be created for material work until architecture is `READY`.

Read `references/architecture.md`.

## Phase 4 — Dependency-first execution planning

Use a fresh **Decomposer** reasoning context.

The Decomposer consumes only resolved requirement authority, architecture, repository evidence, and current state. It must build the dependency model **before** cutting work into lanes.

For each lane, establish:

- objective and owned scope;
- predecessors/dependencies;
- shared or prohibited hotspots;
- verification boundary;
- safe parallel group/wave;
- implementation complexity: `SIMPLE | MEDIUM | HARD`;
- the appropriate available coding-agent capability.

Optimize for the smallest coherent independently implementable and independently verifiable lanes, not the maximum number of agents.

Use safe parallelism aggressively when dependencies and write ownership permit it. Serialize shared hotspots.

Persist the complete plan to `plan.md` and `state.json` before writer dispatch.

Read `references/execution.md`.

## Phase 5 — Implementation and integration

Dispatch fresh bounded implementation contexts.

Each writer receives only what it needs:

- resolved lane objective;
- relevant requirement authority;
- relevant architecture;
- owned paths/capabilities;
- prohibited/shared hotspots;
- dependency assumptions;
- focused verification expectations.

Writers may make local implementation choices within established architecture and authority. They must not redesign product/architecture/scope on their own.

Prefer the least expensive available coding capability that can safely complete the lane; use stronger coding/reasoning capability for genuinely harder lanes. Shipwright must not require specific model names.

A writer does not independently redefine Git authority. The controller tracks and integrates the exact candidate.

When separate writable workspaces/worktrees are useful, place run-owned execution workspaces under the run workspace or another writable temporary location. They are execution artifacts, never authoritative repository state.

After each lane finishes:

1. record result/evidence;
2. update state;
3. integrate only when predecessors and conflict constraints permit;
4. refresh dependency evidence if the implementation materially changes relationships.

## Phase 6 — Independent review

Every material candidate receives independent review in a **fresh reviewer context that did not implement the candidate**.

Use two phases:

### Phase A — blind reconstruction

Give the reviewer:

- exact candidate diff/state;
- relevant tests and execution evidence;
- affected relationships/runtime evidence;
- no original requirement narrative, architecture rationale, implementer reasoning, correction narrative, or expected answer.

The reviewer records:

- what behavior actually changed;
- apparent purpose;
- true affected scope;
- assumptions/contracts changed or introduced;
- implied edge cases/failure modes.

Persist the reconstruction before revealing authority.

### Phase B — authority reconciliation

Then reveal the resolved requirements and architecture. The reviewer explicitly reconciles reconstructed behavior against them and checks correctness, completeness, regressions, security/compatibility implications, maintainability, evidence sufficiency, and unexplained scope.

Material mismatch blocks acceptance.

Corrections return to a bounded writer. Every corrected material candidate is reviewed again in a **new fresh reviewer context** starting with a new blind phase.

An external audit is optional; it is not required by Shipwright.

Read `references/review-and-completion.md`.

## Phase 7 — Verification and Git completion

After review acceptance, run risk-proportional verification using the repository's actual toolchain:

- focused unit/component tests;
- integration/runtime checks where relevant;
- regression tests proportional to blast radius;
- build/lint/type/static checks where applicable;
- visual/runtime evidence when UI correctness is material;
- migration/deployment checks when changed.

Complete Git handoff only for the **exact reviewed and verified candidate**.

Default completion behavior:

1. commit the reviewed candidate when repository/user policy permits;
2. push when remote write authorization is clear or the user/repository workflow requires it;
3. otherwise stop at the exact reviewed local commit and report that push was not authorized;
4. verify changed paths remain within resolved scope;
5. verify repository cleanliness excluding explicitly unrelated pre-existing state;
6. record final SHA/ref/evidence in run state;
7. clean run-owned temporary workspaces after terminal state.

Never claim completion when review, required verification, commit, or an authorized required push is still pending.

## Completion report

Return a concise terminal report:

```text
SHIPWRIGHT COMPLETE
Request: <short outcome>
Mode: NEW_IMPLEMENTATION | CHANGE
Requirements: RESOLVED
Architecture: READY
Implementation: COMPLETE
Independent review: PASS
Verification: PASS
Final commit: <sha>
Remote: <ref/sha | NOT_PUSHED — reason>
Run state: <path>
```

For a blocked run, report the exact phase, persisted run path, missing decision/dependency, and the precise next action. Do not discard the run state.
