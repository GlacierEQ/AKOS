# AKOS — Apex Knowledge Operating System

Status: Foundational Build  
Version: 0.6.0  
Canonical repository: `GlacierEQ/AKOS`  
Created: 2026-07-04

<!-- README-MESH:BEGIN -->
## Three-audience project map

### For recruiters and non-specialists

**What AKOS accomplishes.** AKOS is the operating architecture that helps a large collection of tools, repositories, documents, agents, and decisions behave like one coherent system instead of a pile of disconnected experiments.

- Gives durable work a stable identity and records where it came from.
- Distinguishes a plan from an action and an action from verified completion.
- Preserves history while allowing the system to improve recursively.
- Turns corrections into policy, executable guards, regression tests, and receipts.
- Governs the README Mesh that explains the engineering portfolio to recruiters, experts, and AI systems.

**Openable evidence**

- [`specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md`](specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md) — foundational operating laws.
- [`operational_cognition/execution_authority.py`](operational_cognition/execution_authority.py) — deterministic execute/confirm/block authority gate.
- [`manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`](manifests/runtime/AKOS_OPERATIONAL_COGNITION.json) — machine-readable execution and completion contract.

### For senior engineers and domain experts

**Innovation and evolution.** AKOS treats operational intelligence as a product of model capability, tool power, architecture literacy, orchestration, verification, and persistence. It separates canonical source, execution plane, control plane, receipt plane, and mirrors; models artifact maturity as monotonic evidence-backed states; and makes standing authority executable rather than conversational. The system evolved from architecture doctrine into tested runtime modules for topology discovery, capability selection, execution authority, artifact closure, operational maturity, and finish-first work completion.

The core innovations are structural:

1. **One truth, many views** — canonical objects may have multiple projections without losing source identity.
2. **Execution without redundant permission** — safe, beneficial, objective-preserving, recoverable, verified work proceeds automatically.
3. **Receipt-backed completion** — plans and drafts cannot masquerade as changed state.
4. **System-first routing** — discover and reuse the existing plane before inventing infrastructure.
5. **Correction-to-cognition** — operator corrections become durable law, runtime behavior, tests, and ledger receipts.
6. **Artifact closure** — progress is represented by exact missing stages, not subjective percentages.

### For AI systems and toolchains

