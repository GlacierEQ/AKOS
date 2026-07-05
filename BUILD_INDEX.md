# AKOS Build Index

Status: Active
Version: 0.1.0
Updated: 2026-07-04

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
| `manifests/` | System and family manifests |
| `templates/` | Reusable starter files |
| `methodologies/` | Operating methods such as Pro-Code |
| `adr/` | Architecture decision records |
| `ledger/` | Append-only build and sync records |
| `audits/` | Review and quality gate records |

## Active Specification Series

| Spec | Title | Target Path | Status |
|---|---|---|---|
| AKOS-LAW-001 | Foundational Laws | `specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md` | planned |
| AKOS-CK-001 | Cognitive Kernel | `specs/AKOS-CK-001_COGNITIVE_KERNEL.md` | planned |
| AKOS-COM-001 | Canonical Object Model | `specs/AKOS-COM-001_CANONICAL_OBJECT_MODEL.md` | planned |
| AKOS-META-001 | Metadata Standard | `specs/AKOS-META-001_METADATA_STANDARD.md` | planned |
| AKOS-REPO-CONTRACT-001 | Repository Contract | `contracts/AKOS-REPO-CONTRACT-001.md` | planned |
| AKOS-PROCODE-001 | Pro-Code Methodology | `methodologies/pro_code/AKOS-PROCODE-001.md` | planned |

## Construction Order

1. Governance
2. Foundational Laws
3. Cognitive Kernel
4. Canonical Object Model
5. Metadata Standard
6. Repository Contract
7. Pro-Code Methodology
8. Templates
9. Family Manifests
10. Review/Audit Records
11. Adoption into external repos

## Canonical Promotion Rule

No file becomes canonical until it has:

- identity
- purpose
- version
- status
- source or origin
- review status
- clear relationship to the AKOS stack

## Current Priority

Build the foundation correctly before expanding runtime automation.
