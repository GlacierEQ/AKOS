# AKOS Finisher

The Finisher exists to stop the 98% loop.

It does not brainstorm, expand architecture, create another parallel runtime, or
turn a finished branch into a new research project. It reads an explicit
allowlist of pull requests and answers four questions:

1. Is this work open and still unfinished?
2. Is there a concrete blocker, or only inertia?
3. What is the shortest authorized action that closes it?
4. Did GitHub return a receipt proving the action occurred?

## Finish-first law

> When finishable work exists, expansion is blocked.

`gate` exits with status `3` whenever the queue contains an item that can be
marked ready, merged, or closed without first fixing a hard blocker.

## Commands

```bash
export GITHUB_TOKEN="..."
python -m finisher.finisher scan --config finisher/config.json
python -m finisher.finisher gate --config finisher/config.json
```

Outputs:

- `finisher/out/FINISH_QUEUE.md`
- `finisher/out/FINISH_RECEIPT.json`

The receipt contains the exact PR head SHA used by the scan and a SHA-256 over
the canonical receipt payload.

## Applying closure actions

Application is deliberately two-key:

1. set `policy.allow_apply` to `true` in the reviewed config;
2. set `FINISHER_APPLY=YES` in the execution environment.

Then:

```bash
python -m finisher.finisher apply --config finisher/config.json
```

Only allowlisted targets may be changed. The default action budget is one PR
per run. Merge requests include the expected head SHA so GitHub rejects the
operation if the branch moved after scanning.

## Decision rules

### Hard blockers

- PR is closed or already merged;
- GitHub reports a merge conflict;
- a reported check is pending, failed, or errored;
- an explicitly required check is absent;
- an active review requests changes;
- the configured approval count is unmet;
- a draft is not authorized for promotion.

### Soft blockers

- mergeability has not finished computing;
- no checks are reported and policy permits that condition;
- a draft is authorized to be marked ready.

Soft blockers do not become permanent vetoes. They determine the next action.

## Safety boundary

The Finisher never:

- force-pushes or rewrites history;
- modifies evidence or source files in target repositories;
- creates repositories, issues, or replacement projects;
- contacts courts, hospitals, counsel, agencies, or other third parties;
- reports a merge, close, or promotion without the provider response;
- performs more actions than `max_actions_per_run`.

## Current queue

The checked-in queue is intentionally small and closure-focused:

1. Queen's evidence package — `CHERRY_CHAN_RECOVERY_MATRIX#3`;
2. source-linked actor registry — `AEON-777#52`;
3. bounded canonical CaseBrain core — `SUPERLUMINAL_CASE_MATRIX#62`;
4. AKOS connector reconciliation — `AKOS#4`.

Adding a target requires removing ambiguity about the desired end state. A
repository name or general project aspiration is not a finish target.
