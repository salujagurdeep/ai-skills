# Independent Review and Completion

Review is independent from implementation and is required for material Shipwright work.

## Reviewer isolation

Use a fresh reviewer context that did not implement or correct the candidate.

Do not seed the reviewer with implementer reasoning, intended solution narrative, prior review findings, correction narrative, or expected verdict before blind reconstruction.

## Phase A — Blind reconstruction

Give the reviewer only:

- exact candidate diff/state;
- relevant repository state/relationships;
- tests and runtime/evidence produced by the candidate;
- affected files/contracts needed to understand the change.

The reviewer records, before authority reveal:

```text
BLIND RECONSTRUCTION
Actual behavior changed: ...
Apparent purpose: ...
Affected scope: ...
Contracts/assumptions preserved or changed: ...
Implied edge cases/failure modes: ...
Evidence gaps: ...
```

Persist this under `review/` before continuing.

## Phase B — Authority reconciliation

Reveal `requirements.md`, `architecture.md`, and applicable repository authority.

The reviewer then checks:

- requirement completeness and correctness;
- architecture conformance;
- partial/adjacent solution risk;
- hidden contract or behavior changes;
- error/recovery/edge cases;
- security/privacy/permission implications;
- compatibility and migration implications;
- regression/blast radius;
- maintainability and repository consistency;
- adequacy of tests/runtime/visual evidence.

Verdict:

```text
REVIEW PASS
```

or:

```text
CORRECTION REQUIRED
- BLOCKER: ...
- MAJOR: ...
- MINOR: ...
```

A material mismatch between reconstructed behavior and resolved authority blocks acceptance.

## Corrections and re-review

Send findings to a bounded writer/correction lane only after correction routing is established.

After correction:

1. integrate a new exact candidate;
2. create a **new reviewer context**;
3. start again from blind reconstruction;
4. do not give the new reviewer prior findings during the blind phase.

There is no automatic acceptance because a requested correction was implemented.

## UI work

When the user/repository explicitly supplies a prototype, design file, screenshot baseline, or other current visual authority for this task, use it during authority reconciliation after blind reconstruction.

Otherwise review UI against the resolved requirement, current accepted product/design system, accessibility/interaction expectations, and unintended visual regressions. Historical design artifacts do not automatically become acceptance authority.

## Verification

After `REVIEW PASS`, run repository-appropriate evidence. Select only applicable checks:

- unit/component tests;
- integration tests;
- build/type/lint/static checks;
- runtime/browser/device checks;
- data migration verification;
- compatibility/regression tests;
- visual evidence;
- deployment/package checks.

Verification must cover the behavior that review accepted, not merely report a generic test-suite pass.

## Git completion

Only commit the exact reviewed and verified candidate.

Before terminal completion:

- record baseline and final SHA;
- confirm changed paths stay within resolved scope;
- confirm required tests/evidence passed;
- confirm worktree/index cleanliness excluding explicitly unrelated pre-existing state;
- push only when remote write authorization and repository/user workflow make that action authorized;
- if push is required but blocked, report the run as blocked rather than complete;
- if push is not authorized/required, report the exact local reviewed commit.

## Terminal states

### COMPLETE

All required requirement, architecture, implementation, review, verification, and authorized Git steps are complete.

### BLOCKED

Persist state and report:

- exact blocked phase;
- blocker;
- decision/dependency needed;
- safe work, if any, that remains possible;
- run-state path;
- exact next action.

Do not discard or silently restart a blocked run.
