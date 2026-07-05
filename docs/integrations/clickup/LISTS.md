# ClickUp List Structure

Status: Active Draft
Version: 0.1.1
Created: 2026-07-04
Updated: 2026-07-05

## Purpose

This file defines the starting ClickUp structure for AKOS execution visibility.

The structure should be simple enough to use immediately and strict enough to prevent tool sprawl.

## Starting Folder

Recommended folder name:

```text
AKOS
```

## Starting Lists

| List | Role |
|---|---|
| AKOS Foundation | Core repo, specs, governance, roadmap, current state |
| AKOS Integrations | ClickUp, Supabase, Make, GitHub connector work |
| AKOS Repo Adoption | Applying AKOS manifests and contracts to external repos |
| AKOS Review Queue | Items needing Pro-Code or human review |
| AKOS Backlog | Valid but unscheduled work |

## Status Set

Use a simple status set first:

- Draft
- Ready
- In Progress
- Review
- Blocked
- Complete
- Historical

## Naming Rule

Task names should start with the object or system being changed.

Examples:

- AKOS: finalize Current State boot file
- ClickUp: create required custom fields
- Supabase: draft object table schema
- Repo Adoption: add manifest to spacex-telemetry

## First Tasks

Create these first:

1. ClickUp: create AKOS folder and lists
2. ClickUp: add custom fields
3. AKOS: map open loops from CURRENT_STATE
4. AKOS: create first review queue item
5. AKOS: record manual test result in GitHub

## List Ownership Rule

Each list must represent one operational purpose.

Do not create a new list when a task can be classified by field, status, or priority.

## Pro-Code Check

| Gate | Result |
|---|---|
| Naming | List names are plain and system-scoped |
| Architecture | Folder/list split is simple |
| Failure Handling | Backlog and Blocked states prevent silent loss |
| Maintainability | Five starting lists are enough for manual operation |
| Authenticity | Lists match AKOS execution needs |
| Observability | Review and Blocked states are visible |
| Documentation | Structure is documented before automation |

## Machine Summary

```json
{
  "document": "clickup-lists",
  "version": "0.1.1",
  "folder": "AKOS",
  "lists": ["AKOS Foundation", "AKOS Integrations", "AKOS Repo Adoption", "AKOS Review Queue", "AKOS Backlog"],
  "status_set": ["Draft", "Ready", "In Progress", "Review", "Blocked", "Complete", "Historical"]
}
```
