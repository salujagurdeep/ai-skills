# Independent Review and Completion

Review is independent from implementation and required for material Shipwright work.

## Routes

```text
STANDARD -> shipwright-reviewer      / gpt-5.6-sol / medium
DEEP     -> shipwright-reviewer-deep / gpt-5.6-sol / high
```

Use DEEP for high-consequence security/privacy, migration/data-integrity, public/shared-contract, concurrency/recovery, architecture-sensitive, broad cross-layer or difficult-correction candidates.

## Reviewer isolation

Use a fresh reviewer that did not implement/correct the candidate. Do not seed it with implementer reasoning, intended solution narrative, previous findings, correction narrative or expected verdict before blind reconstruction.

## Phase A — Blind reconstruction

Give only exact candidate diff/state, relevant repository relationships/state, candidate tests/runtime/evidence and affected contracts needed to understand change.

Record actual behavior changed, apparent purpose, affected scope, changed/preserved contracts/assumptions, implied edge cases/failure modes and evidence gaps. Persist it and emit `BLIND_RECONSTRUCTION_RECORDED` before authority reveal.

## Phase B — Authority reconciliation

Reveal `requirements.md`, `architecture.md` and applicable durable repository authority. Check Requirement Authority correctness/completeness, architecture conformance, partial/adjacent solution risk, hidden contract/behavior changes, error/recovery/edge cases, security/privacy/permissions, compatibility/migration, regression/blast radius, maintainability/repository consistency and evidence sufficiency.

Return `REVIEW PASS` or prioritized `CORRECTION REQUIRED`. Material mismatch blocks acceptance.

## Corrections

After correction, integrate a new exact candidate, create a new reviewer context, start again from blind reconstruction and do not expose prior findings in the new blind phase. No automatic acceptance because requested corrections were implemented.

## Verification

After `REVIEW PASS`, run applicable repository-native unit/component/integration tests, build/type/lint/static checks, runtime/browser/device checks, migration verification, compatibility/regression tests, visual evidence and deployment/package checks. Evidence must cover accepted behavior, not merely report a generic suite pass.

## Git completion

Only commit the exact reviewed/verified candidate. Record baseline/final SHA, confirm changed paths stay in scope, required evidence passed and worktree/index cleanliness. Push only when authorized/required; required-but-blocked push means `BLOCKED`. If push is not authorized/required, report exact local reviewed commit. Clean run-owned temporary workspaces.

`COMPLETE` means Requirement Authority, architecture, implementation, independent review, verification and authorized Git steps are complete. A blocked run persists exact phase, blocker, needed decision/dependency, safe remaining work, run path and next action.
