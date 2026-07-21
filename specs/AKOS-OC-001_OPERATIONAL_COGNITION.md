# AKOS-OC-001 — Operational Cognition

**Status:** active draft  
**Version:** 0.1.0  
**Owner:** AKOS Cognitive Kernel and Colossal Orchestrator  
**Effective:** 2026-07-21

## Purpose

Operational Cognition is the AKOS layer that converts reasoning, tools, source access, operator authority, verification, and persistence into completed work.

It exists to eliminate the gap between high analytical capability and low operational closure.

## Governing equation

```text
Operational Power = Model Capability × Tool Power × Tool Literacy × Orchestration × Verification × Persistence
```

A zero or unverified value in verification or persistence prevents a completion claim.

## Six dimensions

### 1. Model capability

Reasoning, synthesis, classification, drafting, coding, and judgment support supplied by the active model.

### 2. Tool power

The operations actually exposed by connected, authenticated, and authorized systems. Tool presence is not tool success.

### 3. Tool literacy

The ability to select the authoritative source and correct operation; preserve provenance; distinguish metadata from content; understand provider receipts; and avoid unsupported claims.

### 4. Orchestration

The ability to bind multiple capabilities into one controlled sequence without duplicated inspection, planning theater, or state loss.

### 5. Verification

Provider-backed confirmation that the requested action happened in the correct target system and produced the expected result.

### 6. Persistence

Durable storage of the result, provenance, hash or provider identifier, validation result, and next-state handoff.

## Operator authority

The operator defines the objective and may authorize target-system mutation through the request itself.

Operational Cognition must not redirect the investigative or analytical burden back onto the operator when the missing proof is reasonably controlled by another actor or system. Operator assertions are preserved as active allegations and routed toward corroboration, record demand, contradiction testing, or controlled inference.

Operational authority does not permit the runtime to fabricate verification. Evidence class and completion status remain explicit.

## Evidence classes

| Class | Runtime treatment |
|---|---|
| `verified_fact` | Established by an authenticated record, recording, image, metadata, provider response, or admission. |
| `architect_assertion` | Operator firsthand account preserved as an active allegation and investigative input. |
| `corroborated_assertion` | Operator assertion supported by one or more independent sources or circumstances. |
| `record_controlled_allegation` | Material allegation whose decisive proof is reasonably expected in another actor's custody or control. |
| `adverse_documentary_contradiction` | Conflict within or between the opposing actor's own records. |
| `missing_required_record` | Record that should exist if the represented process, review, notice, or action occurred. |
| `inference` | Conclusion derived from established inputs and marked as inferential. |
| `disputed_actor_narrative` | Another actor's allegation; not promoted merely because it appears in an official document. |

## Source-routing rules

1. Private connected information routes to the connected private source.
2. Conversation or Library file content routes to the Files surface.
3. Fresh public facts route to current public web or an authoritative live API.
4. Repository state routes to the repository provider.
5. Local builds, tests, hashes, conversions, and packaging route to the execution runtime.
6. Memory may guide retrieval but may not substitute for an available authoritative source.

## Capability selection

A capability is usable only when it is:

- connected;
- authenticated;
- authorized for the requested operation;
- compatible with the target system;
- able to return a verifiable result;
- able to preserve or expose a durable receipt when completion is claimed.

When more than one capability can act, AKOS prefers the capability that is authoritative for the target, supports validation, and supports persistence.

## Runtime pipeline

```text
INTAKE -> BIND -> ROUTE -> EXECUTE -> VALIDATE -> REVIEW -> RELEASE -> LEDGER -> HANDOFF
```

- **INTAKE:** capture the concrete objective and expected result.
- **BIND:** bind source, actor, target, operation, authority, and boundaries.
- **ROUTE:** select the authoritative capability and smallest useful next action.
- **EXECUTE:** perform the actual target-system action.
- **VALIDATE:** confirm the result in the target system with a provider receipt.
- **REVIEW:** check scope, truth class, drift, security, and completeness.
- **RELEASE:** produce the requested artifact or changed state.
- **LEDGER:** persist provenance, result, receipt, hash or identifier, and status.
- **HANDOFF:** return the artifact, link, ID, exact blocker, or next governed action.

## Artifact lifecycle

```text
LOCATED -> ACQUIRED -> HASHED -> PRESERVED -> PARSED -> CLASSIFIED ->
CORRELATED -> DRAFTED -> VERIFIED -> PACKAGED -> STORED -> LOGGED -> READY_FOR_USE
```

Stages are monotonic. A later stage may not be claimed before required earlier stages have receipts.

## Mutation gates

- Read and analysis actions may proceed through approved access.
- Reversible writes require operator authorization.
- Irreversible mutation, external sending, legal filing, service, publication, court contact, or law-enforcement contact requires explicit approval.
- Delete, destructive overwrite, reset, and history destruction remain disabled unless specifically authorized.
- Credentials and connection identifiers never enter source control, memory, receipts, or user-visible logs.

## Completion contract

A task is complete only when all requirements applicable to that task are satisfied:

1. the actual requested action occurred;
2. the target system returned or exposed a provider receipt;
3. the result was independently re-read, fetched, tested, or otherwise validated;
4. the result and provenance were persisted;
5. the final handoff identifies the artifact, path, link, ID, or exact changed state.

A plan, inspection, summary, draft, architecture document, or proposed pull request is not completion unless that artifact was the requested outcome.

## Blocker contract

When blocked, AKOS returns:

- the exact failed capability, permission, dependency, provider condition, or missing input;
- the provider error or objective state sufficient to act;
- the smallest next action that changes the blocked condition;
- no fictional success and no repeated retry without a changed condition.

## Machine implementation

- Runtime package: `operational_cognition/`
- Schema: `schemas/operational_cognition.schema.json`
- Runtime manifest: `manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`
- Tests: `operational_cognition/test_engine.py`
- CI: `.github/workflows/operational-cognition.yml`

## Promotion gate

`AKOS-OC-001` may move from active draft to working canonical after:

1. schema and unit tests pass;
2. one read-only connector route produces a receipt-backed result;
3. one reversible write route produces a provider receipt, validation receipt, ledger receipt, and handoff;
4. no completion claim is made without verification and persistence.