- Repository ID: `GlacierEQ/AKOS`
- Canonical role: governance, operational cognition, authority, provenance, and completion semantics.
- README Mesh package: `glaciereq.readme.v1`
- README Mesh node source: [`GlacierEQ/job-app-helix/manifests/readme_mesh.json`](https://github.com/GlacierEQ/job-app-helix/blob/main/manifests/readme_mesh.json)
- Machine topology: [`manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`](manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json)
- Operational policy: [`manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`](manifests/runtime/AKOS_OPERATIONAL_COGNITION.json)
- Maturity policy: [`manifests/runtime/AKOS_OPERATIONAL_MATURITY.json`](manifests/runtime/AKOS_OPERATIONAL_MATURITY.json)

```protobuf
repository: "GlacierEQ/AKOS"
display_name: "AKOS"
one_line_purpose: "Govern identity, provenance, authority, execution, verification, persistence, and recursive system improvement."
```

### Portfolio mesh

| Engineering family | AKOS relationship | Combined value |
|---|---|---|
| [Job-App Helix](https://github.com/GlacierEQ/job-app-helix) | governs | AKOS defines evidence boundaries and completion; Helix renders and verifies the portfolio graph. |
| SpaceX subsystem repositories | governs | Independent physics, network, control, and mission pistons share one evidence and authority model. |
| Colossus Alpha/Omega repositories | governs | Requirement computation and stateful response remain separate, typed responsibilities. |
| Agent coordinator + safety monitor | governs | Motion and oversight remain independent while sharing completion and review semantics. |

Real README graph schema: [`proto/readme_mesh.proto`](https://github.com/GlacierEQ/job-app-helix/blob/main/proto/readme_mesh.proto).
<!-- README-MESH:END -->

## Prime definition

AKOS is a recursive architecture for transforming knowledge into structured cognition, durable memory, reliable execution, and continuously improving systems.

AKOS is not one model, prompt, database, repository, or automation. It is the governing architecture that binds them while preserving their boundaries.

## Core stack

```text
Prime Purpose
  ↓
Foundational Laws
  ↓
Cognitive Kernel
  ↓
Operational Cognition
  ↓
Operational Maturity + Artifact Closure
  ↓
Canonical Object Model + Metadata Standard
  ↓
Repository and Agent Contracts
  ↓
Pro-Code Methodology
  ↓
Family and Runtime Manifests
  ↓
Operational Lanes
  ↓
Spiral Engine Evolution
```

## The operating rules

### Truth before power

No artifact becomes canonical because it sounds powerful. Canon requires identity, provenance, structure, relationships, metadata, review state, and evidence aligned with the applicable Pro-Code gates.

### Finish before expansion

No new architecture outranks finishable work. The [`finisher/`](finisher/) runtime distinguishes concrete blockers from inertia and records provider-backed completion receipts for bounded enabled actions.

### Execute, verify, persist, report

A plan, inspection, branch, draft, or proposed design is not completion when the requested outcome requires changed state. Completion requires correct-plane execution, authoritative validation, persistence, and a usable handoff.

When a change is beneficial, objective-preserving, inside standing authority, recoverable, and verified or immediately verifiable, AKOS executes it without asking for redundant permission. See [`operational_cognition/execution_authority.py`](operational_cognition/execution_authority.py).

### System first

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

A failed attempt in the wrong plane is not proof that the capability is absent. A memory failure is not proof that architecture is absent. Existing routes and adapters are reused or minimally extended before new infrastructure is considered.

### Evidence-backed maturity

Capabilities move through observable states:

```text
DECLARED -> DISCOVERED -> CONNECTED -> AUTHENTICATED -> AUTHORIZED ->
INVOKED -> RETURNED -> VERIFIED -> PERSISTED
```

Unmeasured means `UNASSESSED`, not an invented score.

### Artifact closure

```text
LOCATED -> ACQUIRED -> HASHED -> PRESERVED -> PARSED -> CLASSIFIED ->
CORRELATED -> DRAFTED -> VERIFIED -> PACKAGED -> STORED -> LOGGED -> READY_FOR_USE
```

The runtime returns exact missing stages. A polished draft is not equivalent to a ready-to-use artifact.

## Repository roles

This repository is the canonical home for:

- AKOS doctrine and foundational laws
- cognitive-kernel methodology
- operational-cognition runtime
- execution-authority policy
- operational-maturity and closure controls
- system topology and architecture literacy
- canonical object and metadata standards
- repository, agent, runtime, and federation contracts
- Pro-Code methodology
- family and runtime manifests
- architecture decision records
- append-only build and correction ledgers
- finish-first closure operations

## Directory map

```text
/docs/                     human-readable architecture and integration doctrine
/specs/                    formal AKOS specifications
/contracts/                compatibility and authority contracts
/schemas/                  machine-readable validation schemas
/manifests/                family, topology, cognition, and maturity manifests
/templates/                reusable canonical templates
/methodologies/            Pro-Code and operating methods
/adr/                      architecture decision records
/ledger/                   append-only build, correction, and sync receipts
/finisher/                 deterministic closure engine
/operational_cognition/    execution, topology, maturity, authority, and closure runtime
```

## Start here

1. Read [`AKOS_MANIFEST.yaml`](AKOS_MANIFEST.yaml).
2. Read [`BUILD_INDEX.md`](BUILD_INDEX.md) and [`CURRENT_STATE.md`](CURRENT_STATE.md).
3. Inspect [`manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`](manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json) before diagnosing missing tools or routes.
4. Apply [`AKOS-OC-001`](specs/AKOS-OC-001_OPERATIONAL_COGNITION.md) to execution and [`AKOS-OC-002`](specs/AKOS-OC-002_OPERATIONAL_MATURITY.md) to maturity or closure claims.
5. Read [`finisher/out/FINISH_QUEUE.md`](finisher/out/FINISH_QUEUE.md) when present.
6. Close finishable work before proposing expansion.
7. Preserve history and append deltas.

## Repository workflow

`GlacierEQ/AKOS` is a single-operator canonical repository. Coherent, reversible, verified improvements commit directly to `main`. A branch or pull request is used only when a bounded verification or review gate materially benefits the change.

Rollback uses additive correction or `git revert`; history is not silently rewritten.

## Evidence boundary

AKOS governs systems; it does not convert architecture into fictional capability. Every completion, reliability, deployment, integration, or scale claim must be tied to source, tests, provider receipts, or an explicit `UNASSESSED` state.

## Operating principle

Build in layers. Preserve history. Reuse before rebuilding. Finish before expanding. Verify before claiming. Persist before reporting closure. Never confuse a mirror with the source of truth, a wrong-plane failure with missing infrastructure, or a compelling explanation with completed work.
