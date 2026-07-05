# AKOS-COM-001 — Canonical Object Model

Canonical ID: AKOS-COM-001
Version: 0.1.1
Status: Active Draft
Created: 2026-07-04
Updated: 2026-07-04
Repository: GlacierEQ/AKOS
Path: specs/AKOS-COM-001_CANONICAL_OBJECT_MODEL.md
Depends On: AKOS-LAW-001, AKOS-CK-001

## Purpose

The Canonical Object Model defines the durable object types AKOS can store, relate, version, review, and promote.

The Cognitive Kernel defines how knowledge moves. The Canonical Object Model defines what durable objects exist.

## Core Rule

Every durable object needs identity, type, status, source, confidence, relationships, and version context.

## Object Types

| Type | Purpose |
|---|---|
| Actor | Person, organization, agent, or system participant |
| Event | Time-bounded occurrence or milestone |
| Evidence | Source artifact used for support or context |
| Claim | Assertion requiring confidence and review |
| Project | Coordinated body of work |
| Repository | Code or documentation repository |
| Prompt | Reusable instruction artifact |
| Automation | Scheduled or triggered process |
| Conversation | Recursive thread or operational lane |
| Decision | Recorded choice with rationale |
| Document | Durable authored artifact |
| System | Integrated architecture or platform |
| Gene | Modular capability |
| Synapse | Relationship or interface |
| Pillar | Load-bearing constraint |
| Piston | Repeatable processing cycle |
| Contract | Compatibility or interface requirement |
| Manifest | Metadata declaration |
| Schema | Machine-readable structure |
| Ledger Entry | Append-only record of change or movement |

## Universal Envelope

```yaml
canonical_id:
type:
title:
summary:
version:
status:
created_at:
updated_at:
source:
repository:
path:
confidence:
verification_status:
relationships: {}
metadata: {}
```

## Relationship Verbs

- depends_on
- derived_from
- supersedes
- superseded_by
- mirrors
- synchronizes_with
- implements
- governs
- references
- contains
- belongs_to

## Lifecycle States

- seed
- draft
- active_draft
- working_canonical
- canonical
- historical
- archived

## Promotion Rule

An object becomes canonical only when it has stable identity, purpose, source, relationship context, metadata, and review status.

## Machine Summary

```json
{
  "spec": "AKOS-COM-001",
  "version": "0.1.1",
  "status": "active_draft",
  "object_model": "durable nouns of AKOS",
  "next_state": "bind object envelope to metadata schema and templates"
}
```
