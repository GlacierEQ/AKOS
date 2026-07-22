# AKOS Build Index

Status: Active Draft  
Version: 0.5.0  
Updated: 2026-07-22

## Purpose

This file is the navigation index for the AKOS architecture repository. It records what exists, what is canonical, what is historical, and what still needs construction.

## Canonical Root Files

| File | Role | Status |
|---|---|---|
| `README.md` | Root definition and boot rule | active |
| `AKOS_MANIFEST.yaml` | System manifest | active draft |
| `BUILD_INDEX.md` | Repository navigation index | active draft |
| `CURRENT_STATE.md` | Read-first operational state | active draft |
| `GOVERNANCE.md` | Promotion and review rules | active |
| `ROADMAP.md` | Build sequence | active |

## Existing Historical Files

| File | Status | Note |
|---|---|---|
| `REPOS.md` | historical / portfolio context | APEX portfolio inventory, not architecture canon |
| `SESSIONS.md` | historical / session context | retained for provenance |

## Canonical Areas

| Directory | Role |
|---|---|
| `docs/` | Human-readable architecture doctrine |
| `specs/` | Formal AKOS specifications |
| `contracts/` | Compatibility and interface contracts |
| `schemas/` | Machine-readable validation schemas |
| `manifests/` | System, family, agent, methodology and runtime manifests |
| `templates/` | Reusable starter files |
| `methodologies/` | Pro-Code, Chunk Power and Agentic Evolution methods |
| `adr/` | Architecture decision records |
| `ledger/` | Append-only build and sync records |
| `audits/` | Review and quality-gate records |
| `operational_cognition/` | Execution, topology, maturity, and artifact-closure runtime |

## Active Specification Series

| Spec | Title | Target Path | Status |
|---|---|---|---|
| AKOS-LAW-001 | Foundational Laws | `specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md` | planned |
| AKOS-CK-001 | Cognitive Kernel | `specs/AKOS-CK-001_COGNITIVE_KERNEL.md` | active seed |
| AKOS-OC-001 | Operational Cognition | `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md` | active draft; executable runtime included |
| AKOS-OC-002 | Operational Maturity and Closure | `specs/AKOS-OC-002_OPERATIONAL_MATURITY.md` | active draft; executable runtime included |
| AKOS-COM-001 | Canonical Object Model | `specs/AKOS-COM-001_CANONICAL_OBJECT_MODEL.md` | active seed |
| AKOS-META-001 | Metadata Standard | `specs/AKOS-META-001_METADATA_STANDARD.md` | active seed |
| AKOS-REPO-CONTRACT-001 | Repository Contract | `contracts/AKOS-REPO-CONTRACT-001.md` | active seed |
| AKOS-PROCODE-001 | Pro-Code Methodology | `methodologies/pro_code/AKOS-PROCODE-001.md` | working canon |
| AKOS-AGENT-CONTRACT-001 | Agent Contract | `contracts/AKOS-AGENT-CONTRACT-001.md` | active seed |
| AKOS-FEDERATION-CONTRACT-001 | CASEBRAIN repository federation | `contracts/AKOS-FEDERATION-CONTRACT-001.md` | review ready |

## Operational Cognition Pack

| Artifact | Path / Owner | Status |
|---|---|---|
| Operational Cognition spec | `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md` | active draft v0.3.0 |
| Operational Maturity spec | `specs/AKOS-OC-002_OPERATIONAL_MATURITY.md` | active draft v0.1.0 |
| Core runtime | `operational_cognition/engine.py` | implemented |
| System-first topology runtime | `operational_cognition/topology.py` | implemented |
| Maturity and closure runtime | `operational_cognition/maturity.py` | implemented |
| Core tests | `operational_cognition/test_engine.py` | implemented |
| Topology tests | `operational_cognition/test_topology.py` | implemented |
| Maturity tests | `operational_cognition/test_maturity.py` | implemented |
| Contract tests | `operational_cognition/test_contracts.py` | implemented |
| Test discovery | `pytest.ini` | implemented |
| Operational record schema | `schemas/operational_cognition.schema.json` | active draft |
| System topology schema | `schemas/akos_system_topology.schema.json` | active draft |
| Maturity scorecard schema | `schemas/operational_maturity.schema.json` | active draft |
| Operational manifest | `manifests/runtime/AKOS_OPERATIONAL_COGNITION.json` | active draft v0.3.0 |
| Topology manifest | `manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json` | active draft |
| Maturity manifest | `manifests/runtime/AKOS_OPERATIONAL_MATURITY.json` | active draft v0.1.0 |
| System-first mentality | `docs/operational_cognition/SYSTEM_FIRST_MENTALITY.md` | active draft |
| Public CI action | `GlacierEQ/public-actions-runner-host` / `akos-operational-cognition-ci` | runner registration proposed |
| Private execution receipts | `GlacierEQ/llm-runner-teams/results/<job_id>.json` | required |
| Cognition receipt | `ledger/2026-07-21_OPERATIONAL_COGNITION.md` | branch receipt |
| Maturity receipt | `ledger/2026-07-22_OPERATIONAL_MATURITY.md` | branch receipt |

