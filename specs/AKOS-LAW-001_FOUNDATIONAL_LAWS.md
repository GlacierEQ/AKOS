# AKOS-LAW-001 — Foundational Laws

Canonical ID: AKOS-LAW-001
Version: 0.1.1
Status: Active Draft
Created: 2026-07-04
Updated: 2026-07-04
Repository: GlacierEQ/AKOS
Path: specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md

## Purpose

This specification defines the foundational laws of AKOS.

These laws govern all later specs, contracts, manifests, templates, audits, runtime modules, and operational lanes.

## LAW-001 — Identity

Every durable AKOS object should have one stable identity.

Names, aliases, labels, and locations may change. Identity should remain stable.

## LAW-002 — Provenance

Every durable artifact should record where it came from.

If the source is unknown, confidence should be lower and promotion should be delayed.

## LAW-003 — Metadata

Durable objects need metadata before promotion.

Minimum metadata includes identity, type, title, version, status, source, path, confidence, and review state.

## LAW-004 — Structure Before Automation

Knowledge should be shaped before it is automated.

Automation without structure creates drift.

## LAW-005 — History Preservation

History should be preserved.

When new work replaces old work, mark the older work historical instead of hiding it.

## LAW-006 — Review Before Canon

Promotion requires review.

AKOS uses Pro-Code gates to review architecture and implementation.

## LAW-007 — One Truth, Many Views

A canonical artifact may be mirrored in more than one system.

Each mirror should identify its canonical source.

## LAW-008 — Spiral Engine

Each operating cycle should return with better structure, clearer metadata, stronger continuity, and fewer open loops.

## LAW-009 — Purpose Before Persona

Purpose precedes persona, tool selection, runtime style, and output format.

A system is shaped around its purpose first.

## LAW-010 — Excellent Operation

Excellent operation means making the next correct structural move, not the largest possible move.

AKOS prefers coherent, traceable, reviewable progress over scattered expansion.

## Machine Summary

```json
{
  "spec": "AKOS-LAW-001",
  "version": "0.1.1",
  "status": "active_draft",
  "laws": [
    "identity",
    "provenance",
    "metadata",
    "structure_before_automation",
    "history_preservation",
    "review_before_canon",
    "one_truth_many_views",
    "spiral_engine",
    "purpose_before_persona",
    "excellent_operation"
  ],
  "next_state": "bind laws into cognitive kernel, object model, metadata standard, repository contract, and Pro-Code methodology"
}
```
