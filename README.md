# AKOS — Apex Knowledge Operating System

[![AKOS Verification](https://github.com/GlacierEQ/AKOS/actions/workflows/ci.yml/badge.svg)](https://github.com/GlacierEQ/AKOS/actions/workflows/ci.yml)
[![AKOS Integrity Gate](https://github.com/GlacierEQ/AKOS/actions/workflows/integrity.yml/badge.svg)](https://github.com/GlacierEQ/AKOS/actions/workflows/integrity.yml)

**Version:** `0.6.1`  
**Canonical repository:** `GlacierEQ/AKOS`  
**Verification state:** `VERIFIED` at evidence level `TEST` for the current reviewed revision  
**Verified matrix:** Python `3.11`, `3.12`, and `3.13`  
**Observed result:** `57 tests`, `0 failures`, `0 errors`, `0 skipped` per interpreter

AKOS is the governance and operational-cognition layer for large, interconnected engineering systems. It converts identity, provenance, authority, execution, verification, persistence, and completion from informal expectations into inspectable contracts and executable behavior.

<!-- README-MESH:BEGIN -->

## For recruiters and non-technical reviewers

### What AKOS accomplishes

A sophisticated collection of tools can still fail as a system: work gets duplicated, actions happen in the wrong place, drafts are reported as completion, and important corrections disappear between sessions. AKOS addresses that coordination failure.

It gives a large engineering portfolio one durable operating model without flattening the individual projects inside it:

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
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Repository-native verification across three Python versions. |
| [`.github/workflows/integrity.yml`](.github/workflows/integrity.yml) | Adversarial integrity tests and Git-anchor verification. |

### Evidence summary

The current promotion receipt establishes repository-local behavior at the `TEST` level:

- 10 discovered test modules;
- 57 executed tests per Python version;
- 3 supported interpreter versions;
- 0 failures, errors, or skips;
- README contract verified;
- all tracked Python files compiled by the independent integrity gate;
- checkout verified against the Git anchor.

It does **not** claim that external providers are connected, that deployment scale has been measured, or that every declared integration has been exercised.

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

AKOS does **not** convert a declared integration into a connected one, a connected provider into an authorized one, or an architecture diagram into executed state. Those transitions require their own receipts.

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

The architecture separates five concerns that are frequently collapsed:

1. **Canonical source** — the authoritative object or record.
2. **Execution plane** — the system capable of changing target state.
3. **Control plane** — policy governing whether and how work proceeds.
4. **Receipt plane** — evidence that an action occurred and was validated.
5. **Projection plane** — human and machine views that never replace the source.

### Core innovations

1. **One truth, many views** — canonical objects can have multiple projections without losing identity.
2. **Execution without redundant permission** — beneficial, objective-preserving, recoverable work can proceed within standing authority.
3. **Receipt-backed completion** — plans and drafts cannot masquerade as changed state.
4. **System-first routing** — existing planes are discovered and reused before infrastructure is invented.
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
- Receipts are written atomically so stale success cannot survive a failed rerun.
- Machine-local paths are rejected from the public README contract.

### Build and verification

```bash
# Install runtime and verification tooling
python -m pip install -e ".[dev]"

# Strictly lint the new verification control surface
ruff check scripts/verify_repository.py scripts/verify_readme_contract.py

# Record, rather than conceal, preexisting quality debt
mkdir -p artifacts/ci
ruff check operational_cognition finisher src tests \
  --output-format json > artifacts/ci/ruff-baseline.json || true

# Compile executable surfaces
python -m compileall -q operational_cognition finisher src scripts tests

# Verify the three-audience README contract
python scripts/verify_readme_contract.py

# Run every AKOS unittest module and emit a positive-count receipt
python scripts/verify_repository.py --output artifacts/ci/test-receipt.json
```

The test receipt schema is `glaciereq.akos.test-receipt.v1`. It records the commit, Python version, discovered modules, test count, failures, errors, skips, evidence level, and conclusion.

The initial strict audit of the preexisting runtime recorded **117 Ruff findings** in `glaciereq.akos.ruff-baseline.v1`. That debt is visible and versioned, but it is not misrepresented as a runtime failure: bytecode compilation, 57 behavioral tests, and the independent integrity gate all pass. New verification code is held to a zero-warning strict gate.

### Verification layers

| Layer | Gate | Current result |
|---|---|---|
| Packaging | Editable installation with explicit dependencies | Passed on Python 3.11–3.13 |
| New control-plane quality | Strict Ruff on verification scripts | Passed |
| Legacy quality baseline | Full Ruff JSON report | 117 findings recorded |
| Syntax/importability | `compileall` plus integrity compile-all | Passed |
| README contract | Recruiter → expert → AI order and portability | Passed |
| Runtime behavior | Positive-count unittest receipt | 57/57 passed per interpreter |
| Integrity | Adversarial tests plus Git-anchor verification | Passed |
| Deployment/scale | Environment-specific evidence | Not claimed |

### Language fit

| Language / format | Responsibility | Boundary | Proof |
|---|---|---|---|
| Python 3.11+ | Operational cognition, authority, topology, maturity, closure, and verification | Executable runtime and test tooling | Three-version CI plus positive-count unittest receipt |
| JSON | Runtime manifests, topology, maturity, and receipt interchange | Machine-readable policy and evidence records | Parsing and contract tests |
| YAML | Canonical AKOS manifest and operator-readable configuration | Human-editable system declaration | Manifest verification tests |
| Markdown | Laws, specifications, ADRs, ledgers, and three-audience communication | Human governance and review surface | README contract gate and openable evidence |

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
  state: VERIFIED
  evidence_level: TEST
  verification_matrix:
    python: ["3.11", "3.12", "3.13"]
    tests_per_interpreter: 57
    test_modules: 10
    failures: 0
    errors: 0
    skipped: 0
  quality_baseline:
    schema: glaciereq.akos.ruff-baseline.v1
    preexisting_findings: 117
    treatment: recorded_nonblocking_debt
  verified_scope:
    - editable package installation and declared dependencies
    - strict quality gate for newly introduced verification code
    - compilation of executable and tracked Python surfaces
    - repository-local operational-cognition, finisher, connector, and manifest tests
    - recruiter, expert, and AI README contract
    - adversarial integrity tests and Git-anchor verification
  blocked_scope:
    - irreversible actions without explicit approval
    - provider-side operations without current provider receipts
  unverified_scope:
    - external connectors not exercised by repository-local tests
    - deployment, performance, reliability, and scale outside GitHub Actions
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
    - atomic test and quality-baseline receipts
  commands:
    install: python -m pip install -e ".[dev]"
    lint_new_code: ruff check scripts/verify_repository.py scripts/verify_readme_contract.py
    compile: python -m compileall -q operational_cognition finisher src scripts tests
    test: python scripts/verify_repository.py --output artifacts/ci/test-receipt.json
    verify_readme: python scripts/verify_readme_contract.py
evidence:
  workflow: .github/workflows/ci.yml
  integrity_workflow: .github/workflows/integrity.yml
  test_runner: scripts/verify_repository.py
  receipt_schema: glaciereq.akos.test-receipt.v1
  quality_schema: glaciereq.akos.ruff-baseline.v1
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
  - Recorded lint debt is not represented as remediated.
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
