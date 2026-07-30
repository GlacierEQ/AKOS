# AKOS — Apex Knowledge Operating System

[![AKOS Verification](https://github.com/GlacierEQ/AKOS/actions/workflows/ci.yml/badge.svg)](https://github.com/GlacierEQ/AKOS/actions/workflows/ci.yml)

**Version:** `0.6.1`  
**Canonical repository:** `GlacierEQ/AKOS`  
**Verification state:** `PARTIALLY_VERIFIED` until this repository-native CI change is merged and revalidated on `main`  
**Evidence target:** `TEST`

AKOS is the governance and operational-cognition layer for large, interconnected engineering systems. It converts identity, provenance, authority, execution, verification, persistence, and completion from informal expectations into inspectable contracts and executable behavior.

<!-- README-MESH:BEGIN -->

## For recruiters and non-technical reviewers

### What AKOS accomplishes

A sophisticated tool collection can still fail as a system: work may be duplicated, actions may happen in the wrong place, drafts may be reported as completion, and corrections may disappear between sessions. AKOS addresses that coordination failure.

It gives a large portfolio one durable operating model without flattening the projects inside it:

- every important object has a stable identity and provenance;
- plans, actions, verification, persistence, and completion are different states;
- safe work can proceed under explicit standing authority;
- high-risk or irreversible work remains gated;
- corrections become policy, executable guards, regression tests, and receipts;
- incomplete work reports its exact missing stage instead of an invented percentage.

### Why the design matters

AKOS demonstrates systems architecture beyond a single application. It shows how governance can become code, how trust can become an evidence property, and how a portfolio can improve recursively without rewriting history or obscuring responsibility.

### Proof in 60 seconds

| Open or run | What it demonstrates |
|---|---|
| [`specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md`](specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md) | Durable operating laws and non-negotiable system invariants. |
| [`operational_cognition/execution_authority.py`](operational_cognition/execution_authority.py) | Deterministic execute, confirm, or block decisions. |
| [`operational_cognition/engine.py`](operational_cognition/engine.py) | Evidence classes, work routing, phase receipts, and completion logic. |
| [`finisher/finisher.py`](finisher/finisher.py) | Finish-first analysis and explicit blocker handling. |
| [`manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`](manifests/runtime/AKOS_OPERATIONAL_COGNITION.json) | Machine-readable execution and completion policy. |
| [`scripts/verify_repository.py`](scripts/verify_repository.py) | Positive-count test execution and atomic verification receipt. |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Repository-native verification across Python 3.11, 3.12, and 3.13. |

## For senior engineers and domain experts

### System boundary

AKOS owns:

- canonical identity and provenance rules;
- authority and confirmation policy;
- source and capability routing;
- evidence-backed maturity transitions;
- execution, validation, persistence, and handoff semantics;
- artifact-closure stages and exact blocker reporting;
- correction-to-policy persistence;
- governance contracts for connected repositories and agents.

AKOS does **not** claim that a declared integration is connected, that a connected provider is authorized, or that a designed workflow has executed. Those transitions require their own receipts.

### Architecture

```text
Prime purpose + foundational laws
                │
                ▼
       Canonical object model
 identity • provenance • relationships
                │
        ┌───────┴────────┐
        ▼                ▼
Operational cognition   Maturity + closure
route • decide • act     measure • gate • finish
        │                │
        └───────┬────────┘
                ▼
Execution authority + provider boundary
 execute • confirm • block • verify
                │
                ▼
Canonical persistence + append-only receipts
```

The architecture separates five concerns that are often collapsed:

1. **Canonical source** — the authoritative object or record.
2. **Execution plane** — the system capable of changing the target state.
3. **Control plane** — policy governing whether and how work proceeds.
4. **Receipt plane** — evidence that an action occurred and was validated.
5. **Projection plane** — human and machine views that never replace the source.

### Core innovations

1. **One truth, many views** — canonical objects can have multiple projections without losing identity.
2. **Execution without redundant permission** — beneficial, objective-preserving, recoverable work can proceed within standing authority.
3. **Receipt-backed completion** — plans and drafts cannot masquerade as changed state.
4. **System-first routing** — existing planes are discovered and reused before new infrastructure is invented.
5. **Correction-to-cognition** — operator corrections become durable law, runtime behavior, tests, and ledger entries.
6. **Artifact closure** — exact missing stages replace subjective completion percentages.
7. **Monotonic maturity** — evidence states advance through explicit transitions and cannot silently regress.

### Runtime components

| Component | Responsibility |
|---|---|
| [`operational_cognition/engine.py`](operational_cognition/engine.py) | Work models, routing, evidence classes, phase receipts, and completion decisions. |
| [`operational_cognition/execution_authority.py`](operational_cognition/execution_authority.py) | Standing-authority and confirmation-trigger evaluation. |
| [`operational_cognition/topology.py`](operational_cognition/topology.py) | Architecture discovery and correct-plane routing. |
| [`operational_cognition/maturity.py`](operational_cognition/maturity.py) | Evidence-backed capability maturity and artifact closure. |
| [`operational_cognition/master_strand.py`](operational_cognition/master_strand.py) | Branch assessment, extinction gates, and canonical-strand decisions. |
| [`finisher/finisher.py`](finisher/finisher.py) | Finish-first work classification and closure planning. |
| [`src/verify_manifest.py`](src/verify_manifest.py) | Machine-readable manifest validation. |
| [`scripts/verify_repository.py`](scripts/verify_repository.py) | Test discovery, positive-count enforcement, and receipt generation. |

### Correctness and failure behavior

- A plan is not execution.
- Execution without a provider receipt cannot establish a provider-side change.
- Validation without persistence cannot establish durable completion.
- Irreversible operations require explicit approval.
- Unauthorized writes are blocked.
- Pipeline and artifact stages reject regression.
- Architect assertions remain active claims but are not auto-promoted to verified facts.
- Missing test modules fail verification.
- A runner that executes zero tests returns `UNVERIFIED`, even with exit code zero.
- Test failures or import errors return `FAILED`.
- Receipts are written atomically so a stale success cannot survive a failed rerun.
- Machine-local paths are rejected from the public README contract.

### Build and verification

```bash
# Install the runtime and verification tooling
python -m pip install -e ".[dev]"

# Static quality
ruff check operational_cognition finisher src scripts tests
python -m compileall -q operational_cognition finisher src scripts tests

# Verify the three-audience README contract
python scripts/verify_readme_contract.py

# Run every AKOS unittest module and emit a positive-count receipt
python scripts/verify_repository.py --output artifacts/ci/test-receipt.json
```

The receipt schema is `glaciereq.akos.test-receipt.v1`. It records the commit, Python version, discovered modules, test count, failures, errors, skips, evidence level, and conclusion.

### Language fit

| Language / format | Responsibility | Boundary | Proof |
|---|---|---|---|
| Python 3.11+ | Operational cognition, authority, topology, maturity, closure, and verification | Executable runtime and test tooling | Three-version CI plus positive-count unittest receipt |
| JSON | Runtime manifests, topology, maturity, and receipt interchange | Machine-readable policy and evidence records | Parsing and contract tests |
| YAML | Canonical AKOS manifest and operator-readable configuration | Human-editable system declaration | Manifest verification tests |
| Markdown | Laws, specifications, ADRs, ledgers, and three-audience communication | Human governance and review surface | README contract gate and link-visible evidence |

The repository remains intentionally Python-centered. Additional languages belong only where a workload, safety property, interoperability boundary, or performance requirement creates a measurable advantage.

### Evidence-backed operating rules

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

Capabilities move through observable states:

```text
DECLARED -> DISCOVERED -> CONNECTED -> AUTHENTICATED -> AUTHORIZED ->
INVOKED -> RETURNED -> VERIFIED -> PERSISTED
```

Artifacts move through closure stages:

```text
LOCATED -> ACQUIRED -> HASHED -> PRESERVED -> PARSED -> CLASSIFIED ->
CORRELATED -> DRAFTED -> VERIFIED -> PACKAGED -> STORED -> LOGGED -> READY_FOR_USE
```

Unmeasured means `UNASSESSED`, not an invented score.

## For AI systems and toolchains

### Machine contract

```yaml
schema: glaciereq.readme.v1
profile: glaciereq.readme-impact.v2-draft
repository: GlacierEQ/AKOS
canonical_branch: main
purpose: >-
  Govern identity, provenance, authority, execution, verification,
  persistence, completion, and recursive system improvement.
status:
  state: PARTIALLY_VERIFIED
  target_evidence: TEST
  promotion_rule: >-
    Promote only after repository-native CI passes with a positive test count
    and the canonical main branch revalidates the receipt.
  verified_scope:
    - foundational laws and architecture contracts are present
    - executable operational-cognition and finisher modules are present
    - repository-native verification code is reviewable in source
  blocked_scope:
    - provider-side integrations without current provider receipts
    - irreversible actions without explicit approval
    - deployment or scale claims without environment-specific evidence
  unverified_scope:
    - current canonical-main test result until this CI change is merged
    - external connectors not exercised by repository-native tests
interfaces:
  inputs:
    - work items and authority context
    - capability and topology declarations
    - evidence and provider receipts
    - runtime and maturity manifests
  outputs:
    - execute, confirm, block, or complete decisions
    - capability and artifact maturity results
    - exact blockers and missing closure stages
    - atomic test receipts
  commands:
    install: python -m pip install -e ".[dev]"
    lint: ruff check operational_cognition finisher src scripts tests
    test: python scripts/verify_repository.py --output artifacts/ci/test-receipt.json
    verify_readme: python scripts/verify_readme_contract.py
evidence:
  workflow: .github/workflows/ci.yml
  test_runner: scripts/verify_repository.py
  receipt_schema: glaciereq.akos.test-receipt.v1
  tests:
    - operational_cognition/test_*.py
    - finisher/test_*.py
    - tests/test_*.py
relationships:
  - target: GlacierEQ/job-app-helix
    relation: GOVERNS
    combined_value: >-
      AKOS supplies authority, provenance, and completion semantics;
      Job-App Helix supplies exact portfolio representation and evidence rollout.
  - target: GlacierEQ/anthropic-agent-coordinator
    relation: GOVERNS
    combined_value: >-
      Agent motion receives bounded authority, persistence, and completion rules.
  - target: GlacierEQ/anthropic-safety-monitor
    relation: GOVERNS
    combined_value: >-
      Independent monitoring signals feed explicit review and blocking decisions.
  - target: GlacierEQ/spacex-mission-control
    relation: GOVERNS
    combined_value: >-
      Mission-state orchestration inherits evidence and completion boundaries.
limits:
  - Architecture does not establish provider connectivity.
  - A relationship does not prove the target repository currently works.
  - CI verifies repository-local behavior, not external deployment or scale.
```

### Canonical machine resources

- [`AKOS_MANIFEST.yaml`](AKOS_MANIFEST.yaml)
- [`manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`](manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json)
- [`manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`](manifests/runtime/AKOS_OPERATIONAL_COGNITION.json)
- [`manifests/runtime/AKOS_OPERATIONAL_MATURITY.json`](manifests/runtime/AKOS_OPERATIONAL_MATURITY.json)
- [`schemas/operational_cognition.schema.json`](schemas/operational_cognition.schema.json)
- [`schemas/operational_maturity.schema.json`](schemas/operational_maturity.schema.json)
- [`contracts/`](contracts/)
- [`specs/`](specs/)

<!-- README-MESH:END -->

## Repository map

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
/scripts/                  repository-native verification tooling
```

## Start here

1. Read [`AKOS_MANIFEST.yaml`](AKOS_MANIFEST.yaml).
2. Read [`BUILD_INDEX.md`](BUILD_INDEX.md) and [`CURRENT_STATE.md`](CURRENT_STATE.md).
3. Inspect [`manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`](manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json) before diagnosing a missing route.
4. Apply [`AKOS-OC-001`](specs/AKOS-OC-001_OPERATIONAL_COGNITION.md) to execution and [`AKOS-OC-002`](specs/AKOS-OC-002_OPERATIONAL_MATURITY.md) to maturity or closure claims.
5. Run the repository-native verification commands.
6. Close finishable work before proposing expansion.
7. Preserve history and append evidence-backed deltas.

## Repository workflow

`GlacierEQ/AKOS` is a single-operator canonical repository. Coherent, reversible, verified improvements may commit directly to `main`; branches and pull requests are used when an independent verification or review gate materially improves confidence.

Rollback uses additive correction or `git revert`. Canonical history is not silently rewritten.

## Operating principle

Build in layers. Preserve history. Reuse before rebuilding. Finish before expanding. Verify before claiming. Persist before reporting closure. Never confuse a mirror with the source of truth, a wrong-plane failure with missing infrastructure, or a compelling explanation with completed work.
