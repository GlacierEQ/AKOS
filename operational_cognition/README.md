# AKOS Operational Cognition Runtime

Canonical ID: `AKOS-OC-001`

This package converts model capability, tool power, tool literacy, architecture literacy, orchestration, verification, and persistence into deterministic runtime decisions.

## Core rule

A model response, plan, inspection, or draft is not completion when the requested outcome requires a real target-system action.

A failed attempt in the wrong plane is not proof that the correct plane is missing.

## System-first sequence

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

Before diagnosing absence or proposing infrastructure, inspect canonical manifests, repository roles, catalogs, adapters, open pull requests, connected capabilities, and receipt stores.

## Runtime pipeline

```text
INTAKE -> BIND -> DISCOVER -> MAP -> ROUTE -> EXECUTE ->
VALIDATE -> REVIEW -> RELEASE -> LEDGER -> HANDOFF
```

## Artifact lifecycle

```text
LOCATED -> ACQUIRED -> HASHED -> PRESERVED -> PARSED -> CLASSIFIED ->
CORRELATED -> DRAFTED -> VERIFIED -> PACKAGED -> STORED -> LOGGED -> READY_FOR_USE
```

## Existing private-workload execution route

```text
GlacierEQ/AKOS
  -> metadata-only job + exact source ref
GlacierEQ/public-actions-runner-host
  -> allowlisted public execution
GlacierEQ/llm-runner-teams
  -> private policy, claim, approval, and immutable receipt
```

Private AKOS owns no executable GitHub Actions workflows.

## Anti-rebuild behavior

- Reuse a verified route before creating infrastructure.
- Extend the existing execution plane with one bounded catalog action, adapter, or route binding before creating a new runner.
- Reject a private workflow when the public execution face already owns the work.
- Reject a new runner or control plane when the verified topology already supplies one.
- Require architecture discovery before treating a capability as absent.
- Convert material operator corrections into a policy record, executable guard, regression test, repaired route, and append-only receipt.

## Evidence classes

- `verified_fact`
- `architect_assertion`
- `corroborated_assertion`
- `record_controlled_allegation`
- `adverse_documentary_contradiction`
- `missing_required_record`
- `inference`
- `disputed_actor_narrative`

An Architect Assertion is preserved as an active allegation and investigative input. It is not discarded for lack of an externally controlled record, and it is not automatically mislabeled as independently verified.

## Tests

```bash
python -m compileall -q operational_cognition
python -m unittest -v operational_cognition.test_engine
python -m unittest -v operational_cognition.test_topology
pytest
```

Public verification routes through `GlacierEQ/public-actions-runner-host` action `akos-operational-cognition-ci`; detailed results return to `GlacierEQ/llm-runner-teams/results/<job_id>.json`.
