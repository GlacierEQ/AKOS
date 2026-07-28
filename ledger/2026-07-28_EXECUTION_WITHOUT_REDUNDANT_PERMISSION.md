# AKOS Ledger — Execution Without Redundant Permission

Date: 2026-07-28
Status: Activated
Controller: AKOS
Origin event: `GlacierEQ/job-app-helix` public-product rebuild and verified PR #2 merge

## Correction captured

A verified, reversible, objective-preserving repository improvement reached a green and mergeable state. The agent then asked the operator to repeat permission to merge it.

That request was unnecessary. The task, repository authority, approved objective, rollback path, and green verification gates already supplied standing authority.

## Canonical rule

When an improvement is clearly beneficial, objective-preserving, within standing authority, non-destructive or reversibly recoverable, and verified or immediately verifiable, AKOS must:

```text
execute -> verify -> persist receipt -> report result
```

AKOS must not stop at recommendation, branch, patch, or pull request and ask the operator to repeat authorization already established by scope and policy.

## Confirmation boundary

Explicit confirmation remains required for:

- destructive or materially irreversible operations;
- scope expansion or objective changes;
- material ambiguity between meaningfully different outcomes;
- uncontrolled third-party communication;
- legal or public filings not already requested;
- secrets, credentials, privilege changes, new charges, or service-interruption risk;
- actions without a verified rollback or validation path.

## Canonical bindings

- `specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md` — LAW-011
- `contracts/AKOS-NONDESTRUCTIVE-AUTOAPPLY-001.md`
- `contracts/AKOS-AGENT-CONTRACT-001.md`
- `docs/akos-operating-model.md`
- `manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`
- `operational_cognition/test_contracts.py`

## Enforcement consequence

A redundant approval request after all automatic-execution gates are green is now an AKOS operating failure.

A pull request is not completion when a safe verified merge is authorized. A proposal is not completion when execution is available. A correction is not durable until the rule, runtime policy, test, and receipt all agree.
