# ClickUp Manual Test

Status: Active Draft
Version: 0.1.1
Created: 2026-07-04
Updated: 2026-07-05

## Purpose

This file defines the first manual test for AKOS ClickUp integration.

The goal is to prove that ClickUp can represent AKOS work without losing source context, review state, or canonical boundary.

## Test Source

Use this source file:

```text
CURRENT_STATE.md
```

## Test Task

Create one ClickUp task from an open loop in `CURRENT_STATE.md`.

Recommended task title:

```text
AKOS: finish integration specs
```

## Required Task Fields

The task should include:

- AKOS Type: Open Loop
- Source: CURRENT_STATE.md
- Status: Ready
- Priority: High
- Review State: Draft
- Next Action: complete integration specs in docs/integrations

## Required Links

The task should link back to:

```text
GlacierEQ/AKOS/CURRENT_STATE.md
```

## Pass Criteria

The test passes if:

- the task exists in ClickUp
- the task points back to `CURRENT_STATE.md`
- the task has a clear next action
- the task has a review state
- the task does not represent itself as the canonical source
- a human can understand completion without reading this chat

## Fail Criteria

The test fails if:

- the task has no source
- the task has no next action
- the task duplicates an existing task without reference
- the task cannot be traced back to AKOS
- the task claims completion when GitHub work is not complete

## Result Field

Record the result as:

```text
Not Run / Pass / Fail / Blocked
```

Current result:

```text
Not Run
```

## Result Recording Rule

After the manual test is run, update this file with:

- date run
- result
- task URL or task ID
- what passed
- what failed
- next action

## Pro-Code Check

| Gate | Result |
|---|---|
| Naming | Test object and task title are explicit |
| Architecture | ClickUp points back to GitHub source |
| Failure Handling | Fail criteria are defined |
| Maintainability | Test is manual and repeatable |
| Authenticity | Test proves only source preservation, not full automation |
| Observability | Result field is explicit |
| Documentation | Test lives in AKOS repo |

## Machine Summary

```json
{
  "document": "clickup-manual-test",
  "version": "0.1.1",
  "status": "not_run",
  "test_source": "CURRENT_STATE.md",
  "test_task": "AKOS: finish integration specs"
}
```
