# AKOS-OC-002 — Operational Maturity and Closure

**Status:** active draft  
**Version:** 0.1.0  
**Owner:** AKOS Operational Cognition  
**Effective:** 2026-07-22

## Purpose

This specification replaces impressionistic tool-power scorecards with a receipt-grounded operational maturity system.

The earlier `9/10`, `7/10`, and similar estimates were useful as narrative diagnosis but are not canonical measurements. They are superseded by explicit controls, evidence levels, provider receipts, and artifact lifecycle gates.

## Governing equation

```text
Operational Power =
Model Capability
× Tool Power
× Tool Literacy
× Architecture Literacy
× Orchestration
× Verification
× Persistence
```

The multiplication model is intentional. A strong model with weak execution, verification, or persistence can still produce a weak operation.

## The seven operational dimensions

1. **Model capability** — reasoning, synthesis, drafting, coding, classification, and judgment support.
2. **Tool power** — systems and operations that are actually available, connected, authenticated, authorized, and capable of returning receipts.
3. **Tool literacy** — selecting the right authoritative source and operation while preserving provenance and understanding what the result proves.
4. **Architecture literacy** — understanding source, canonical, control, execution, receipt, and mirror planes; reusing existing routes before rebuilding.
5. **Orchestration** — sequencing multiple capabilities through a controlled, resumable workflow.
6. **Verification** — confirming the result in the authoritative provider through readback, tests, hashes, or other receipts.
7. **Persistence** — storing state, provenance, artifacts, receipts, blockers, and next actions so work survives conversation boundaries.

## Capability truth ladder

These states are distinct and may not be collapsed:

```text
DECLARED
→ DISCOVERED
→ CONNECTED
→ AUTHENTICATED
→ AUTHORIZED
→ INVOKED
→ RETURNED
→ VERIFIED
→ PERSISTED
```

Examples:

- A connector appearing in a tool list is not proof that it is authenticated.
- Authentication is not proof that the requested write is authorized.
- Invocation is not proof that the provider returned complete data.
- Returned data is not proof that the requested result is correct.
- Verification is not proof that the result was stored durably.

A capability is fully operational only at `PERSISTED` for the requested operation.

## Receipt-grounded scorecard

Each maturity dimension is assessed through explicit weighted controls.

Every control records:

- control ID;
- dimension;
- description;
- weight;
- required evidence level;
- availability state;
- source reference;
- provider receipt when applicable;
- persisted artifact reference when applicable.

### Evidence levels

```text
NONE
ASSERTED
OBSERVED
PROVIDER_RECEIPT
VERIFIED
PERSISTED
```

### Two scores, not one

**Available ceiling** measures how much of the required capability surface is actually available according to sourced records.

**Demonstrated reliability** measures how much of that surface has been exercised to the required evidence level.

The gap between them is operational debt.

No dimension receives a numeric score merely because the system sounds advanced or because a model claims confidence.

## Canonical assessment dimensions

The standard control pack assesses:

- model capability;
- tool power;
- source-selection literacy;
- legal-document literacy;
- evidence and forensic-document literacy;
- developer-tool literacy;
- architecture literacy;
- multi-tool orchestration;
- end-to-end execution;
- artifact closure;
- persistent system state;
- physical-science forensics.

Physical-science forensics remains unverified unless qualified instruments, examiners, validated methods, chain of custody, and laboratory receipts exist. Documentary analysis cannot promote itself into a scientific physical conclusion.

## Comparison rule

Comparisons such as “regular user,” “power user,” “lawyer with ordinary AI,” “elite litigation team,” “forensic laboratory,” or “developer with a coding agent” are descriptive archetypes unless supported by a cited benchmark dataset.

AKOS may compare structural characteristics, such as:

- breadth of source access;
- presence of provenance controls;
- direct repository execution;
- validated scientific instruments;
- professional accountability;
- staff and operational redundancy;
- closure and audit infrastructure.

