# AKOS — Apex Knowledge Operating System

[![AKOS Verification](https://github.com/GlacierEQ/AKOS/actions/workflows/ci.yml/badge.svg)](https://github.com/GlacierEQ/AKOS/actions/workflows/ci.yml)
[![AKOS Integrity Gate](https://github.com/GlacierEQ/AKOS/actions/workflows/integrity.yml/badge.svg)](https://github.com/GlacierEQ/AKOS/actions/workflows/integrity.yml)

**Version:** `0.6.1`  
**Canonical repository:** `GlacierEQ/AKOS`  
**Verification state:** `VERIFIED` at evidence level `TEST` for the current reviewed revision  
**Verified matrix:** Python `3.11`, `3.12`, and `3.13`  
**Observed result:** `94 collected`, `94 passed`, `12 modules`, `0 failures`, `0 errors`, `0 skips`

AKOS is the governance and operational-cognition layer for large, interconnected engineering systems. It converts identity, provenance, authority, execution, verification, persistence, and completion from informal expectations into inspectable contracts and executable behavior.

<!-- README-MESH:BEGIN -->

## For recruiters and non-technical reviewers

### What AKOS accomplishes

A sophisticated collection of tools can still fail as a system: work gets duplicated, actions happen in the wrong place, drafts are reported as completion, and corrections disappear between sessions. AKOS addresses that coordination failure.

It gives a large engineering portfolio one durable operating model without flattening the projects inside it:

- every important object has a stable identity and provenance;
- plans, actions, verification, persistence, and completion are different states;
- safe and recoverable work can proceed under explicit standing authority;
- high-risk or irreversible work remains gated;
- corrections become policy, executable guards, regression tests, and receipts;
- incomplete work reports its exact missing stage instead of an invented percentage.

### Why it matters

AKOS demonstrates systems architecture beyond a single application. It shows how governance becomes code, how trust becomes an evidence property, and how a portfolio improves recursively without rewriting history or obscuring responsibility.

### Proof in 60 seconds

| Open or run | What it demonstrates |
|---|---|
| [`specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md`](specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md) | Durable operating laws and system invariants. |
| [`operational_cognition/execution_authority.py`](operational_cognition/execution_authority.py) | Deterministic execute, confirm, or block decisions. |
| [`operational_cognition/engine.py`](operational_cognition/engine.py) | Evidence classes, routing, phase receipts, and completion logic. |
| [`finisher/finisher.py`](finisher/finisher.py) | Finish-first analysis and exact blocker handling. |
| [`scripts/verify_repository.py`](scripts/verify_repository.py) | Exhaustive pytest collection and atomic proof receipts. |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Three-version package, contract, and behavioral verification. |
| [`.github/workflows/integrity.yml`](.github/workflows/integrity.yml) | Adversarial integrity tests and Git-anchor verification. |
| [`ledger/2026-07-30_FINISHER_ACTION_BOUNDARY.md`](ledger/2026-07-30_FINISHER_ACTION_BOUNDARY.md) | Evidence-backed migration of secret-bearing execution to the correct plane. |

### Evidence summary

The current promotion receipt establishes repository-local behavior at the `TEST` level:

- 12 discovered modules across integrity, operational cognition, Finisher, manifests, and verifier tooling;
- 94 collected and executed tests on each supported Python version;
- 94 passes with no failures, errors, skips, collection errors, or internal errors;
- editable installation with explicit dependencies and installed verification commands;
- strict zero-warning lint for the new verification control surface;
- compilation of executable and tracked Python surfaces;
- recruiter → expert → AI README contract verification;
- read-only workflow-policy enforcement and Git-anchor verification.

It does **not** claim external-provider connectivity, deployment scale, production reliability, or exercised behavior outside repository-local CI.

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

The architecture separates concerns that are commonly collapsed:

1. **Canonical source** — the authoritative object or record.
2. **Execution plane** — the system capable of changing target state.
3. **Control plane** — policy governing whether and how work proceeds.
4. **Receipt plane** — evidence that an action occurred and was validated.
5. **Projection plane** — human and machine views that never replace the source.

### Core innovations

1. **One truth, many views** — canonical objects support multiple projections without losing identity.
2. **Execution without redundant permission** — beneficial, objective-preserving, recoverable work can proceed within standing authority.
3. **Receipt-backed completion** — plans and drafts cannot masquerade as changed state.
4. **System-first routing** — existing planes are discovered and reused before infrastructure is invented.
5. **Correction-to-cognition** — corrections become durable law, runtime behavior, tests, and ledger entries.
6. **Artifact closure** — exact missing stages replace subjective completion percentages.
7. **Monotonic maturity** — evidence states advance through explicit transitions and cannot silently regress.

### Runtime map

| Component | Responsibility |
|---|---|
| [`operational_cognition/engine.py`](operational_cognition/engine.py) | Work models, routing, evidence classes, phase receipts, and completion decisions. |
| [`operational_cognition/execution_authority.py`](operational_cognition/execution_authority.py) | Standing-authority and confirmation-trigger evaluation. |
| [`operational_cognition/topology.py`](operational_cognition/topology.py) | Architecture discovery and correct-plane routing. |
| [`operational_cognition/maturity.py`](operational_cognition/maturity.py) | Capability maturity and artifact closure. |
| [`operational_cognition/master_strand.py`](operational_cognition/master_strand.py) | Branch assessment, extinction gates, and canonical-strand decisions. |
| [`finisher/finisher.py`](finisher/finisher.py) | Finish-first classification and closure planning. |
| [`src/verify_manifest.py`](src/verify_manifest.py) | Canonical manifest validation. |
| [`scripts/verify_repository.py`](scripts/verify_repository.py) | Exhaustive pytest collection, outcome accounting, and atomic receipts. |
| [`scripts/verify_readme_contract.py`](scripts/verify_readme_contract.py) | Portable public-document contract verification. |

### Correctness and failure behavior

- A plan is not execution.
- Execution without a provider receipt cannot establish provider-side change.
- Validation without persistence cannot establish durable completion.
- Irreversible operations require explicit approval.
- Unauthorized writes are blocked.
- Missing test modules produce a `FAILED` receipt.
- Zero collected or executed tests remain `UNVERIFIED`.
- Collection, usage, and internal pytest errors produce `FAILED` evidence.
- Function-style pytest tests and class-based unittest cases share one exhaustive collection.
- Receipt files use exclusive temporary files and atomic replacement.
- README verification is independent of the caller's working directory.
- macOS, Windows, and file-URL local paths are rejected from the public README.
- Repository workflows are restricted to exact read-only permissions, local checkout, and nonpersistent credentials.
- Secret-bearing cross-repository finishing is prohibited in AKOS Actions and routed to the governed action face.

### Build and verification

```bash
# Install runtime and verification tooling
python -m pip install -e ".[dev]"

# Strictly lint the newly introduced verification boundary
ruff check \
  scripts/verify_repository.py \
  scripts/verify_readme_contract.py \
  tests/test_verification_tools.py \
  operational_cognition/test_contracts.py

# Compile executable surfaces
python -m compileall -q operational_cognition finisher src scripts tests

# Verify the three-audience public contract
akos-verify-readme

# Run exhaustive pytest collection and emit the receipt
akos-verify --output artifacts/ci/test-receipt.json
```

The receipt schema is `glaciereq.akos.test-receipt.v1`. It records the revision, interpreter and pytest versions, discovered modules, collected count, executed outcomes, collection and internal errors, evidence level, and conclusion.

### Verification layers

| Layer | Current result |
|---|---|
| Packaging and declared dependencies | Passed on Python 3.11–3.13 |
| New verification-code lint | Passed with zero findings |
| Existing-runtime Ruff baseline | 117 findings recorded, not hidden or mislabeled as fixed |
| Bytecode and tracked-file compilation | Passed |
| README audience and portability contract | Passed |
| Exhaustive repository behavior | 94/94 passed per interpreter |
| Workflow authority contract | Passed; exact read-only local verification only |
| Finisher verification | Passed after secret-bearing execution was retired |
| Adversarial integrity + Git anchor | Passed |
| Deployment, performance, and scale | Not claimed |

### Quality-debt treatment

The initial strict audit of the preexisting runtime recorded **117 Ruff findings** in `glaciereq.akos.ruff-baseline.v1`. That debt is visible and versioned. It is not confused with behavioral correctness, and it is not represented as remediated. New verification code is held to a zero-warning gate while legacy debt is reduced through bounded, behavior-preserving changes.

### Language fit

| Language / format | Responsibility | Boundary | Proof |
|---|---|---|---|
| Python 3.11+ | Cognition, authority, topology, maturity, closure, and verification | Executable runtime and proof tooling | Three-version CI plus exhaustive pytest receipt |
| JSON | Runtime manifests, topology, maturity, and receipts | Machine-readable policy and evidence | Parsing and contract tests |
| YAML | Canonical manifests and GitHub workflow policy | Human-editable declarations | Manifest and workflow-contract tests |
| Markdown | Laws, specifications, ADRs, ledgers, and three-audience communication | Human governance and review | README contract and openable evidence |

The repository remains intentionally Python-centered. Additional languages belong only where a workload, safety property, interoperability boundary, or performance requirement creates measurable value.

### Evidence-backed operating rules

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

```text
DECLARED -> DISCOVERED -> CONNECTED -> AUTHENTICATED -> AUTHORIZED ->
INVOKED -> RETURNED -> VERIFIED -> PERSISTED
```

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
    pytest: "8.4.2"
    tests_per_interpreter: 94
    test_modules: 12
    passed: 94
    failures: 0
    errors: 0
    skipped: 0
    collection_errors: 0
    internal_errors: 0
  quality_baseline:
    schema: glaciereq.akos.ruff-baseline.v1
    preexisting_findings: 117
    treatment: recorded_nonblocking_debt
  verified_scope:
    - editable package installation and declared dependencies
    - installed akos-verify and akos-verify-readme commands
    - strict quality gate for new verification code and regression tests
    - compilation of executable and tracked Python surfaces
    - exhaustive pytest collection across function and class test styles
    - operational-cognition, finisher, integrity, connector, manifest, and verifier tests
    - recruiter, expert, and AI README contract
    - read-only workflow authority contract
    - adversarial integrity tests and Git-anchor verification
  blocked_scope:
    - irreversible actions without explicit approval
    - provider-side operations without current provider receipts
    - secret-bearing or cross-repository execution from AKOS Actions
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
    lint_new_code: >-
      ruff check scripts/verify_repository.py scripts/verify_readme_contract.py
      tests/test_verification_tools.py operational_cognition/test_contracts.py
    compile: python -m compileall -q operational_cognition finisher src scripts tests
    test: akos-verify --output artifacts/ci/test-receipt.json
    verify_readme: akos-verify-readme
evidence:
  workflow: .github/workflows/ci.yml
  integrity_workflow: .github/workflows/integrity.yml
  finisher_workflow: .github/workflows/finisher.yml
  test_runner: scripts/verify_repository.py
  receipt_schema: glaciereq.akos.test-receipt.v1
  quality_schema: glaciereq.akos.ruff-baseline.v1
  action_boundary_receipt: ledger/2026-07-30_FINISHER_ACTION_BOUNDARY.md
  tests:
    - .integrity/test_*.py
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
    combined_value: Agent motion receives bounded authority, persistence, and completion rules.
  - target: GlacierEQ/anthropic-safety-monitor
    relation: GOVERNS
    combined_value: Independent monitoring feeds explicit review and blocking decisions.
  - target: GlacierEQ/spacex-mission-control
    relation: GOVERNS
    combined_value: Mission orchestration inherits evidence and completion boundaries.
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
/docs/                     architecture and integration doctrine
/specs/                    formal AKOS specifications
/contracts/                compatibility and authority contracts
/schemas/                  machine-readable validation schemas
/manifests/                topology, cognition, and maturity manifests
/templates/                reusable canonical templates
/methodologies/            Pro-Code and operating methods
/adr/                      architecture decision records
/ledger/                   append-only build, correction, migration, and sync receipts
/finisher/                 deterministic closure engine
/operational_cognition/    execution, topology, maturity, authority, and closure runtime
/scripts/                  installed repository-verification tooling
```

## Start here

1. Read [`AKOS_MANIFEST.yaml`](AKOS_MANIFEST.yaml).
2. Read [`BUILD_INDEX.md`](BUILD_INDEX.md) and [`CURRENT_STATE.md`](CURRENT_STATE.md).
3. Inspect [`manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`](manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json) before diagnosing a missing route.
4. Apply [`AKOS-OC-001`](specs/AKOS-OC-001_OPERATIONAL_COGNITION.md) to execution and [`AKOS-OC-002`](specs/AKOS-OC-002_OPERATIONAL_MATURITY.md) to maturity or closure claims.
5. Run `akos-verify-readme` and `akos-verify`.
6. Close finishable work before proposing expansion.
7. Preserve history and append evidence-backed deltas.

## Operating principle

Build in layers. Preserve history. Reuse before rebuilding. Finish before expanding. Verify before claiming. Persist before reporting closure. Never confuse a mirror with the source of truth, a wrong-plane failure with missing infrastructure, or a compelling explanation with completed work.
