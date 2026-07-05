# AKOS Handoff Protocol

Status: Active Draft
Version: 0.1.0
Created: 2026-07-04

## Purpose

This protocol defines what every AKOS-aware session should read and write so continuity survives across tools, models, and time.

## Start-of-Session Handoff

Read these first:

1. `README.md`
2. `AKOS_MANIFEST.yaml`
3. `BUILD_INDEX.md`
4. `CURRENT_STATE.md`
5. Relevant spec, contract, or integration file for the task

## Session Intake Questions

Before acting, identify:

- What object is being changed?
- What is the canonical source?
- What is the current status?
- What prior decision controls this work?
- What would count as done?

## End-of-Session Handoff

Every meaningful session should record:

- files changed
- commits created
- decisions made
- blockers
- next action
- superseded items
- open loops

## Continuity Rule

Do not create a disconnected report when a canonical thread, file, or lane already exists.

Append deltas where continuity matters.

## Machine Summary

```json
{
  "document": "handoff-protocol",
  "version": "0.1.0",
  "start_files": ["README.md", "AKOS_MANIFEST.yaml", "BUILD_INDEX.md", "CURRENT_STATE.md"],
  "end_fields": ["files_changed", "commits", "decisions", "blockers", "next_action", "open_loops"]
}
```
