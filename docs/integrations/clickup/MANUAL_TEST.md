# ClickUp Manual Test

Status: Active Draft
Version: 0.1.2
Created: 2026-07-04
Updated: 2026-07-07

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
Pass
```

## Result Record

Date run: 2026-07-07

Result: Pass

ClickUp task ID:

```text
86ajea1uj
```

ClickUp task URL:

```text
https://app.clickup.com/t/86ajea1uj
```

ClickUp location:

```text
Team Space / AKOS / AKOS Integrations
```

What passed:

- AKOS folder was created in Team Space.
- AKOS Integrations list was created inside the AKOS folder.
- Test task was created in the AKOS Integrations list.
- Task preserves source file context: `GlacierEQ/AKOS/CURRENT_STATE.md`.
- Task preserves review state: Draft.
- Task preserves next action: complete integration specs in `docs/integrations`.
- Task states that GitHub remains canonical for AKOS architecture.

What failed:

- No pass criteria failed.

Limitations:

- Custom ClickUp fields were not created by this test.
- Required AKOS fields were preserved in the task description rather than native custom fields.

Next action:

```text
Build Supabase integration pack using the same folder-based pattern.
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
| Naming | Pass |
| Architecture | Pass |
| Failure Handling | Pass |
| Maintainability | Pass |
| Authenticity | Pass |
| Observability | Pass with limitation: fields are in description, not native custom fields |
| Documentation | Pass |

## Machine Summary

```json
{
  "document": "clickup-manual-test",
  "version": "0.1.2",
  "status": "pass",
  "date_run": "2026-07-07",
  "task_id": "86ajea1uj",
  "task_url": "https://app.clickup.com/t/86ajea1uj",
  "location": "Team Space / AKOS / AKOS Integrations",
  "next_action": "build Supabase integration pack"
}
```
