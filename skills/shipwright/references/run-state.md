# Shipwright Run State

The run workspace is Shipwright's execution memory. Conversation is the interface; persisted state is the source of truth for progress.

## Location

Use `$SHIPWRIGHT_RUN_ROOT` when set. Otherwise use the platform writable temporary directory:

```text
<temp>/shipwright/<repository-fingerprint>/<run-id>/
```

The fingerprint derives from canonical repository path/remote identity without exposing secrets.

## Required files

```text
state.json
requirements.md
architecture.md
plan.md
evidence/
review/
workspaces/
```

`workspaces/` is optional.

## State

Keep `state.json` compact. Track run ID, repository/baseline branch+SHA, mode/request, phase, requested/actual controller route, requirements/architecture/diagnosis/plan status, lanes, candidate SHA, review tier/attempt/status, verification, Git state, blockers and updated timestamp.

Each lane records ID/objective, dependencies, status, workspace, requested profile/model/reasoning, actual profile/model/reasoning, evidence pointer and integrated candidate/commit identity.

## Transition rule

Before every material transition:

1. read `state.json`;
2. confirm current phase/prerequisites;
3. perform one legal next action;
4. persist result immediately;
5. only then dispatch/transition again.

Do not infer progress from conversation when persisted state exists.

## High-level transitions

```text
ORIENTATION -> REQUIREMENTS
REQUIREMENTS -> ARCHITECTURE | BLOCKED
ARCHITECTURE -> DIAGNOSIS | PLANNING | REQUIREMENTS | BLOCKED
DIAGNOSIS -> PLANNING | REQUIREMENTS | ARCHITECTURE | BLOCKED
PLANNING -> IMPLEMENTATION | BLOCKED
IMPLEMENTATION -> REVIEW | PLANNING | BLOCKED
REVIEW -> VERIFICATION | IMPLEMENTATION | PLANNING | BLOCKED
VERIFICATION -> GIT | IMPLEMENTATION | BLOCKED
GIT -> COMPLETE | BLOCKED
```

Returning to PLANNING means old decomposition is stale.

## Resume

For `$shipwright resume`, identify current repository, locate non-terminal runs for its fingerprint, choose newest unless multiple are plausibly active, re-read persisted phase artifacts, verify repository baseline/candidate did not materially diverge, then resume from next legal transition.

`$shipwright resume <run-id>` selects the run explicitly and applies the same consistency checks.

Do not delete blocked/interrupted runs. After COMPLETE, remove only run-owned worktrees/temp clones/process artifacts; preserve only evidence user/repository policy requires. Never delete unrelated temporary files.
