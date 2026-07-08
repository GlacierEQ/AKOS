# AKOS Operational Readiness Review

Status: Active Draft
Version: 0.1.0
Created: 2026-07-07

## Purpose

This document defines how AKOS decides whether a connector, automation, schema, or runtime process is ready for operational use.

## Review Rule

Operational readiness is not a vibe.

It is a recorded state supported by evidence from manual use, validation, failure handling, and review.

## Required Review Sections

Each readiness review should include:

- artifact name
- artifact type
- owner or actor
- source
- target system
- current readiness level
- requested readiness level
- test history
- known limitations
- failure modes
- rollback or recovery path
- next action

## Readiness Questions

1. What problem does this solve?
2. What source does it depend on?
3. What system does it affect?
4. What is the smallest tested action?
5. What has been proven manually?
6. What has not been proven?
7. What could fail silently?
8. How would we know?
9. Where is the result recorded?
10. What must happen before automation?

## Operational Use Requirements

Before operational use, AKOS needs:

- manual test pass
- validation record
- known limitation record
- failure mode record
- next action record
- ledger entry

## Automation Use Requirements

Before automation, AKOS also needs:

- repeatable manual path
- duplicate handling
- stale-state handling
- sync direction rule
- stop rule
- recovery rule
- monitoring path

## Current Example

ClickUp is ready for manual use after the first manual test passed.

ClickUp is not ready for automation because native custom fields, duplicate handling, stale handling, sync rules, and recovery rules are not complete.

## Machine Summary

```json
{
  "document": "operational-readiness-review",
  "version": "0.1.0",
  "manual_use_requires": ["manual test pass", "validation record", "limitations", "failure modes", "next action", "ledger entry"],
  "automation_requires": ["repeatable manual path", "duplicate handling", "stale handling", "sync direction", "stop rule", "recovery rule", "monitoring path"]
}
```
