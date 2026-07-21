# AKOS Build Index

Status: Active Draft  
Version: 0.4.1  
Updated: 2026-07-21

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
| `operational_cognition/` | Receipt-driven execution and system-first topology cognition |

## Active Specification Series

| Spec | Title | Target Path | Status |
|---|---|---|---|
| AKOS-LAW-001 | Foundational Laws | `specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md` | planned |
| AKOS-CK-001 | Cognitive Kernel | `specs/AKOS-CK-001_COGNITIVE_KERNEL.md` | active seed |
| AKOS-OC-001 | Operational Cognition | `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md` | active draft; executable runtime included |
| AKOS-COM-001 | Canonical Object Model | `specs/AKOS-COM-001_CANONICAL_OBJECT_MODEL.md` | active seed |
| AKOS-META-001 | Metadata Standard | `specs/AKOS-META-001_METADATA_STANDARD.md` | active seed |
| AKOS-REPO-CONTRACT-001 | Repository Contract | `contracts/AKOS-REPO-CONTRACT-001.md` | active seed |
| AKOS-PROCODE-001 | Pro-Code Methodology | `methodologies/pro_code/AKOS-PROCODE-001.md` | working canon |
| AKOS-AGENT-CONTRACT-001 | Agent Contract | `contracts/AKOS-AGENT-CONTRACT-001.md` | active seed |
| AKOS-FEDERATION-CONTRACT-001 | CASEBRAIN repository federation | `contracts/AKOS-FEDERATION-CONTRACT-001.md` | review ready |

## Operational Cognition Pack

| Artifact | Path / Owner | Status |
|---|---|---|
| Formal specification | `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md` | active draft v0.3.0 |
| Core runtime | `operational_cognition/engine.py` | implemented |
| System-first topology runtime | `operational_cognition/topology.py` | implemented |
| Unit tests | `operational_cognition/test_engine.py` | implemented |
| Topology regression tests | `operational_cognition/test_topology.py` | implemented |
| Architecture tests | `operational_cognition/test_contracts.py` | implemented |
| Test discovery | `pytest.ini` | implemented |
| Operational record schema | `schemas/operational_cognition.schema.json` | validated JSON draft |
| System topology schema | `schemas/akos_system_topology.schema.json` | implemented |
| Runtime manifest | `manifests/runtime/AKOS_OPERATIONAL_COGNITION.json` | active draft v0.3.0 |
| Canonical topology manifest | `manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json` | active draft |
| System-first mentality | `docs/operational_cognition/SYSTEM_FIRST_MENTALITY.md` | active draft |
| Public CI action | `GlacierEQ/public-actions-runner-host` / `akos-operational-cognition-ci` | runner registration proposed |
| Private execution receipts | `GlacierEQ/llm-runner-teams/results/<job_id>.json` | required |
| Build receipt | `ledger/2026-07-21_OPERATIONAL_COGNITION.md` | branch receipt |

AKOS owns no executable private-repository Actions workflows. Private CI and validation route through the public action face, which performs an allowlisted short-lived checkout and publishes immutable detailed receipts to the private control plane.

The runtime now enforces both execution-first and system-first cognition:

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

A wrong-plane failure is not evidence that the correct execution plane is missing. When an execution plane exists but the exact route is absent, AKOS extends the existing catalog, adapter, or route binding instead of creating parallel infrastructure.

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

The federation registry adds design-stage Source Intake/Hasher, Timeline Normalizer, Contradiction Candidate, Memory Distiller, Notion Review Mirror and Operator Control workers. No worker is marked `verified_live`.

## Construction Order

1. Governance and valid manifest
2. Foundational laws and truth contracts
3. Operational Cognition execution and receipt contract
4. System-first topology and anti-rebuild cognition
5. Public action-face registration and private-receipt validation
6. Canonical Object Model and metadata
7. Repository and federation contracts
8. Pro-Code review
9. Commit-pinned manifests and schemas
10. Credential rotation and storage hardening
11. One audited read-only integration slice through AKOS-OC-001
12. One receipt-backed reversible write probe
13. Worker dry run with immutable receipt
14. Human-reviewed promotion

## Canonical Promotion Rule

No file, repository, connector or worker becomes canonical/live until it has identity, purpose, version and source revision; explicit claim and authority boundaries; topology alignment; Pro-Code review and passing schema validation; a deployment/run receipt where runtime behavior is claimed; and human approval for promotion.

No runtime task becomes complete merely because a plan, draft, or status report exists. Completion requires architecture discovery, correct-plane execution, authoritative validation, persistence, and handoff under `AKOS-OC-001`.

## Current Priority

Merge the public action registration, dispatch `akos-operational-cognition-ci` against the exact AKOS branch SHA, preserve the private receipt, and then run one source-to-recall path through Operational Cognition. Do not create parallel runners or private workflows for work already owned by the public execution face.
