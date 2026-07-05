# AKOS-REPO-CONTRACT-001 — Repository Contract

Version: 0.1.0
Status: Active Seed
Created: 2026-07-04

## Purpose

This contract defines the minimum structure for an AKOS-compatible repository.

## Required Files

```text
README.md
AKOS_MANIFEST.yaml
CONTRACT.yaml
/docs/
/schemas/
/tests/
```

## Required Manifest Fields

```yaml
canonical_id:
family_id:
name:
version:
status:
purpose:
repository:
primary_layer:
quality_gates: []
```

## Pro-Code Binding

Every compatible repository should be reviewable under `AKOS-PROCODE-001`.

## Promotion Rule

A repository should not be marked canonical until its manifest, contract, documentation, and Pro-Code review are complete or explicitly waived.
