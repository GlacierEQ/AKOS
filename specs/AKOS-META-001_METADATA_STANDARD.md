# AKOS-META-001 — Metadata Standard

Version: 0.1.0
Status: Active Seed
Created: 2026-07-04

## Purpose

The Metadata Standard defines the minimum fields required for AKOS artifacts.

## Required Fields

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
```

## Recommended Relationship Fields

```yaml
relationships:
  parents: []
  children: []
  depends_on: []
  derived_from: []
  supersedes: []
  superseded_by: []
  mirrors: []
```

## Status Values

- draft
- working
- reviewed
- canonical
- historical
- archived
- frozen

## Rule

No artifact should be promoted without metadata sufficient for future review.
