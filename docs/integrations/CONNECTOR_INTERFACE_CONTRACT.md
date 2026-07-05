# AKOS Connector Interface Contract

Status: Active Draft
Version: 0.1.0
Created: 2026-07-04

## Purpose

This contract defines the minimum standard for connecting AKOS to another system.

It exists so external tools do not fragment AKOS identity, status, review state, or source discipline.

## Connector Law

A connector is a surface, not the canon.

Every connector should either point to a canonical AKOS record or clearly state that it is holding draft operational state.

## Minimum Connector Record

Every connected record should preserve:

- canonical ID when available
- AKOS object type
- title
- status
- owner
- source system
- source location
- target system
- target location
- last updated date
- review state

## Required Connector Behavior

A connector should support five behaviors:

1. Create a mapped record.
2. Read the mapped record.
3. Update status without losing identity.
4. Link back to the canonical source.
5. Flag stale or incomplete records.

## Drift Rule

When a connected record diverges from the canonical source, the connector should not silently overwrite either side.

It should create a review item or record a sync note.

## Promotion Rule

A connected record cannot promote itself to canonical.

Canonical promotion happens through AKOS governance and Pro-Code review.

## Quality Gates

Every connector must pass:

- Naming
- Architecture
- Failure Handling
- Maintainability
- Authenticity
- Observability
- Documentation

## Machine Summary

Document: CONNECTOR_INTERFACE_CONTRACT
Version: 0.1.0
Status: Active Draft
Role: shared connector standard
