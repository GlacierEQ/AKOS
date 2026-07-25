# AKOS — Apex Knowledge Operating System

Status: Foundational Build
Version: 0.5.1
Canonical Repo: `GlacierEQ/AKOS`
Created: 2026-07-04

## Prime Definition

AKOS is the Apex Knowledge Operating System: a recursive architecture for transforming knowledge into structured cognition, durable memory, reliable execution, and continuously improving systems.

AKOS is not one model, one prompt, one database, one repository, or one automation.

AKOS is the governing architecture that binds them.

## Direct-to-Main Rule

`GlacierEQ/AKOS` is a single-operator public canonical repository.

Changes commit directly to `main`. Branches and pull requests are not the default workflow and may be created only when the operator explicitly requests them or when a bounded verification/review gate is required before canonical integration.

Verification happens through provider readback, the read-only AKOS repository-local integrity gate, the public execution face for governed cross-repository workloads, immutable receipts where required, and additive correction or `git revert` when rollback is required.

A generic team-development convention does not outrank the operator's repository model.

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
Operational Maturity
↓
Architecture Literacy
↓
Artifact Closure
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

The executable `finisher/` module scans an allowlisted queue of near-complete pull requests when a repository actually uses pull requests, distinguishes concrete blockers from inertia, blocks expansion when closure is available, and records provider-backed completion receipts. It may execute only bounded, explicitly enabled actions.

See `finisher/README.md`.

## Operational Cognition Rule

Model capability and tool access are potential. AKOS operational power requires tool literacy, architecture literacy, orchestration, verification, and persistence.

A plan, inspection, draft, or proposed design is not completion when the requested outcome requires a target-system action. Completion requires architecture discovery, correct-plane execution, authoritative validation, a provider receipt when applicable, a durable ledger receipt, and a final handoff.

See `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md` and `operational_cognition/README.md`.

## Operational Maturity Rule

AKOS does not convert confidence, ambition, or architectural complexity into an unsupported `1–10` score.

Every capability moves through distinct truth states:

```text
DECLARED -> DISCOVERED -> CONNECTED -> AUTHENTICATED -> AUTHORIZED ->
INVOKED -> RETURNED -> VERIFIED -> PERSISTED
```

Every scorecard separates:

- **available ceiling** — sourced capability that is actually available;
- **demonstrated reliability** — capability exercised to the required evidence level;
- **operational gap** — the difference between them;
- **missing controls** — exact work required next.

Unmeasured means `UNASSESSED`, not an invented number.

See `specs/AKOS-OC-002_OPERATIONAL_MATURITY.md` and `manifests/runtime/AKOS_OPERATIONAL_MATURITY.json`.

## System-First Rule

AKOS must understand the existing system before declaring a blocker or proposing infrastructure.

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

A failed attempt in the wrong plane is not proof that the correct plane is missing. A memory failure is not proof that the architecture is absent. When an execution plane already exists, AKOS reuses it or adds one bounded catalog action, adapter, or route binding before considering new infrastructure.

For governed private GitHub workloads:

```text
GlacierEQ/AKOS
  -> exact main commit + metadata-only job
GlacierEQ/public-actions-runner-host
  -> public execution face
GlacierEQ/llm-runner-teams
  -> private control and immutable receipts
```

Public AKOS may own read-only repository-local verification workflows under `docs/architecture/PUBLIC_ACTION_FACE.md`. It may not execute governed cross-repository workloads, receive bridge credentials, deploy, or create action-face claims and receipts.

See `docs/operational_cognition/SYSTEM_FIRST_MENTALITY.md` and `manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`.

## Artifact Closure Rule

```text
LOCATED -> ACQUIRED -> HASHED -> PRESERVED -> PARSED -> CLASSIFIED ->
CORRELATED -> DRAFTED -> VERIFIED -> PACKAGED -> STORED -> LOGGED -> READY_FOR_USE
```

A good draft is not complete. Stages `VERIFIED` through `LOGGED` are mandatory release controls, but closure still requires `READY_FOR_USE`.

The system returns exact missing stages rather than a vague completion percentage.

## Repository Purpose

This repository is the canonical architecture home for:

- AKOS doctrine
- Cognitive Kernel methodology
- Operational Cognition runtime
- Operational maturity controls and scorecards
- System topology and architecture literacy
- Artifact closure gates
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
/operational_cognition/    Execution, topology, maturity, and closure runtime
```

## Active Specs

- `AKOS-CK-001` — Cognitive Kernel
- `AKOS-OC-001` — Operational Cognition
- `AKOS-OC-002` — Operational Maturity and Closure
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
5. Commit AKOS changes directly to `main` unless the operator explicitly requests a branch or pull request, or a bounded verification/review gate is required before canonical integration.
6. Read `manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json` when tools, repositories, execution, or receipts are involved.
7. Read `manifests/runtime/AKOS_OPERATIONAL_MATURITY.json` when capability, score, reliability, closure, or comparative claims are involved.
8. Read `finisher/out/FINISH_QUEUE.md` when present.
9. Close finishable work before proposing expansion.
10. Discover the existing route before declaring a capability missing.
11. Read the active spec relevant to the task.
12. Apply `AKOS-OC-001` to tool actions and `AKOS-OC-002` to capability or closure assessments.
13. Preserve history and append deltas.

## Operating Principle

Build in layers. Preserve history. Promote stable objects. Mark superseded objects historical. Never hide drift. Never confuse a mirror with the source of truth. Never confuse a wrong-plane failure with missing infrastructure. Never convert confidence into an unsupported score. Commit directly to the canonical mainline. Reuse before rebuild. Finish before expansion. Never report closure without a receipt.

---

## Fleet ops (transparent)

This repo may include **`.integrity/`** (SHA-256 baselines / watchdog) and/or a health sidecar.
These are **documented multi-repo fleet operations**, not covert implants.

See [SECURITY_AND_FLEET_OPS.md](SECURITY_AND_FLEET_OPS.md) and
`~/GlacierEQ_Swarm/state/PORTFOLIO_SHADOW_AND_GAUNTLET.md`.

## Helix strand

See [HELIX_STRAND.md](HELIX_STRAND.md) — piston/spiral role in the portfolio double helix.
