# AKOS Operational Cognition Build Receipt

**Date:** 2026-07-21  
**Canonical ID:** AKOS-OC-001  
**Branch:** `akos-operational-cognition-2026-07-21`  
**Pull Request:** `GlacierEQ/AKOS#7`  
**Status:** implemented on branch; public runner registration and immutable execution receipt pending

## Objective

Convert the comparative analysis of tool power, tool literacy, orchestration, verification, persistence, and execution continuity into executable AKOS operational cognition.

## Changed State

Created:

- `operational_cognition/__init__.py`
- `operational_cognition/engine.py`
- `operational_cognition/test_engine.py`
- `operational_cognition/test_contracts.py`
- `operational_cognition/README.md`
- `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md`
- `schemas/operational_cognition.schema.json`
- `manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`
- `pytest.ini`

Updated:

- `README.md`
- `AKOS_MANIFEST.yaml`
- `BUILD_INDEX.md`
- `CURRENT_STATE.md`

Removed:

- `.github/workflows/operational-cognition.yml`
- `.github/workflows/ci.yml`

The removed workflows were invalid for the established APEX architecture because AKOS is a private workload and policy repository. Private repositories do not own GitHub Actions execution. All such work routes through the public action face.

## Public Runner Binding

The governed route is:

```text
GlacierEQ/AKOS private source ref
  -> metadata-only job request
GlacierEQ/public-actions-runner-host
  -> allowlisted short-lived checkout
  -> GitHub-hosted execution
GlacierEQ/llm-runner-teams
  -> immutable private result receipt
  -> sanitized public status and operator handoff
```

A registration change was created in `GlacierEQ/public-actions-runner-host` on branch `akos-operational-cognition-ci` for:

```text
pillar: C
action: akos-operational-cognition-ci
target_repo: GlacierEQ/AKOS
adapter: test
gate: standard
```

## Runtime Capabilities

The implementation provides:

1. authoritative capability selection;
2. explicit source routing;
3. operator-authority and explicit-approval gates;
4. provider-receipt enforcement for target-system writes;
5. validation and persistence requirements before completion;
6. exact blocker output;
7. monotonic pipeline and artifact stages;
8. evidence classes including Architect Assertion, record-controlled allegation, adverse documentary contradiction, and missing required record;
9. machine-readable completion summaries;
10. architecture enforcement that a private AKOS repository owns no executable Actions workflows.

## Verification

An isolated Python 3 runtime compiled `operational_cognition/engine.py` and ran 11 unit tests successfully before repository submission.

Covered gates:

- authoritative capability outranks memory-only capability;
- missing capability returns an exact blocker;
- writes require operator authority;
- irreversible actions require explicit approval;
- a plan cannot substitute for execution;
- a claimed write without provider receipt is blocked;
- verified but unpersisted work is not complete;
- completion requires validation, ledger persistence, and handoff;
- Architect Assertions remain active without false verification;
- pipeline and artifact regression are rejected;
- source routing is explicit.

The earlier private-repository Action attempts are retained only as evidence of incorrect routing. Their failures do not establish a missing runner. The correct execution capability already exists in the APEX public runner team; the defect was that the AKOS work was sent through the wrong plane.

## Truth Boundary

This receipt proves repository mutation, isolated unit-test execution, private-workflow removal, and creation of the public action registration branch. It does not claim that the public action registration is merged, that the public runner job has completed, or that an immutable private result receipt already exists.

## Next Governed Action

Merge the action registration into the public execution face, dispatch `akos-operational-cognition-ci` against the exact AKOS source ref, preserve the immutable result under `GlacierEQ/llm-runner-teams/results/<job_id>.json`, and update PR #7 with that receipt.
