# Failure and Reconciliation Rule — AKOS Governance Delta

- **Canonical ID:** `AKOS-LEDGER-2026-08-01-FAILURE-RECONCILIATION`
- **Date:** 2026-08-01
- **Status:** `active_draft`
- **Repository:** `GlacierEQ/AKOS`
- **Change type:** failure handling and completion-state clarification
- **Related rule:** `AKOS-LEDGER-2026-08-01-PROGRESS-PERSISTENCE`

## Purpose

Close the principal ambiguity in progress persistence: a task cannot be
reported as complete when one required record layer is missing, stale,
contradictory, or unverified. The rule makes blocked and failed work visible
and gives later reconciliation a preserved, auditable path.

## Canonical changes

- `GOVERNANCE.md` now defines explicit operation states and reconciliation
  requirements.
- `AKOS_MANIFEST.yaml` now declares failure reconciliation, no silent
  completion, required record layers, and cross-view verification.
- This append-only entry records the change without replacing the prior
  progress-persistence entry.

## Required behavior

- Missing or unupdatable layers produce an explicit
  `reconciliation_required` state.
- Original records are preserved; later corrections are dated and identify the
  changed fields, evidence, and final disposition.
- Conflicting views are not silently overwritten.
- Completion requires a final cross-view check.

## Boundaries

- This rule governs work-state reporting and record integrity; it does not
  create case facts or authenticate evidence originals.
- `GlacierEQ/monolith` remains a map that points to AKOS rather than a second
  governance authority.

## Verification

- Existing governance, manifest, and prior ledger entry were inspected before
  modification.
- The change is additive and preserves the prior append-only record.
- The target repository continues to use direct-to-`main` operation under its
  manifest.
- Post-commit provider receipt and cross-file validation remain required.
