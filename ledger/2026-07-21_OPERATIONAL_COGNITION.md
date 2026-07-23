# AKOS Operational Cognition Build Receipt

**Date:** 2026-07-21  
**Canonical ID:** AKOS-OC-001  
**Branch:** `akos-operational-cognition-2026-07-21`  
**Pull Request:** `GlacierEQ/AKOS#7`  
**Status:** implemented on branch; public runner registration and immutable execution receipt pending

## Objective

Convert the comparative analysis of model capability, tool power, tool literacy, architecture literacy, orchestration, verification, persistence, and execution continuity into executable AKOS operational cognition.

## Correction Captured

The initial implementation incorrectly treated failed private-repository workflow attempts as evidence that an execution runner was missing.

The operator corrected that diagnosis: the APEX architecture already provides a public execution face and a private control/receipt plane.

AKOS converted that correction into system state rather than leaving it as an apology:

1. private AKOS workflows were removed;
2. the public runner lane was registered in `GlacierEQ/public-actions-runner-host#15`;
3. the private receipt route through `GlacierEQ/llm-runner-teams` was restored;
4. a canonical topology manifest and schema were added;
5. executable topology guards and regression tests were added;
6. the formal Operational Cognition contract was upgraded with architecture literacy and anti-rebuild rules.

## Created

- `operational_cognition/__init__.py`
- `operational_cognition/engine.py`
- `operational_cognition/topology.py`
- `operational_cognition/test_engine.py`
- `operational_cognition/test_topology.py`
- `operational_cognition/test_contracts.py`
- `operational_cognition/README.md`
- `docs/operational_cognition/SYSTEM_FIRST_MENTALITY.md`
- `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md`
- `schemas/operational_cognition.schema.json`
- `schemas/akos_system_topology.schema.json`
- `manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`
- `manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`
- `pytest.ini`

## Updated

- `README.md`
- `AKOS_MANIFEST.yaml`
- `BUILD_INDEX.md`
- `CURRENT_STATE.md`

## Removed

- `.github/workflows/operational-cognition.yml`
- `.github/workflows/ci.yml`

The removed workflows violated the established APEX architecture because AKOS is a private workload and policy repository. Private repositories do not own GitHub Actions execution.

## Locked Public Runner Binding

```text
GlacierEQ/AKOS
  private source ref + canonical policy
        |
        | metadata-only job request
        v
GlacierEQ/public-actions-runner-host
  sole public Actions execution face
        |
        | governed execution result
        v
GlacierEQ/llm-runner-teams
  private control, approval, claim, and immutable receipt plane
```

Public runner registration:

```text
pillar: C
action: akos-operational-cognition-ci
target_repo: GlacierEQ/AKOS
adapter: test
gate: standard
```

## System-First Runtime

The topology runtime now enforces:

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

It distinguishes:

- an existing ready route;
- an existing execution plane with an unregistered lane;
- a missing adapter or route binding;
- a missing permission or approval;
- successful execution with a missing receipt;
- unverified topology;
- verified absence of an execution plane.

It rejects:

- private workflows when the public execution face exists;
- new runners when the existing plane can execute or be extended;
- duplicate control planes;
- infrastructure proposals made before architecture discovery;
- wrong-plane failure as proof of system absence.

When the execution plane exists but the exact lane is missing, the allowed response is one bounded catalog action, adapter, or route binding—not a parallel runner.

## Core Runtime Capabilities

1. authoritative capability selection;
2. explicit source routing;
3. operator-authority and explicit-approval gates;
4. provider-receipt enforcement for target-system writes;
5. validation and persistence requirements before completion;
6. exact blocker output;
7. monotonic pipeline and artifact stages;
8. evidence classes including Architect Assertion, record-controlled allegation, adverse documentary contradiction, and missing required record;
9. machine-readable completion summaries;
10. system topology resolution and anti-rebuild proposal judgment;
11. architecture enforcement that private AKOS owns no executable Actions workflows.

## Verification

Before repository submission, an isolated Python 3 runtime compiled the original Operational Cognition engine and ran 11 unit tests successfully.

After the system-first correction, an isolated Python 3 harness compiled the new topology runtime and exercised discovery, existing-route resolution, private-workflow rejection, new-runner rejection, bounded catalog extension, receipt-plane blocking, and duplicate-node rejection successfully.

The exact committed topology suite remains subject to the registered public-runner execution and immutable private result receipt.

## Truth Boundary

This receipt proves repository mutation, private-workflow removal, topology policy implementation, addition of executable guards and regression tests, isolated runtime checks, and creation of the public action registration branch.

It does not claim that public runner PR #15 is merged, that `akos-operational-cognition-ci` has executed against the current AKOS head, or that an immutable private result receipt already exists.

## Next Governed Action

Merge the action registration into the public execution face, dispatch `akos-operational-cognition-ci` against the exact AKOS source ref, preserve the immutable result under `GlacierEQ/llm-runner-teams/results/<job_id>.json`, and update PR #7 with that receipt.
