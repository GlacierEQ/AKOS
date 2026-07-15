# CASEBRAIN Federation Contract

Status: active
Version: 1.0.0
Effective: 2026-07-15

## Purpose
CASEBRAIN is a federated legal knowledge system. Each connected platform has one authoritative responsibility. Cross-system copies are projections and must preserve stable IDs, source pointers, hashes, verification state, and synchronization receipts.

## System authority
- GitHub: schemas, migrations, adapters, prompts, tests, architecture decisions, and automation canon.
- Supabase: canonical operational records, relationships, connector state, and append-only audit receipts.
- Notion: reviewed human-facing dashboards and command projections.
- ClickUp: execution, approvals, blockers, and delivery state.
- Drive and Dropbox: original evidence objects and immutable source files.

## Core invariants
1. Every canonical object receives a stable `CBR-<TYPE>-<ULID>` identifier.
2. Evidence is never silently moved, renamed, overwritten, transformed, or deleted.
3. Every extracted statement preserves source URI, SHA-256, page or line anchor, extraction method, and verification state.
4. Contradictions are modeled as first-class records; they are never flattened into a single narrative.
5. Connector writes are idempotent and emit append-only receipts.
6. Notion and ClickUp contain projections plus canonical IDs, never competing truth stores.
7. Destructive, public, filing, or evidence-changing actions require human approval.
8. Every sync must be reversible or explicitly marked irreversible before approval.

## Canonical object types
`case`, `actor`, `event`, `evidence`, `claim`, `contradiction`, `authority`, `filing`, `task`, `relationship`, `connector_object`, `sync_run`, `sync_receipt`, `verification_event`.

## Required provenance
Each evidence-derived record must include:
- `casebrain_id`
- `case_id`
- `source_system`
- `source_uri`
- `source_object_id`
- `sha256`
- `page_start` / `page_end` or equivalent line/time anchors
- `extraction_method`
- `verification_status`
- `created_at`
- `updated_at`

## Synchronization contract
Each connector operation must use an idempotency key derived from:
`operation_type + canonical_id + target_system + target_parent + payload_hash`.

Each operation emits a receipt containing request hash, result status, remote object ID, remote URL, prior state pointer when available, timestamp, and error details when applicable.

## First governed slice
The first production reconciliation slice is case `1FDV-23-0001009`. It must remain read-only until source roots, identity crosswalks, and evidence hashing are approved.