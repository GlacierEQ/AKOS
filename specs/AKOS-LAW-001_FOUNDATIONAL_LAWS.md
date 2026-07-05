# AKOS-LAW-001 — Foundational Laws

Version: 0.1.0
Status: Draft
Created: 2026-07-04

## Purpose

This specification defines the foundational laws of AKOS.

These laws guide all later specs, contracts, manifests, templates, audits, and runtime modules.

## LAW-001 — Identity

Every durable AKOS object should have one stable identity.

Names, aliases, and locations may change. Identity should remain stable.

## LAW-002 — Provenance

Every durable artifact should record where it came from.

If the source is unknown, the confidence should be lower.

## LAW-003 — Metadata

Durable objects need metadata before promotion.

At minimum: identity, type, title, version, status, source, and review state.

## LAW-004 — Structure

Knowledge should be shaped before it is automated.

Automation without structure creates drift.

## LAW-005 — History

History should be preserved.

When new work replaces old work, mark the older work historical instead of hiding it.

## LAW-006 — Review

Promotion requires review.

AKOS uses Pro-Code gates to review architecture and implementation.

## LAW-007 — One Truth, Many Views

A canonical artifact may be mirrored in more than one system.

The mirror should identify the source.

## LAW-008 — Spiral Engine

Each operating cycle should return with better structure, clearer metadata, and stronger continuity.

## Machine Summary

```json
{
  "spec": "AKOS-LAW-001",
  "version": "0.1.0",
  "status": "draft",
  "laws": [
    "identity",
    "provenance",
    "metadata",
    "structure",
    "history",
    "review",
    "one_truth_many_views",
    "spiral_engine"
  ]
}
```
