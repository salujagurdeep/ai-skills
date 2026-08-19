# Shipwright Run State

The run workspace is Shipwright's execution memory. Conversation is the interface; persisted run state is the source of truth for progress.

## Location

Use `$SHIPWRIGHT_RUN_ROOT` when set. Otherwise use the platform's writable temporary directory:

```text
<temp>/shipwright/<repository-fingerprint>/<run-id>/
```

The repository fingerprint should be derived from the canonical repository path or remote identity without exposing secrets. The run ID should be unique and human-readable enough to resume.

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

`workspaces/` is optional and exists only when separate writer worktrees/workspaces are needed.

## State shape

Keep `state.json` compact. Minimum fields:

```json
{
  "run_id": "...",
  "repository": "...",
  "baseline_branch": "...",
  "baseline_sha": "...",
  "mode": "NEW_IMPLEMENTATION | CHANGE",
  "request": "...",
  "phase": "ORIENTATION | REQUIREMENTS | ARCHITECTURE | PLANNING | IMPLEMENTATION | REVIEW | VERIFICATION | GIT | COMPLETE | BLOCKED",
  "requirements": "NOT_STARTED | IN_PROGRESS | RESOLVED | BLOCKED",
  "architecture": "NOT_STARTED | IN_PROGRESS | READY | BLOCKED",
  "plan": "NOT_STARTED | READY | STALE",
  "lanes": [],
  "candidate_sha": null,
  "review": "NOT_STARTED | IN_PROGRESS | PASS | CORRECTION_REQUIRED",
  "verification": "NOT_STARTED | PASS | FAIL",
  "git": "NOT_STARTED | COMMITTED | PUSHED | PUSH_NOT_AUTHORIZED",
  "blockers": [],
  "updated_at": "..."
}
```

Lane records should contain only execution-relevant state: lane ID, objective, dependencies, status, workspace, owner/agent context identifier when available, result/evidence pointers, and integrated commit/candidate identity.

## Transition rule

Before every material transition:

1. read `state.json`;
2. confirm the current phase and prerequisites;
3. perform one legal next action;
4. persist the result immediately;
5. then dispatch or transition again.

Do not infer phase progress from the conversation when persisted state exists.

## Legal high-level transitions

```text
ORIENTATION -> REQUIREMENTS
REQUIREMENTS -> ARCHITECTURE | BLOCKED
ARCHITECTURE -> PLANNING | REQUIREMENTS | BLOCKED
PLANNING -> IMPLEMENTATION | BLOCKED
IMPLEMENTATION -> REVIEW | PLANNING | BLOCKED
REVIEW -> VERIFICATION | IMPLEMENTATION | PLANNING | BLOCKED
VERIFICATION -> GIT | IMPLEMENTATION | BLOCKED
GIT -> COMPLETE | BLOCKED
```

Returning to `PLANNING` means material dependency/scope/architecture implications changed and the old decomposition is stale.

## Resume

For `$shipwright resume`:

1. identify the current repository;
2. locate non-terminal runs for its fingerprint;
3. choose the newest run unless more than one is plausibly active, in which case ask the user to choose;
4. re-read all persisted phase artifacts required by `state.json`;
5. verify the repository baseline/candidate has not materially diverged;
6. resume from the next legal transition.

For `$shipwright resume <run-id>`, select that run directly and perform the same consistency checks.

## Cleanup

Do not delete a blocked or interrupted run.

After `COMPLETE`:

- preserve only evidence the user/repository workflow explicitly requires;
- remove run-owned worktrees/temp clones/process artifacts;
- the run directory may then be removed or retained according to user policy.

Never delete unrelated temporary files.
