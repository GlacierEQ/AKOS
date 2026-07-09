# AKOS Build Index

Status: Active
Version: 0.1.3
Updated: 2026-07-08

## Purpose

This file is the navigation index for the AKOS architecture repository.

It records what exists, what is canonical, what is historical, and what still needs construction.

## Canonical Root Files

| File | Role | Status |
|---|---|---|
| `README.md` | Root definition and boot rule | active |
| `AKOS_MANIFEST.yaml` | System manifest | active |
| `BUILD_INDEX.md` | Repository navigation index | active |
| `GOVERNANCE.md` | Promotion and review rules | active |
| `ROADMAP.md` | Build sequence | active |

## Existing Historical Files

| File | Status | Note |
|---|---|---|
| `REPOS.md` | historical / portfolio context | APEX portfolio inventory, not AKOS architecture canon |
| `SESSIONS.md` | historical / session context | Session record retained for provenance |

## Canonical Areas

| Directory | Role |
|---|---|
| `docs/` | Human-readable architecture doctrine |
| `specs/` | Formal AKOS specifications |
| `contracts/` | Compatibility and interface contracts |
| `schemas/` | Machine-readable validation schemas |
| `manifests/` | System, family, agent, and methodology manifests |
| `templates/` | Reusable starter files |
| `methodologies/` | Operating methods such as Pro-Code, Chunk Power, and Agentic Evolution |
| `adr/` | Architecture decision records |
| `ledger/` | Append-only build and sync records |
| `audits/` | Review and quality gate records |

## Active Specification Series

| Spec | Title | Target Path | Status |
|---|---|---|---|
| AKOS-LAW-001 | Foundational Laws | `specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md` | planned |
| AKOS-CK-001 | Cognitive Kernel | `specs/AKOS-CK-001_COGNITIVE_KERNEL.md` | active seed |
| AKOS-COM-001 | Canonical Object Model | `specs/AKOS-COM-001_CANONICAL_OBJECT_MODEL.md` | active seed |
| AKOS-META-001 | Metadata Standard | `specs/AKOS-META-001_METADATA_STANDARD.md` | active seed |
| AKOS-REPO-CONTRACT-001 | Repository Contract | `contracts/AKOS-REPO-CONTRACT-001.md` | active seed |
| AKOS-PROCODE-001 | Pro-Code Methodology | `methodologies/pro_code/AKOS-PROCODE-001.md` | active seed |
| AKOS-ACE-001 | Agentic Cognitive Evolution | `specs/AKOS-ACE-001_AGENTIC_COGNITIVE_EVOLUTION.md` | active seed |
| AKOS-ACE-002 | Evolution Governance Model | `specs/AKOS-ACE-002_EVOLUTION_GOVERNANCE_MODEL.md` | active seed |
| AKOS-AGENT-CONTRACT-001 | Agent Contract | `contracts/AKOS-AGENT-CONTRACT-001.md` | active seed |
| AKOS-PER-001 | Persona Toolbelt Model | `specs/AKOS-PER-001_PERSONA_TOOLBELT_MODEL.md` | active draft |
| METH-PROCODE-CHUNK-POWER | Pro-Code Chunk Power | `methodologies/pro_code_chunk_power/README.md` | active seed |

## Active Agentic Seeds

| Agent | Manifest | Status |
|---|---|---|
| Memory Curator | `manifests/agents/AGENT-MEMORY-CURATOR.yaml` | active seed |
| Repository Steward | `manifests/agents/AGENT-REPOSITORY-STEWARD.yaml` | active seed |
| Pro-Code Reviewer | `manifests/agents/AGENT-PROCODE-REVIEWER.yaml` | active seed |

## Active Persona Families

| Family | Manifest | Status |
|---|---|---|
| Aionic Tree | `manifests/families/FAM-AIONIC-TREE.yaml` | active draft |

## Active Persona Bridge Documents

| Document | Path | Status |
|---|---|---|
| Aionic Tree to AKOS Toolbelt | `docs/persona-systems/AIONIC_TREE_TO_AKOS_TOOLBELT.md` | active draft |

## ACE Templates

| Template | Path | Status |
|---|---|---|
| Evolution Proposal | `templates/EVOLUTION_PROPOSAL.template.yaml` | active seed |
| Memory Delta | `templates/MEMORY_DELTA.template.yaml` | active seed |

## Construction Order

1. Governance
2. Foundational Laws
3. Cognitive Kernel
4. Canonical Object Model
5. Metadata Standard
6. Repository Contract
7. Pro-Code Methodology
8. Pro-Code Chunk Power
9. Agentic Cognitive Evolution
10. Templates
11. Family Manifests
12. Persona Toolbelt Manifests
13. Review/Audit Records
14. Adoption into external repos

## Canonical Promotion Rule

No file becomes canonical until it has:

- identity
- purpose
- version
- status
- source or origin
- review status
- clear relationship to the AKOS stack

## Chunk Power Rule

Build AKOS in small reviewable chunks. Each chunk must have a clear purpose, boundary, target path, review result, and next action.

## ACE Governance Rule

Agents may propose evolution. AKOS governs promotion.

## Current Priority

Harden AKOS-PER-001, create a reusable persona manifest template, and promote the Aionic Tree family into individual agent manifests only after Pro-Code review.
