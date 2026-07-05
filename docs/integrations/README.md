# AKOS Integrations

Status: Active Draft
Version: 0.1.0
Created: 2026-07-04

## Purpose

This folder defines how AKOS connects to external systems without losing canonical identity, provenance, review status, or source-of-truth discipline.

## Priority Order

1. ClickUp
2. Supabase
3. Make
4. GitHub

## Integration Rule

An integration should not create structure on its own.

It should map an AKOS object into another system while preserving identity, status, source, and review context.

## Files

| File | Role |
|---|---|
| `clickup.md` | Task and execution-state integration |
| `supabase.md` | Structured data integration |
| `make.md` | Automation and routing integration |
| `github.md` | Canonical architecture and version integration |

## Shared Mapping Fields

```yaml
canonical_id:
akos_type:
title:
status:
source_system:
source_location:
target_system:
target_location:
owner:
updated_at:
review_status:
related_objects: []
```

## Machine Summary

```json
{
  "folder": "docs/integrations",
  "version": "0.1.0",
  "priority_order": ["ClickUp", "Supabase", "Make", "GitHub"]
}
```
