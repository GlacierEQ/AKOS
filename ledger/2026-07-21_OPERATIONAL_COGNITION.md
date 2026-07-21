# AKOS Operational Cognition Build Receipt

**Date:** 2026-07-21  
**Canonical ID:** AKOS-OC-001  
**Branch:** `akos-operational-cognition-2026-07-21`  
**Status:** implemented on branch; promotion pending CI and connector receipts

## Objective

Convert the comparative analysis of tool power, tool literacy, orchestration,
verification, persistence and execution continuity into executable AKOS
operational cognition.

## Changed State

Created:

- `operational_cognition/__init__.py`
- `operational_cognition/engine.py`
- `operational_cognition/test_engine.py`
- `operational_cognition/README.md`
- `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md`
- `schemas/operational_cognition.schema.json`
- `manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`
- `.github/workflows/operational-cognition.yml`

Updated:

- `README.md`
- `AKOS_MANIFEST.yaml`
- `BUILD_INDEX.md`
- `CURRENT_STATE.md`

## Runtime Capabilities

The implementation now provides:

1. authoritative capability selection;
2. explicit source routing;
3. operator-authority and explicit-approval gates;
4. provider-receipt enforcement for target-system writes;
5. validation and persistence requirements before completion;
6. exact blocker output;
7. monotonic pipeline and artifact stages;
8. evidence classes including Architect Assertion, record-controlled allegation,
   adverse documentary contradiction and missing required record;
9. machine-readable completion summaries.

## Verification

An isolated Python 3 runtime compiled `operational_cognition/engine.py` and ran
11 unit tests successfully before repository submission.

Covered gates:

- authoritative capability outranks memory-only capability;
- missing capability returns an exact blocker;
- writes require operator authority;
- irreversible actions require explicit approval;
- a plan cannot substitute for execution;
- a claimed write without provider receipt is blocked;
- verified but unpersisted work is not complete;
- completion requires validation, ledger persistence and handoff;
- Architect Assertions remain active without false verification;
- pipeline and artifact regression are rejected;
- source routing is explicit.

GitHub Actions verification remains pending until the branch pull request runs.
Connector promotion remains blocked until one read-only and one reversible-write
provider receipt path complete under the new runtime.

## Truth Boundary

This receipt proves repository mutation and isolated unit-test execution. It does
not claim that external connectors are wired, that production writes are active,
or that `AKOS-OC-001` is working canonical.

## Next Governed Action

Open the pull request, run CI, review the diff, and then use `AKOS-OC-001` to
control the next audited CASEBRAIN source-to-recall probe.
