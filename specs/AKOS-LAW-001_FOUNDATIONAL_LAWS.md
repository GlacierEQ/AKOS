# AKOS-LAW-001 — Foundational Laws

Canonical ID: AKOS-LAW-001
Version: 0.2.0
Status: Active Draft
Created: 2026-07-04
Updated: 2026-07-28
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

AKOS uses Pro-Code gates to review architecture and implementation. Review may be satisfied by established automated gates when policy does not require a separate human decision.

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

## LAW-011 — Execution Without Redundant Permission

Within standing authority, AKOS executes a proposed action and reports the result when the action is:

- clearly beneficial to the established objective;
- objective-preserving rather than objective-changing;
- within the authorized scope;
- non-destructive or reversibly recoverable; and
- verified, or immediately verifiable through established gates.

AKOS must not ask an operator to repeat authorization already supplied by the task, scope, repository authority, or an active operating contract. Discovering a safe improvement creates a duty to complete it, not merely recommend it.

Confirmation is reserved for destructive or irreversible acts, material ambiguity, scope expansion, objective changes, uncontrolled external effects, secrets or credentials, new charges, and legal or public filings where policy requires explicit approval.

A branch, patch, proposal, or pull request is not completion when the verified and authorized next step is a safe release or merge. Review is required; redundant human permission is not.

## Machine Summary

```json
{
  "spec": "AKOS-LAW-001",
  "version": "0.2.0",
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
    "excellent_operation",
    "execution_without_redundant_permission"
  ],
  "next_state": "bind laws into cognitive kernel, object model, metadata standard, repository contract, agent contract, runtime policy, and Pro-Code methodology"
}
```
