# AKOS Connector Registry

Status: Active Draft
Version: 0.2.0
Created: 2026-07-04
Updated: 2026-07-26

## Purpose

The connector registry defines how AKOS names and governs connected systems.

A connector is not automatically canonical. A connector is an execution or storage surface that must map back to AKOS object identity.

## Connector ID Model

```text
CONN-<SYSTEM>-<NUMBER>
```

Examples:

```text
CONN-CLICKUP-001
CONN-SUPABASE-001
CONN-MAKE-001
CONN-GITHUB-001
CONN-NOTION-001
CONN-KIMI-001
```

## Priority Connectors

| Priority | Connector | Role |
|---|---|---|
| 1 | ClickUp | Task and execution state |
| 2 | Supabase | Structured data layer |
| 3 | Make | Automation layer |
| 4 | GitHub | Architecture and version source |
| 5 | Notion | Dashboard and navigation mirror |

## Implemented Edge Connectors

| Connector ID | Connector | Role | Canonical authority | Readiness |
|---|---|---|---|---|
| `CONN-KIMI-001` | Kimi Portable Memory Adapter | External-agent memory import and portability | no | Ready for Manual Test |

## Shared Object Fields

Every connector should preserve or map:

```yaml
canonical_id:
type:
title:
status:
source_system:
source_location:
updated_at:
owner:
related_objects: []
review_status:
```

## Connector Rules

- Never let a connector define truth by accident.
- Every mirrored object should point back to its canonical source.
- Every automation should preserve object identity.
- Every sync should record source and target location.
- Every connector failure should be visible in review.

## Machine Summary

```json
{
  "document": "connector-registry",
  "version": "0.2.0",
  "priority_connectors": ["ClickUp", "Supabase", "Make", "GitHub", "Notion"],
  "implemented_edge_connectors": ["CONN-KIMI-001"]
}
```
