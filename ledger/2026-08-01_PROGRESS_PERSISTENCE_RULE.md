# Progress Persistence Rule — AKOS Governance Delta

- **Canonical ID:** `AKOS-LEDGER-2026-08-01-PROGRESS-PERSISTENCE`
- **Date:** 2026-08-01
- **Status:** `active_draft`
- **Repository:** `GlacierEQ/AKOS`
- **Change type:** governance rule and manifest principle

## Purpose

Promote the progress-persistence requirement into AKOS so completed or
materially blocked work is not left as disconnected reports. The rule requires
applicable detailed, machine-readable, ledger/index, and backlog/source-pointer
records to be updated in the same pass.

## Canonical changes

- `GOVERNANCE.md` now contains the **Progress Persistence Rule**.
- `AKOS_MANIFEST.yaml` now declares `progress_persistence_across_views`.
- This append-only ledger entry records the promotion and its boundaries.

## Boundaries

- AKOS owns the governance rule; it does not become the owner of case facts or
  evidence originals.
- `GlacierEQ/monolith` remains the cartographic map and points to AKOS rather
  than duplicating AKOS governance.
- A layer that is not applicable, blocked, or deferred must say so explicitly;
  absence is not completion.

## Verification

- Existing AKOS governance and manifest were inspected before modification.
- The change is additive and preserves historical records.
- The target repository uses direct-to-`main` operation under its manifest.
- Post-commit provider receipt and validation remain required by AKOS policy.
