# Finisher Action-Boundary Migration Receipt

**Date:** 2026-07-30  
**Repository:** `GlacierEQ/AKOS`  
**Decision:** Preserve repository-local Finisher verification; retire secret-bearing cross-repository execution from AKOS Actions.

## Previous state

`.github/workflows/finisher.yml` exposed a manual `scan`, `gate`, or `apply` workflow and consumed `FINISHER_GITHUB_TOKEN` to operate on allowlisted private repositories.

That implementation conflicted with the current public-action-face architecture:

- AKOS is public and owns policy, contracts, tests, and read-only local verification.
- Governed execution against private repositories belongs to `GlacierEQ/public-actions-runner-host` or another explicitly authorized private execution plane.
- Public workflows must not consume private workload tokens or persist checkout credentials.

## Migration

The workflow now:

1. runs only for Finisher source or workflow changes;
2. declares `permissions: contents: read`;
3. checks out only AKOS with `persist-credentials: false`;
4. compiles the Finisher package;
5. runs the local Finisher test module;
6. contains no secret, manual apply input, cross-repository checkout, or mutation path.

The Finisher runtime and configuration remain in AKOS as governed policy and executable logic. Only the GitHub Actions execution authority moved to the correct plane.

## Verification

The migration is enforced by `operational_cognition/test_contracts.py`, which examines every repository workflow and requires:

- exact read-only contents permission;
- nonpersistent checkout credentials;
- repository-local checkout only;
- no `pull_request_target`;
- no `workflow_call` execution surface;
- no private or control token references.

The dedicated Finisher verification workflow and the full AKOS verification matrix both passed after this change.

## Rollback

Rollback must not restore a secret-bearing workflow to AKOS. A future execution path must be implemented in the governed private action face and linked back through a provider receipt.
