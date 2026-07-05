# AKOS-COM-001 — Canonical Object Model

Version: 0.1.0
Status: Active Seed
Created: 2026-07-04

## Purpose

The Canonical Object Model defines the durable object types AKOS can store, relate, version, and promote.

## Core Rule

Every durable object needs identity, type, status, source, confidence, relationships, and version context.

## Object Types

- Actor
- Event
- Evidence
- Claim
- Project
- Repository
- Prompt
- Automation
- Conversation
- Decision
- Document
- System
- Gene
- Synapse
- Pillar
- Piston
- Contract
- Manifest
- Schema
- Ledger Entry

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

## Promotion Rule

An object becomes canonical only when it has stable identity, purpose, source, relationship context, and review status.
