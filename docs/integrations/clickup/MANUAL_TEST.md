# ClickUp Manual Test

Status: Active Draft
Version: 0.1.0
Created: 2026-07-04

## Purpose

This file defines the first manual test for AKOS ClickUp integration.

The goal is to prove that ClickUp can represent AKOS work without losing source context.

## Test Object

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

## Pass Criteria

The test passes if:

- the task exists in ClickUp
- the task points back to `CURRENT_STATE.md`
- the task has a clear next action
- the task has a review state
- the task does not pretend ClickUp is the canonical source

## Fail Criteria

The test fails if:

- the task has no source
- the task has no next action
- the task duplicates an existing task without reference
- the task cannot be traced back to AKOS

## Result Field

Record the result as:

```text
Not Run / Pass / Fail / Blocked
```

Current result:

```text
Not Run
```
