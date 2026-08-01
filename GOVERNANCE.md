# AKOS Governance

Canonical ID: AKOS-GOV-001
Status: Active Draft
Version: 0.3.0
Created: 2026-07-04
Updated: 2026-08-01
Repository: GlacierEQ/AKOS

## Purpose

This file defines how AKOS architecture files are created, reviewed, executed, promoted, superseded, and preserved.

## Excellent Operation Standard

AKOS is built through disciplined operation:

1. Inspect before changing.
2. Update existing canonical files before creating replacements.
3. Create new files only when no canonical file exists.
4. Preserve historical files unless there is explicit reason to remove them.
5. Record deltas rather than overwriting context.
6. Promote only stable, reviewed artifacts.
7. Prefer small, traceable commits.
8. Execute safe verified improvements without redundant permission.
9. Continue through authorized release instead of stopping at a proposal.
10. Ask only when a defined confirmation trigger exists.

## Default Execution Authority

When an action is clearly beneficial, objective-preserving, within standing authority, non-destructive or recoverable, and verified or immediately verifiable, AKOS must:

```text
execute -> verify -> persist -> release when authorized -> report
```

AKOS must not ask the operator to repeat authorization already supplied by the task, objective, repository authority, connected-system permissions, or an active AKOS contract.

Confirmation is reserved for destructive or irreversible acts, material ambiguity, scope expansion, objective changes, uncontrolled external effects, legal or public filings not already requested, secrets or credentials, new charges, service interruption, or missing rollback and verification paths.

A pull request is not completion when a safe verified merge is authorized.

Canonical implementation:

- `specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md` — LAW-011
- `contracts/AKOS-NONDESTRUCTIVE-AUTOAPPLY-001.md`
- `contracts/AKOS-AGENT-CONTRACT-001.md`
- `specs/AKOS-OC-001A_EXECUTION_AUTHORITY_ADDENDUM.md`
- `operational_cognition/execution_authority.py`

## Source of Truth

`GlacierEQ/AKOS` is the canonical source for AKOS architecture.

Other systems may mirror or summarize AKOS, but mirrors should point back to this repository.

Historical bootstrap material in other repositories may be referenced, but it is not canonical unless promoted here.

## Status Values

| Status | Meaning |
|---|---|
| seed | Captured starting point |
| draft | Structured but not reviewed |
| active_draft | In use but still evolving |
| working_canonical | Operationally accepted pending final review |
| canonical | Current source of truth |
| historical | Superseded but preserved |
| archived | Retained only for reference |

## Promotion Requirements

A file should not become canonical unless it has:

- clear name;
- canonical ID where appropriate;
- version;
- status;
- purpose;
- owner or source;
- review state;
- relationship to the AKOS stack;
- path in the repository;
- Pro-Code review or waiver where applicable;
- validation and rollback evidence for executable changes.

Review may be satisfied by established automated gates when no confirmation trigger requires a separate human decision.

## Pro-Code Gates

AKOS review uses seven gates:

- Naming
- Architecture
- Failure Handling
- Maintainability
- Authenticity
- Observability
- Documentation

## Change Rule

Before modifying AKOS:

1. Read `README.md`.
2. Read `AKOS_MANIFEST.yaml`.
3. Read `BUILD_INDEX.md`.
4. Read the file being changed.
5. Apply the smallest coherent improvement.
6. Verify the changed state.
7. Complete any safe authorized release.
8. Record the result in the relevant ledger, session note, or build index.
9. Report the completed result and remaining risk.

## Progress Persistence Rule

For every completed or materially blocked operation, update each applicable
record layer in the same pass:

1. the detailed report or canonical artifact;
2. the machine-readable manifest, receipt, or verification record;
3. the relevant append-only ledger, session note, or build index; and
4. the source inventory, backlog, or next-action pointer.

A result is not persisted as complete until the applicable layers are updated,
or an explicit `not_applicable`, `blocked`, or `deferred` state records why a
layer could not be updated. Records must distinguish completed, verified,
blocked, deferred, and proposed work. A view may summarize the canonical
record, but it may not silently replace it.

## Historical Preservation Rule

Historical files are not deleted simply because they are imperfect.

They should be marked historical, linked to their replacement, and preserved for provenance.

## Canonical Rule

One truth may have many views. The canonical source must be explicit.
