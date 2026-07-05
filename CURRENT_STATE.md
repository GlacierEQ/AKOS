# AKOS Current State

Status: Active
Version: 0.1.0
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

The repo now contains root definitions, operating documents, foundational specs, connector discipline, and handoff rules.

## Current Build Layer

Active layer:

```text
Connector-first implementation planning
```

This means the next build work should define how connected systems map to AKOS objects before automations are created.

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

## Open Loops

- Add integration specs for ClickUp, Supabase, Make, and GitHub.
- Add schemas for shared AKOS objects.
- Add templates for connector records.
- Add session ledger entries.
- Apply AKOS manifests to representative external repos.

## Highest-Leverage Next Action

Finish the `docs/integrations/` folder, then create templates for shared object mapping.

## Machine Summary

```json
{
  "document": "CURRENT_STATE",
  "version": "0.1.0",
  "status": "active",
  "current_layer": "connector-first implementation planning",
  "priority_order": ["ClickUp", "Supabase", "Make", "GitHub"],
  "highest_leverage_next_action": "finish docs/integrations and object mapping templates"
}
```
