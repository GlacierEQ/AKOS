# AKOS Current State

Status: Active
Version: 0.1.1
Updated: 2026-07-04

## Purpose

This is the single read-first state file for AKOS sessions.

A future AKOS-aware session should read this file after `README.md`, `AKOS_MANIFEST.yaml`, and `BUILD_INDEX.md` before making changes.

## Canonical Repository

```text
GlacierEQ/AKOS
```

## Current Position

AKOS has moved from concept into repository-backed architecture.

The repo now contains root definitions, operating documents, foundational specs, connector discipline, handoff rules, and the first folder-based integration pack.

## Current Build Layer

Active layer:

```text
Connector-first implementation planning
```

This means connected systems must map back to AKOS object identity before automation expands.

## Locked Stack Priority

1. ClickUp
2. Supabase
3. Make
4. GitHub

## Active Read Path

Read in this order:

1. `README.md`
2. `AKOS_MANIFEST.yaml`
3. `BUILD_INDEX.md`
4. `CURRENT_STATE.md`
5. `docs/akos-operating-model.md`
6. `docs/stack-priority.md`
7. `docs/connector-registry.md`
8. Relevant integration spec

## Current Completed Pack

- Root README
- AKOS manifest
- Build index
- Governance seed
- Roadmap
- Operating model
- Stack priority
- Connector registry
- Handoff protocol
- APEX linkage
- Foundational laws
- Cognitive Kernel seed
- Canonical Object Model seed
- Metadata standard seed
- Repository contract seed
- Pro-Code seed
- Integration index
- Connector interface contract
- Connector readiness gates
- ClickUp folder pack

## ClickUp Integration Status

```text
Ready for Manual Test
```

Completed ClickUp files:

- `docs/integrations/clickup/README.md`
- `docs/integrations/clickup/ROLE.md`
- `docs/integrations/clickup/FIELDS.md`
- `docs/integrations/clickup/LISTS.md`
- `docs/integrations/clickup/MANUAL_TEST.md`
- `docs/integrations/clickup/READINESS_REVIEW.md`

## Open Loops

- Run ClickUp manual test and record result.
- Add integration specs for Supabase, Make, and GitHub.
- Add schemas for shared AKOS objects.
- Add templates for connector records.
- Add session ledger entries.
- Apply AKOS manifests to representative external repos.

## Highest-Leverage Next Action

Run the ClickUp manual test, then build the Supabase integration pack using the same folder-based pattern.

## Machine Summary

```json
{
  "document": "CURRENT_STATE",
  "version": "0.1.1",
  "status": "active",
  "current_layer": "connector-first implementation planning",
  "priority_order": ["ClickUp", "Supabase", "Make", "GitHub"],
  "clickup_status": "ready_for_manual_test",
  "highest_leverage_next_action": "run ClickUp manual test, then build Supabase integration pack"
}
```
