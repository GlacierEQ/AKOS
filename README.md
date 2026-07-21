# AKOS — Apex Knowledge Operating System

Status: Foundational Build
Version: 0.4.0
Canonical Repo: `GlacierEQ/AKOS`
Created: 2026-07-04

## Prime Definition

AKOS is the Apex Knowledge Operating System: a recursive architecture for transforming knowledge into structured cognition, durable memory, reliable execution, and continuously improving systems.

AKOS is not one model, one prompt, one database, one repository, or one automation.

AKOS is the governing architecture that binds them.

## Core Stack

```text
Prime Purpose
↓
Foundational Laws
↓
Cognitive Kernel
↓
Operational Cognition
↓
Architecture Literacy
↓
Canonical Object Model
↓
Metadata Standard
↓
Repository Contracts
↓
Pro-Code Methodology
↓
Family Manifests
↓
Runtime Modules
↓
Operational Lanes
↓
Spiral Engine Evolution
```

## Foundational Rule

No artifact becomes canonical because it sounds powerful.

It becomes canonical when it has identity, provenance, structure, relationships, metadata, review status, and Pro-Code gate alignment.

## Finish-First Rule

No new architecture outranks finishable work.

The executable `finisher/` module scans an allowlisted queue of near-complete pull requests, distinguishes concrete blockers from inertia, blocks expansion when closure is available, and records provider-backed completion receipts. It may execute only bounded, explicitly enabled actions.

See `finisher/README.md`.

## Operational Cognition Rule

Model capability and tool access are potential. AKOS operational power requires tool literacy, architecture literacy, orchestration, verification, and persistence.

A plan, inspection, draft, or proposed design is not completion when the requested outcome requires a target-system action. Completion requires architecture discovery, correct-plane execution, authoritative validation, a provider receipt when applicable, a durable ledger receipt, and a final handoff.

See `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md` and `operational_cognition/README.md`.

## System-First Rule

AKOS must understand the existing system before declaring a blocker or proposing infrastructure.

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

A failed attempt in the wrong plane is not proof that the correct plane is missing. A memory failure is not proof that the architecture is absent. When an execution plane already exists, AKOS reuses it or adds one bounded catalog action, adapter, or route binding before considering new infrastructure.

For private GitHub workloads:

```text
GlacierEQ/AKOS
  -> exact source ref + metadata-only job
GlacierEQ/public-actions-runner-host
  -> public execution face
GlacierEQ/llm-runner-teams
  -> private control and immutable receipts
```

Private AKOS owns no executable GitHub Actions workflows.

See `docs/operational_cognition/SYSTEM_FIRST_MENTALITY.md` and `manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`.

## Repository Purpose

This repository is the canonical architecture home for:

- AKOS doctrine
- Cognitive Kernel methodology
- Operational Cognition runtime
- System topology and architecture literacy
- Canonical Object Model
- Metadata standards
- Repository contracts
- Pro-Code methodology
- Family manifests
- Templates
- Build records
- Architecture decision records
- Finish-first closure operations

## Directory Map

```text
/docs/                     Human-readable architecture doctrine
/specs/                    Formal AKOS specifications
/contracts/                Required compatibility contracts
/schemas/                  Machine-readable validation schemas
/manifests/                Family and system manifests
/templates/                Reusable file templates
/methodologies/            Operating methods such as Pro-Code
/adr/                      Architecture decision records
/ledger/                   Append-only build and sync records
/finisher/                 Deterministic closure engine and receipt queue
/operational_cognition/    Execution-first and system-first cognition runtime
```

## Active Specs

- `AKOS-CK-001` — Cognitive Kernel
- `AKOS-OC-001` — Operational Cognition
- `AKOS-COM-001` — Canonical Object Model
- `AKOS-META-001` — Metadata Standard
- `AKOS-REPO-CONTRACT-001` — Repository Contract
- `AKOS-PROCODE-001` — Pro-Code Methodology

## Session Boot Rule

At the start of any AKOS-aware session:

1. Read this README.
2. Read `AKOS_MANIFEST.yaml`.
3. Read `BUILD_INDEX.md`.
4. Read `CURRENT_STATE.md`.
5. Read `manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json` when tools, repositories, execution, or receipts are involved.
6. Read `finisher/out/FINISH_QUEUE.md` when present.
7. Close finishable work before proposing expansion.
8. Discover the existing route before declaring a capability missing.
9. Read the active spec relevant to the task.
10. Apply `AKOS-OC-001` whenever tools, target-system actions, verification, or persistence are involved.
11. Preserve history and append deltas.

## Operating Principle

Build in layers. Preserve history. Promote stable objects. Mark superseded objects historical. Never hide drift. Never confuse a mirror with the source of truth. Never confuse a wrong-plane failure with missing infrastructure. Reuse before rebuild. Finish before expansion. Never report closure without a receipt.
