# AKOS Stack Priority

Status: Active Draft
Version: 0.1.0
Created: 2026-07-04

## Purpose

This file locks the current implementation order so AKOS does not sprawl into disconnected tooling.

## Current Priority Order

1. ClickUp
2. Supabase
3. Make
4. GitHub

## Why This Order

ClickUp comes first because execution needs visible task state.

Supabase comes second because durable structured records need a stable data layer.

Make comes third because automation should connect already-defined objects, not invent structure.

GitHub remains the architecture source of truth and implementation record.

## Vector Tiering

AKOS should distinguish between storage and retrieval tiers.

| Tier | Role |
|---|---|
| Hot | Current operational context |
| Warm | Active projects and recurring lanes |
| Cold | Historical reference |
| Frozen | Immutable canonical or archival record |

## Implementation Rule

Do not automate a workflow until its object type, metadata, owner, and review path are clear.

## Machine Summary

```json
{
  "document": "stack-priority",
  "version": "0.1.0",
  "priority_order": ["ClickUp", "Supabase", "Make", "GitHub"],
  "vector_tiers": ["hot", "warm", "cold", "frozen"]
}
```
