# ClickUp Integration

Status: Active Draft
Version: 0.1.0
Created: 2026-07-04
Priority: 1

## Purpose

This folder defines the ClickUp integration for AKOS.

ClickUp is the execution visibility layer. It shows what work exists, what is waiting, what is under review, and what is complete.

## Boundary

ClickUp is not the source of truth for AKOS architecture.

AKOS architecture lives in GitHub. ClickUp records work that points back to GitHub, Notion, or another canonical source.

## Principle

No ClickUp task should exist as an isolated orphan when it represents AKOS work.

It should point back to a source file, source decision, source object, or source lane.

## Folder Files

- `ROLE.md`
- `FIELDS.md`
- `LISTS.md`
- `MANUAL_TEST.md`
- `READINESS_REVIEW.md`

## Current Status

Folder initialized. Implementation details are added in small files so each piece can be reviewed independently.
