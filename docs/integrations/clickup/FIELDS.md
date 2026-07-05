# ClickUp Field Map

Status: Active Draft
Version: 0.1.1
Created: 2026-07-04
Updated: 2026-07-05

## Purpose

This file defines the minimum fields a ClickUp item should preserve when it represents AKOS work.

The purpose is traceability: a future operator should know what the item is, where it came from, what state it is in, and what completion means.

## Required Fields

| Field | Purpose |
|---|---|
| AKOS ID | Stable object identity when available |
| AKOS Type | Object class such as Task, Review, Project, Open Loop, or Adoption Item |
| Title | Human-readable work name |
| Status | Current work state |
| Owner | Person, agent, or system responsible for next action |
| Priority | Execution importance |
| Source | Origin file, repo, lane, note, or decision |
| Review State | Draft, working, review, accepted, historical, or blocked |

## Recommended Fields

| Field | Purpose |
|---|---|
| Due Date | Time-bound execution control |
| Related Object | Linked AKOS object or repo file |
| GitHub Path | Source architecture or implementation file |
| System | Source or target system |
| Last Checked | Most recent review date |
| Blocker | Short blocker statement |
| Next Action | One concrete next step |

## Status Mapping

| AKOS State | ClickUp State |
|---|---|
| draft | Draft |
| working | In Progress |
| review | Review |
| blocked | Blocked |
| accepted | Complete |
| historical | Archived |

## Minimal Valid Item

A minimal AKOS ClickUp item needs:

- title
- AKOS type
- source
- status
- owner or next action
- review state

## Field Rule

A ClickUp item is incomplete if it cannot point back to a source.

## Pro-Code Check

| Gate | Result |
|---|---|
| Naming | Fields are named plainly |
| Architecture | Fields preserve AKOS identity and source context |
| Failure Handling | Missing source makes item incomplete |
| Maintainability | Field set is small enough to apply manually |
| Authenticity | ClickUp remains execution state, not architecture truth |
| Observability | Status and review state are visible |
| Documentation | This file lives beside the integration spec |

## Machine Summary

```json
{
  "document": "clickup-fields",
  "version": "0.1.1",
  "required_fields": ["AKOS ID", "AKOS Type", "Title", "Status", "Owner", "Priority", "Source", "Review State"],
  "minimal_valid_item": ["title", "AKOS type", "source", "status", "owner or next action", "review state"]
}
```
