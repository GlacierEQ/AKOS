# CASEBRAIN AKOS Orchestration Audit — 2026-07-15

## Decision

AKOS is the sole orchestration and governance control plane for CASEBRAIN connector operations.

## Existing foundation confirmed

- PR #1 merged the truth-safe CASEBRAIN powerup federation, repository contracts, worker gates, and registry.
- PR #2 promoted exact merged source receipts while preserving activation gates.
- GitHub remains code and contract canon.
- CASEBRAIN is the validated knowledge and case graph.
- Notion and ClickUp remain projections and execution surfaces, not competing truth stores.

## Durable artifacts now bound into AKOS

- `architecture/federation-contract.md`
- `schemas/canonical/casebrain-object.schema.json`
- `supabase/migrations/0001_casebrain_core.sql`
- `config/casebrain-connectors.json`
- `manifests/runtime/CASEBRAIN_CONNECTOR_ORCHESTRATION.json`

## Connector state observed

| Connector | State | AKOS handling |
|---|---|---|
| GitHub | Connected and writable | Canonical commits and receipts |
| Notion | Connected | Reviewed projection only |
| ClickUp | Connected; comment action inconsistent | Execution anchor preserved; no false completion |
| Supabase | No visible project | Blocked pending organization, cost confirmation, and project selection |
| Google Drive | Connected; intake root not designated | Read-only until exact allowlisted root |
| Dropbox | Connected; intake root not designated | Read-only until exact allowlisted root |

## Non-negotiable gates

- No evidence mutation before an approved preview.
- No automatic filing, service, publication, or external communication.
- No legal fact promotion without source anchors and verification state.
- No silent database provisioning or billable operation.
- No filename-only identity.
- No conflict flattening.
- Every approved write must be idempotent and emit an append-only receipt.

## Next executable slice

1. Obtain exact Google Drive and Dropbox intake roots.
2. Perform read-only inventory and SHA-256 fingerprinting.
3. Select one primary record for `1FDV-23-0001009`.
4. Generate a `CASE_EVENT` candidate with page-level provenance.
5. Validate it against the canonical schema.
6. Emit a preview and wait for explicit apply approval.
7. After Supabase is selected, apply `0001_casebrain_core.sql`, run security and performance advisors, and register the validated object plus receipt.

## Result

The federation is no longer an abstract design. AKOS now contains the contracts, object schema, database migration, connector registry, runtime orchestration manifest, and immutable implementation audit needed to drive the first governed case slice.
