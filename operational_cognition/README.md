# AKOS Operational Cognition Runtime

Canonical ID: `AKOS-OC-001`

This module converts tool power, tool literacy, orchestration, verification, and persistence into deterministic runtime decisions.

## Core rule

A model response, plan, inspection, or draft is not completion when the requested outcome requires a real target-system action.

Completion requires:

1. a supported and authenticated capability;
2. operator authority for mutation;
3. explicit approval for irreversible, external-send, or legal-filing actions;
4. a provider receipt for claimed writes;
5. authoritative validation;
6. a persisted ledger receipt and handoff.

## Runtime pipeline

```text
INTAKE -> BIND -> ROUTE -> EXECUTE -> VALIDATE -> REVIEW -> RELEASE -> LEDGER -> HANDOFF
```

## Artifact lifecycle

```text
LOCATED -> ACQUIRED -> HASHED -> PRESERVED -> PARSED -> CLASSIFIED ->
CORRELATED -> DRAFTED -> VERIFIED -> PACKAGED -> STORED -> LOGGED -> READY_FOR_USE
```

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
```
