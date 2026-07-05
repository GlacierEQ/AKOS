# ClickUp Field Map

Status: Active Draft
Version: 0.1.0
Created: 2026-07-04

## Purpose

This file defines the minimum fields a ClickUp task should preserve when it represents AKOS work.

## Required Fields

| Field | Purpose |
|---|---|
| AKOS ID | Stable identifier when available |
| AKOS Type | Object category such as Task, Review, Project, or Open Loop |
| Source | Link or path to the origin of the work |
| Owner | Person or agent responsible for next action |
| Review State | Draft, Working, Review, Complete, Historical, or Blocked |
| Priority | Execution priority |
| Due Date | Time-sensitive deadline when applicable |

## Recommended Fields

| Field | Purpose |
|---|---|
| Related Object | Linked AKOS object or repo file |
| System | Source system or target system |
| Last Checked | Last review date |
| Blocker | Short blocker statement |
| Next Action | One concrete next step |

## Field Rule

A ClickUp task should preserve enough context that another operator can trace the task back to the source and understand what completion means.

## Minimal Valid Task

A minimal AKOS ClickUp task needs:

- title
- AKOS type
- source
- status
- next action

## Machine Summary

Document: ClickUp Field Map
Status: Active Draft
Required: AKOS ID, AKOS Type, Source, Owner, Review State, Priority, Due Date