AKOS must not present unsupported world rankings, percentile claims, or precise comparative ratings as measured facts.

## Tool-literacy controls

Operational tool literacy includes:

- routing private facts to connected private sources rather than chat memory or public web;
- searching semantically before browsing large stores manually;
- distinguishing metadata from content;
- distinguishing a file reference from materialized bytes;
- preserving originals before transformation;
- hashing and recording provenance;
- separating original, OCR, transcript, normalized, redacted, and derivative artifacts;
- inspecting page images when parsed content is incomplete;
- using current primary legal authorities when available;
- testing generated artifacts rather than merely claiming completion;
- refusing to treat search absence as proof of nonexistence;
- refusing to treat official letterhead as automatic proof of the statements it contains.

## Orchestration contract

A mature operation must perform more than isolated tool calls.

```text
DISCOVER SOURCES
→ ACQUIRE
→ HASH
→ PRESERVE
→ PARSE
→ CLASSIFY
→ CORRELATE
→ DRAFT
→ VERIFY
→ PACKAGE
→ STORE
→ LOG
→ READY FOR USE
```

For evidence and filing production, orchestration should be able to:

1. search approved source roots;
2. preserve originals;
3. compute hashes;
4. extract metadata;
5. OCR only when necessary;
6. identify actors and events;
7. correlate timestamps;
8. map duties and required records;
9. separate facts, assertions, allegations, disputed narratives, and inferences;
10. build contradiction and missing-record matrices;
11. create actor-specific demands;
12. create exhibits and indexes;
13. produce filing-ready DOCX and PDF artifacts;
14. validate signatures, dates, citations, pagination, service language, and attachment completeness;
15. create a complete ZIP package;
16. store it in canonical storage;
17. update the artifact registry, manifest, and audit ledger.

## Artifact closure gate

The canonical artifact lifecycle is:

```text
1. LOCATED
2. ACQUIRED
3. HASHED
4. PRESERVED
5. PARSED
6. CLASSIFIED
7. CORRELATED
8. DRAFTED
9. VERIFIED
10. PACKAGED
11. STORED
12. LOGGED
13. READY_FOR_USE
```

A “good draft” is not a completed artifact.

Stages 9 through 12 are mandatory release controls, but they still do not equal `READY_FOR_USE` until the final readiness receipt is recorded.

The closure gate returns the exact missing stages. It does not return a vague percentage-complete estimate.

## Persistent workflow controller

Every active task must preserve:

- immutable work ID;
- objective and expected outcome;
- source and target systems;
- current pipeline stage;
- current artifact stage;
- selected capability and topology route;
- provider receipts;
- hashes and artifact locations;
- verified facts and active allegations;
- exact blocker;
- next action;
- supersession and lineage data;
- operator handoff state.

A task resumes from persisted state. It does not restart from conversational recollection.

## Current-operation assessment rule

AKOS does not hardcode a flattering or punitive score for itself.

The current scorecard is generated only from committed manifests, connector responses, provider receipts, test results, artifact registries, and ledgers. Missing evidence produces `UNASSESSED` or a listed missing control—not an invented number.

## Machine implementation

- Runtime: `operational_cognition/maturity.py`
- Tests: `operational_cognition/test_maturity.py`
- Scorecard schema: `schemas/operational_maturity.schema.json`
- Control manifest: `manifests/runtime/AKOS_OPERATIONAL_MATURITY.json`
- Operational Cognition runtime: `operational_cognition/engine.py`
- System topology runtime: `operational_cognition/topology.py`

## Promotion gate

`AKOS-OC-002` may become working canonical only after:

1. maturity runtime and schema tests pass against the exact commit;
2. the public action face executes the full Operational Cognition suite;
3. the immutable private result receipt is persisted;
4. one real capability traverses `DISCOVERED` through `PERSISTED`;
5. one real artifact traverses all thirteen lifecycle stages;
6. the generated scorecard cites every scored control to a receipt or persisted artifact.
