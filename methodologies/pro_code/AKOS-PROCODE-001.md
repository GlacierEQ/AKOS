# AKOS-PROCODE-001 — Pro-Code Methodology

Canonical ID: AKOS-PROCODE-001
Version: 0.2.0
Status: Active Draft
Created: 2026-07-04
Updated: 2026-07-04
Repository: GlacierEQ/AKOS
Path: methodologies/pro_code/AKOS-PROCODE-001.md
Depends On: AKOS-LAW-001, AKOS-CK-001, AKOS-COM-001, AKOS-META-001

## Purpose

Pro-Code is the AKOS quality methodology.

It prevents architecture from remaining only conceptual by requiring artifacts to pass disciplined review gates before promotion.

## Core Rule

No artifact is canonical until it is reviewable.

No artifact is elite until it can survive chunked construction, gate review, and future maintenance.

## Seven Gates

| Gate | Review Question |
|---|---|
| Naming | Is the artifact named clearly? |
| Architecture | Are boundaries and interfaces clear? |
| Failure Handling | Are failure paths considered? |
| Maintainability | Can a future operator understand it? |
| Authenticity | Does it honestly match its stated purpose? |
| Observability | Can status and health be inspected? |
| Documentation | Does the documentation live with the work? |

## Chunk Power

Chunk Power is the Pro-Code execution method for building complex AKOS systems without drift.

A chunk is the smallest coherent unit of build work that can be reviewed, committed, and understood independently.

## Chunk Rules

1. One chunk should have one primary purpose.
2. One chunk should produce one inspectable delta.
3. One chunk should be small enough to review fully.
4. One chunk should pass Pro-Code gates before promotion.
5. One chunk should leave the system more navigable than before.
6. One chunk should never hide uncertainty.
7. One chunk should record what changed and why.

## Chunk Lifecycle

```text
Select
Scope
Build
Review
Commit
Record
Promote or Hold
```

## Chunk Types

| Type | Purpose |
|---|---|
| spec_chunk | Adds or improves a formal specification |
| contract_chunk | Adds or improves a compatibility contract |
| schema_chunk | Adds or improves machine-readable structure |
| manifest_chunk | Adds or improves metadata declarations |
| audit_chunk | Reviews artifact quality |
| adoption_chunk | Adds AKOS compatibility to another repo |
| cleanup_chunk | Clarifies, deduplicates, or marks historical material |
| ledger_chunk | Records movement, promotion, or synchronization |

## Elite Build Standard

Elite AKOS build means:

- inspect first
- avoid duplicate canon
- build in coherent chunks
- preserve history
- mark uncertainty
- bind work to metadata
- pass Pro-Code gates
- commit with traceable purpose
- promote only after review

## Promotion Levels

| Level | Meaning |
|---|---|
| Draft | Created but not reviewed |
| Gate Checked | Reviewed against Pro-Code gates |
| Working Canonical | Operationally accepted but evolving |
| Canonical | Current source of truth |
| Historical | Superseded but preserved |

## Machine Summary

```json
{
  "spec": "AKOS-PROCODE-001",
  "version": "0.2.0",
  "status": "active_draft",
  "method": "Pro-Code plus Chunk Power",
  "gates": [
    "naming",
    "architecture",
    "failure_handling",
    "maintainability",
    "authenticity",
    "observability",
    "documentation"
  ],
  "chunk_lifecycle": [
    "select",
    "scope",
    "build",
    "review",
    "commit",
    "record",
    "promote_or_hold"
  ],
  "next_state": "create chunk template and build ledger format"
}
```