## Operational Truth Rules

```text
Capability:
DECLARED -> DISCOVERED -> CONNECTED -> AUTHENTICATED -> AUTHORIZED ->
INVOKED -> RETURNED -> VERIFIED -> PERSISTED

Architecture:
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST

Artifact:
LOCATED -> ACQUIRED -> HASHED -> PRESERVED -> PARSED -> CLASSIFIED ->
CORRELATED -> DRAFTED -> VERIFIED -> PACKAGED -> STORED -> LOGGED -> READY_FOR_USE
```

AKOS owns no executable private-repository Actions workflows. Private CI and validation route through the public action face, which performs an allowlisted short-lived checkout and publishes immutable detailed receipts to the private control plane.

A wrong-plane failure is not evidence that the correct execution plane is missing. An available tool is not a verified capability. A good draft is not a completed artifact. Unmeasured maturity remains `UNASSESSED` rather than receiving an invented numeric score.

## CASEBRAIN Federation Pack

| Artifact | Path | Status |
|---|---|---|
| Federation contract | `contracts/AKOS-FEDERATION-CONTRACT-001.md` | review ready |
| Registry schema | `schemas/CASEBRAIN_POWERUP_FEDERATION.schema.json` | validated draft |
| Repository/worker registry | `manifests/federations/CASEBRAIN_POWERUP_FEDERATION.json` | validated draft |
| Operator guide | `docs/federation/CASEBRAIN_POWERUP_FEDERATION.md` | review ready |
| Build ledger | `ledger/2026-07-14_CASEBRAIN_POWERUP_FEDERATION.md` | proposed receipt |

## Active Agentic Seeds

| Agent | Manifest | Status |
|---|---|---|
| Memory Curator | `manifests/agents/AGENT-MEMORY-CURATOR.yaml` | active seed |
| Repository Steward | `manifests/agents/AGENT-REPOSITORY-STEWARD.yaml` | active seed |
| Pro-Code Reviewer | `manifests/agents/AGENT-PROCODE-REVIEWER.yaml` | active seed |

## Construction Order

1. Governance and valid manifest
2. Foundational laws and truth contracts
3. Operational Cognition execution and receipt contract
4. System-first topology and anti-rebuild cognition
5. Operational maturity controls and artifact closure
6. Public action-face registration and private-receipt validation
7. First receipt-grounded AKOS scorecard
8. One capability traversing through `PERSISTED`
9. One artifact traversing through `READY_FOR_USE`
10. Canonical Object Model and metadata
11. Repository and federation contracts
12. Pro-Code review
13. Commit-pinned manifests and schemas
14. Credential rotation and storage hardening
15. One audited read-only integration slice through AKOS-OC-001
16. One receipt-backed reversible write probe
17. Worker dry run with immutable receipt
18. Human-reviewed promotion

## Canonical Promotion Rule

No file, repository, connector, worker, scorecard, or artifact becomes canonical/live until it has identity, purpose, version and source revision; explicit claim and authority boundaries; topology alignment; control-level evidence; Pro-Code review and passing schema validation; a deployment or execution receipt where runtime behavior is claimed; complete artifact closure where applicable; and human approval for promotion.

No runtime task becomes complete merely because a plan, draft, status report, or high-confidence assessment exists. Completion requires architecture discovery, correct-plane execution, authoritative validation, persistence, artifact closure, and handoff under `AKOS-OC-001` and `AKOS-OC-002`.

## Current Priority

Merge the public action registration, dispatch `akos-operational-cognition-ci` against the exact AKOS branch SHA, preserve the private receipt, generate the first receipt-grounded maturity scorecard, and complete one real artifact through `READY_FOR_USE`.
