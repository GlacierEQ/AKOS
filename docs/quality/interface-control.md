# AKOS Interface Control Standard

Status: Active Draft
Version: 0.1.0
Created: 2026-07-07

## Purpose

This document defines how AKOS controls boundaries between systems.

A system can only be trusted when its authority, input, output, and limits are explicit.

## Core Rule

Every interface must preserve identity and source.

## Interface Record

Each AKOS interface should define:

- source system
- target system
- object type
- input fields
- output fields
- owner or actor
- allowed actions
- blocked actions
- validation method
- ledger requirement

## Current System Boundaries

| System | Role | Canonical Authority |
|---|---|---|
| GitHub | Architecture, specs, contracts, schemas, templates, ledger | Yes |
| ClickUp | Execution visibility and task state | No |
| Notion | Dashboard and navigation mirror | No |
| Supabase | Structured data after schema approval | Partial, only for approved tables |
| Make | Automation routing after contract approval | No |

## Blocked Interface Behavior

Do not allow:

- ClickUp to overwrite GitHub canon
- Notion to become source of truth by accident
- Make to automate before stop rules exist
- Supabase to store undefined object types
- any connector to create orphan records

## Interface Validation

An interface passes when:

- input source is known
- target system is known
- object type is known
- allowed actions are known
- blocked actions are known
- result can be validated
- ledger path is known

## Machine Summary

```json
{
  "document": "interface-control",
  "version": "0.1.0",
  "core_rule": "every interface must preserve identity and source",
  "canonical_system": "GitHub"
}
```
