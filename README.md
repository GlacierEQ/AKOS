# AKOS — Apex Knowledge Operating System

[![AKOS Verification](https://github.com/GlacierEQ/AKOS/actions/workflows/ci.yml/badge.svg)](https://github.com/GlacierEQ/AKOS/actions/workflows/ci.yml)
[![AKOS Integrity Gate](https://github.com/GlacierEQ/AKOS/actions/workflows/integrity.yml/badge.svg)](https://github.com/GlacierEQ/AKOS/actions/workflows/integrity.yml)
[![Infinity Stone Forge](https://github.com/GlacierEQ/AKOS/actions/workflows/infinity-stones.yml/badge.svg)](https://github.com/GlacierEQ/AKOS/actions/workflows/infinity-stones.yml)

**Version:** `0.7.0`  
**Canonical repository:** `GlacierEQ/AKOS`  
**Verification state:** `VERIFIED` at evidence level `TEST` for the recorded repository-local scope  
**Verified matrix:** Python `3.11`, `3.12`, and `3.13`  
**Promotion basis:** `118/118` full AKOS tests, `10/10` focused Forge tests, and `4/4` PSYSOC-X calibration cases on tested revision `5b960219635fcd95a9a98a2d7c1bfc5d19111c84`

AKOS is the governance and operational-cognition layer for large, interconnected engineering systems. It converts identity, provenance, authority, execution, verification, persistence, and completion from informal expectations into inspectable contracts and executable behavior.

<!-- README-MESH:BEGIN -->

<!-- README-ACT:HUMAN -->

## The Operating System That Refuses to Call a Draft Done

*Recruiter lens · what AKOS changes, why it matters, and where the proof lives*

A sophisticated collection of tools can still fail as a system: work gets duplicated, actions happen in the wrong place, drafts are reported as completion, and corrections disappear between sessions. AKOS addresses that coordination failure.

It gives a large engineering portfolio one durable operating model without flattening the projects inside it:

- every important object has a stable identity and provenance;
- plans, actions, verification, persistence, and completion are different states;
- safe and recoverable work can proceed under explicit standing authority;
- high-risk or irreversible work remains gated;
- corrections become policy, executable guards, regression tests, and receipts;
- incomplete work reports its exact missing stage instead of an invented percentage;
- practiced AI instincts can become versioned, reversible, testable Infinity Stones.

### Why it matters

AKOS demonstrates systems architecture beyond a single application. It shows how governance becomes code, how trust becomes an evidence property, and how a portfolio improves recursively without rewriting history or obscuring responsibility.

### Proof in 60 seconds

| Open or run | What it demonstrates |
|---|---|
| [`specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md`](specs/AKOS-LAW-001_FOUNDATIONAL_LAWS.md) | Durable operating laws and system invariants. |
| [`operational_cognition/execution_authority.py`](operational_cognition/execution_authority.py) | Deterministic execute, confirm, or block decisions. |
| [`operational_cognition/engine.py`](operational_cognition/engine.py) | Evidence classes, routing, phase receipts, and completion logic. |
| [`finisher/finisher.py`](finisher/finisher.py) | Finish-first analysis and exact blocker handling. |
| [`infinity_stones/README.md`](infinity_stones/README.md) | The executable Infinity Stone Forge and its verified first release. |
| [`stones/psysoc-x/STONE.md`](stones/psysoc-x/STONE.md) | PSYSOC-X’s human-calibration purpose, limits, interfaces, and proof. |
| [`receipts/2026-08-02_psysoc-x_v0.1.0_promotion.json`](receipts/2026-08-02_psysoc-x_v0.1.0_promotion.json) | Exact promotion basis, workflow runs, hashes, scope, and non-claims. |
| [`scripts/verify_repository.py`](scripts/verify_repository.py) | Exhaustive pytest collection and atomic proof receipts. |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Three-version package, contract, and behavioral verification. |
| [`.github/workflows/infinity-stones.yml`](.github/workflows/infinity-stones.yml) | Three-version Forge lint, compile, test, receipt, and artifact verification. |
| [`.github/workflows/integrity.yml`](.github/workflows/integrity.yml) | Adversarial integrity tests and Git-anchor verification. |
| [`ledger/2026-07-30_FINISHER_ACTION_BOUNDARY.md`](ledger/2026-07-30_FINISHER_ACTION_BOUNDARY.md) | Evidence-backed migration of secret-bearing execution to the correct plane. |

### Evidence summary

The promotion receipt establishes repository-local behavior at the `TEST` level:

- 17 discovered test modules across integrity, operational cognition, Finisher, manifests, Forge behavior, and verifier tooling;
- 118 collected and executed full-repository tests on each supported Python version at the tested promotion revision;
- 118 passes with no failures, errors, skips, collection errors, or internal errors;
- 10 focused Forge tests on each supported Python version;
- 4 of 4 manifest-driven PSYSOC-X calibration cases passed;
- editable installation with explicit dependencies and installed verification commands;
- strict zero-warning lint for the Forge and new verification control surfaces;
- compilation of executable and tracked Python surfaces;
- four-act README contract verification;
- read-only, secretless workflow-policy enforcement and Git-anchor verification.

It does **not** claim external-provider connectivity, deployment scale, production reliability, clinical validity, hidden-trait prediction, or exercised behavior outside repository-local CI.

<!-- README-ACT:MASTER -->

## Where Governance Becomes Executable

*Master section · architecture, authority, correctness, failure behavior, and tradeoffs*

### System boundary

AKOS owns:

- canonical identity and provenance rules;
- authority and confirmation policy;
- source and capability routing;
- evidence-backed maturity transitions;
- execution, validation, persistence, and handoff semantics;
- artifact-closure stages and exact blocker reporting;
- correction-to-policy persistence;
- governance contracts for connected repositories and agents;
- Infinity Stone identity, composition, boundaries, and repository-local verification.

AKOS does **not** convert a declared integration into a connected one, a connected provider into an authorized one, an architecture diagram into executed state, or a deterministic calibration engine into a claim of psychological prediction. Those transitions require their own receipts.

### Architecture

```text
Prime purpose + foundational laws
                │
                ▼
       Canonical object model
 identity • provenance • relationships
                │
        ┌───────┴──────────────┐
        ▼                      ▼
Operational cognition     Infinity Stone Forge
route • decide • act      package • compose • verify
        │                      │
        └──────────┬───────────┘
                   ▼
          Maturity + closure
         measure • gate • finish
                   │
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
6. **Specialization plane** — reversible stone packages that shape judgment or presentation without mutating the base model or evidence.

### Core innovations

1. **One truth, many views** — canonical objects support multiple projections without losing identity.
2. **Execution without redundant permission** — beneficial, objective-preserving, recoverable work can proceed within standing authority.
3. **Receipt-backed completion** — plans and drafts cannot masquerade as changed state.
4. **System-first routing** — existing planes are discovered and reused before infrastructure is invented.
5. **Correction-to-cognition** — corrections become durable law, runtime behavior, tests, and ledger entries.
6. **Artifact closure** — exact missing stages replace subjective completion percentages.
7. **Monotonic maturity** — evidence states advance through explicit transitions and cannot silently regress.
8. **Reversible specialization** — named AI instincts become inspectable stone manifests, engines, skills, upgrades, gauntlets, tests, and receipts.

### Runtime map

| Component | Responsibility |
|---|---|
| [`operational_cognition/engine.py`](operational_cognition/engine.py) | Work models, routing, evidence classes, phase receipts, and completion decisions. |
| [`operational_cognition/execution_authority.py`](operational_cognition/execution_authority.py) | Standing-authority and confirmation-trigger evaluation. |
| [`operational_cognition/topology.py`](operational_cognition/topology.py) | Architecture discovery and correct-plane routing. |
| [`operational_cognition/maturity.py`](operational_cognition/maturity.py) | Capability maturity and artifact closure. |
| [`operational_cognition/master_strand.py`](operational_cognition/master_strand.py) | Branch assessment, extinction gates, and canonical-strand decisions. |
| [`operational_cognition/adaptation.py`](operational_cognition/adaptation.py) | Bounded dynamic routing and unhealthy-signal backoff. |
| [`finisher/finisher.py`](finisher/finisher.py) | Finish-first classification and closure planning. |
| [`infinity_stones/registry.py`](infinity_stones/registry.py) | Safe manifest loading, identity validation, and alias collision protection. |
| [`infinity_stones/composition.py`](infinity_stones/composition.py) | Deterministic stone and upgrade composition with loadout hashing. |
| [`infinity_stones/psysoc_x.py`](infinity_stones/psysoc_x.py) | Bounded human-calibration profiles from explicit context. |
| [`scripts/verify_stones.py`](scripts/verify_stones.py) | Manifest-driven calibration verification and atomic Forge receipts. |
| [`scripts/verify_repository.py`](scripts/verify_repository.py) | Exhaustive pytest collection, outcome accounting, and atomic receipts. |
| [`scripts/verify_readme_contract.py`](scripts/verify_readme_contract.py) | Distinctive four-act public-document contract verification. |

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
- Generic visible audience headings are rejected; hidden markers preserve deterministic four-act parsing.
- macOS, Windows, and file-URL local paths are rejected from the public README.
- Repository workflows are restricted to exact read-only permissions, local checkout, nonpersistent credentials, and no secret-bearing execution.
- Reusable verification may inspect a caller repository but cannot inherit mutation authority.
- Explicitly unhealthy adaptation signals cannot earn a healthy routing score from latency, cost, queue, or confidence alone.
- PSYSOC-X cannot alter evidence state, diagnose a person, infer protected traits, or exploit fear, shame, grief, dependency, or confusion.

### Build and verification

```bash
# Install runtime and verification tooling
python -m pip install -e ".[dev]"

# Strictly lint the new verification and Forge boundaries
ruff check \
  infinity_stones \
  scripts/verify_repository.py \
  scripts/verify_readme_contract.py \
  scripts/verify_stones.py \
  tests/test_verification_tools.py \
  tests/test_infinity_stones.py \
  tests/test_psysoc_x.py \
  operational_cognition/test_contracts.py

# Compile executable surfaces
python -m compileall -q operational_cognition finisher infinity_stones src scripts tests

# Verify the four-act public contract
akos-verify-readme

# Verify the stone registry, composition, and calibration cases
akos-verify-stones --output artifacts/ci/infinity-stone-receipt.json

# Run exhaustive pytest collection and emit the repository receipt
akos-verify --output artifacts/ci/test-receipt.json
```

The repository receipt schema is `glaciereq.akos.test-receipt.v1`. The Forge receipt schema is `glaciereq.infinity-stone-verification-receipt.v1`. Both distinguish observed test behavior from deployment, provider, scale, or human-prediction claims.

### Verification layers

| Layer | Current result |
|---|---|
| Packaging and declared dependencies | Passed on Python 3.11–3.13 at the tested promotion revision |
| New verification and Forge lint | Passed with zero findings |
| Existing-runtime Ruff baseline | 136 findings recorded, not hidden or mislabeled as fixed |
| Bytecode and tracked-file compilation | Passed |
| README four-act and portability contract | Passed |
| Focused Forge behavior | 10/10 passed per interpreter |
| PSYSOC-X calibration cases | 4/4 passed per interpreter |
| Exhaustive repository behavior | 118/118 passed per interpreter at the tested promotion revision |
| Workflow authority contract | Passed; exact read-only, secretless, local verification only |
| Nervous-system and Aspen Grove contracts | Passed |
| Adversarial integrity + Git anchor | Passed |
| Deployment, performance, human-prediction accuracy, and scale | Not claimed |

### Quality-debt treatment

The current strict audit records **136 Ruff findings** in `glaciereq.akos.ruff-baseline.v1`. That debt is visible and versioned. It is not confused with behavioral correctness, and it is not represented as remediated. New verification and Forge code are held to zero-warning gates while legacy debt is reduced through bounded, behavior-preserving changes.

### Language fit

| Language / format | Responsibility | Boundary | Proof |
|---|---|---|---|
| Python 3.11+ | Cognition, authority, topology, maturity, closure, stone composition, calibration, and verification | Executable runtime and proof tooling | Three-version CI plus exhaustive and Forge receipts |
| JSON | Runtime manifests, topology, maturity, stone contracts, gauntlets, and receipts | Machine-readable policy and evidence | Parsing, composition, and contract tests |
| YAML | Canonical manifests and GitHub workflow policy | Human-editable declarations | Manifest and workflow-contract tests |
| Markdown | Laws, specifications, skills, ADRs, ledgers, and four-act communication | Human governance and review | README contract and openable evidence |

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

```text
INSTINCT -> IDENTITY -> SKILLS -> JUDGMENT -> BOUNDARIES -> COMPOSITION ->
TESTS -> RECEIPTS -> TEST-VERIFIED SPECIALIZATION
```

Unmeasured means `UNASSESSED`, not an invented score.

<!-- README-ACT:MACHINE -->

## Enter Through the Contracts, Exit With Receipts

*Machine section · canonical resources, exact commands, evidence classes, and retrieval boundaries*

### Machine contract

```yaml
schema: glaciereq.readme.v1
profile: glaciereq.readme-impact.v2.1
repository: GlacierEQ/AKOS
canonical_branch: main
purpose: >-
  Govern identity, provenance, authority, execution, verification,
  persistence, completion, reversible specialization, and recursive improvement.
status:
  state: VERIFIED
  evidence_level: TEST
  promotion_receipt: receipts/2026-08-02_psysoc-x_v0.1.0_promotion.json
  tested_revision: 5b960219635fcd95a9a98a2d7c1bfc5d19111c84
  verification_matrix:
    python: ["3.11", "3.12", "3.13"]
    pytest: "8.4.2"
    full_akos_tests_per_interpreter: 118
    focused_forge_tests_per_interpreter: 10
    psysoc_x_cases_per_interpreter: 4
    passed_full_akos: 118
    passed_forge: 10
    passed_psysoc_x_cases: 4
    failures: 0
    errors: 0
    skipped: 0
    collection_errors: 0
    internal_errors: 0
  quality_baseline:
    schema: glaciereq.akos.ruff-baseline.v1
    preexisting_findings: 136
    treatment: recorded_nonblocking_debt
  verified_scope:
    - editable package installation and declared dependencies
    - installed akos-verify, akos-verify-readme, and akos-verify-stones commands
    - strict quality gate for new verification and Forge code
    - compilation of executable and tracked Python surfaces
    - exhaustive pytest collection across function and class test styles
    - operational-cognition, finisher, integrity, connector, manifest, Forge, and verifier tests
    - deterministic stone registry, alias resolution, composition, and loadout hashing
    - bounded PSYSOC-X calibration across four manifest-driven cases
    - four-act README contract
    - read-only, secretless workflow authority contract
    - nervous-system, Aspen Grove, adversarial integrity, and Git-anchor verification
  blocked_scope:
    - irreversible actions without explicit approval
    - provider-side operations without current provider receipts
    - secret-bearing or cross-repository mutation from AKOS Actions
    - evidence promotion by a stone or presentation engine
  unverified_scope:
    - external connectors not exercised by repository-local tests
    - deployment, performance, reliability, and scale outside GitHub Actions
    - clinical, diagnostic, or therapeutic validity
    - hidden-trait or motive prediction
    - planned stones stone-elite-pro-builder and stone-juggernaut-jack
interfaces:
  inputs:
    - work items and authority context
    - capability and topology declarations
    - evidence and provider receipts
    - runtime and maturity manifests
    - explicit audience, decision, stakes, skepticism, load, privacy, and evidence context
  outputs:
    - execute, confirm, block, or complete decisions
    - capability and artifact maturity results
    - exact blockers and missing closure stages
    - deterministic stone loadouts and digests
    - human-resonance profiles with humor, tone, density, logic, dignity, and warnings
    - atomic repository, Forge, and quality-baseline receipts
  commands:
    install: python -m pip install -e ".[dev]"
    lint_new_code: >-
      ruff check infinity_stones scripts/verify_repository.py
      scripts/verify_readme_contract.py scripts/verify_stones.py
      tests/test_verification_tools.py tests/test_infinity_stones.py
      tests/test_psysoc_x.py operational_cognition/test_contracts.py
    compile: >-
      python -m compileall -q operational_cognition finisher
      infinity_stones src scripts tests
    test: akos-verify --output artifacts/ci/test-receipt.json
    verify_readme: akos-verify-readme
    verify_stones: >-
      akos-verify-stones --output artifacts/ci/infinity-stone-receipt.json
evidence:
  workflow: .github/workflows/ci.yml
  integrity_workflow: .github/workflows/integrity.yml
  forge_workflow: .github/workflows/infinity-stones.yml
  nervous_system_workflow: .github/workflows/nervous-system-contract.yml
  aspen_grove_workflow: .github/workflows/aspen-grove-manifest.yml
  test_runner: scripts/verify_repository.py
  forge_runner: scripts/verify_stones.py
  receipt_schema: glaciereq.akos.test-receipt.v1
  forge_receipt_schema: glaciereq.infinity-stone-verification-receipt.v1
  promotion_receipt: receipts/2026-08-02_psysoc-x_v0.1.0_promotion.json
  tests:
    - .integrity/test_*.py
    - operational_cognition/test_*.py
    - finisher/test_*.py
    - tests/test_*.py
relationships:
  - target: GlacierEQ/job-app-helix
    relation: GOVERNS
    combined_value: >-
      AKOS supplies authority, provenance, completion, and reversible-specialization semantics;
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
  - PSYSOC-X presentation calibration is not human diagnosis or hidden-trait prediction.
  - Recorded lint debt is not represented as remediated.
```

### Canonical machine resources

- [`AKOS_MANIFEST.yaml`](AKOS_MANIFEST.yaml)
- [`manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`](manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json)
- [`manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`](manifests/runtime/AKOS_OPERATIONAL_COGNITION.json)
- [`manifests/runtime/AKOS_OPERATIONAL_MATURITY.json`](manifests/runtime/AKOS_OPERATIONAL_MATURITY.json)
- [`registry/stones.json`](registry/stones.json)
- [`stones/psysoc-x/stone.json`](stones/psysoc-x/stone.json)
- [`upgrades/do-it-again/upgrade.json`](upgrades/do-it-again/upgrade.json)
- [`gauntlets/humanized-evidence-presentation.json`](gauntlets/humanized-evidence-presentation.json)
- [`receipts/2026-08-02_psysoc-x_v0.1.0_promotion.json`](receipts/2026-08-02_psysoc-x_v0.1.0_promotion.json)
- [`schemas/operational_cognition.schema.json`](schemas/operational_cognition.schema.json)
- [`schemas/operational_maturity.schema.json`](schemas/operational_maturity.schema.json)
- [`schemas/infinity-stone.schema.json`](schemas/infinity-stone.schema.json)
- [`schemas/infinity-upgrade.schema.json`](schemas/infinity-upgrade.schema.json)
- [`contracts/`](contracts/)
- [`specs/`](specs/)

<!-- README-MESH:END -->

<!-- README-ACT:MESH -->

## The Nervous System Behind the Forge

*Mesh section · how governance, memory, engineering, language boundaries, and specializations combine without collapsing authority*

AKOS governs the stone forge, but it does not pretend to contain every specialized capability itself. It inherits memory, boot, engineering doctrine, execution practice, and polyglot governance through an explicit nervous system:

```text
MEMORY → TOOL → CURE → INNOVATE → RESPOND
```

| System | Role in the living architecture |
|---|---|
| [Aspen Grove Core](https://github.com/GlacierEQ/aspen-grove-core) | Canonical memory and context-routing root. |
| [Apex Boot Core](https://github.com/GlacierEQ/apex-boot-core) | Boot sequence and runtime initialization boundary. |
| [Pro_Code](https://github.com/GlacierEQ/Pro_Code) | Engineering doctrine and quality constitution. |
| [pro-code](https://github.com/GlacierEQ/pro-code) | Engineering execution and implementation practice. |
| [The Tower of Babel](https://github.com/GlacierEQ/the-tower-of-babel) | Polyglot language-boundary governance. |
| [Infinity Stone Forge](infinity_stones/README.md) | Versioned, reversible specialization packages, composition, and proof receipts. |

The links define inheritance and routing, not automatic connectivity or runtime success. Each connected system retains its own source, authority boundary, evidence state, and verification burden.

## Repository map

```text
/docs/                     architecture, ontology, and integration doctrine
/specs/                    formal AKOS specifications
/contracts/                compatibility and authority contracts
/schemas/                  machine-readable validation schemas
/manifests/                topology, cognition, and maturity manifests
/templates/                reusable canonical templates
/methodologies/            Pro-Code and operating methods
/adr/                      architecture decision records
/ledger/                   append-only build, correction, migration, and sync receipts
/receipts/                 immutable promotion and verification evidence
/finisher/                 deterministic closure engine
/operational_cognition/    execution, topology, maturity, authority, and closure runtime
/infinity_stones/          executable stone registry, composition, calibration, and receipts
/stones/                   authored runtime-specialization packages
/upgrades/                 cross-stone behavior modifiers
/gauntlets/                governed stone and upgrade compositions
/scripts/                  installed repository-verification tooling
```

## Start here

1. Read [`AKOS_MANIFEST.yaml`](AKOS_MANIFEST.yaml).
2. Read [`BUILD_INDEX.md`](BUILD_INDEX.md) and [`CURRENT_STATE.md`](CURRENT_STATE.md).
3. Inspect [`manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`](manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json) before diagnosing a missing route.
4. Read [`infinity_stones/README.md`](infinity_stones/README.md) and the [PSYSOC-X promotion receipt](receipts/2026-08-02_psysoc-x_v0.1.0_promotion.json).
5. Apply [`AKOS-OC-001`](specs/AKOS-OC-001_OPERATIONAL_COGNITION.md) to execution and [`AKOS-OC-002`](specs/AKOS-OC-002_OPERATIONAL_MATURITY.md) to maturity or closure claims.
6. Run `akos-verify-readme`, `akos-verify-stones`, and `akos-verify`.
7. Close finishable work before proposing expansion.
8. Preserve history and append evidence-backed deltas.

## Operating principle

Build in layers. Preserve history. Reuse before rebuilding. Finish before expanding. Verify before claiming. Persist before reporting closure. Never confuse a mirror with the source of truth, a wrong-plane failure with missing infrastructure, a stone with its invocation sentence, or a compelling explanation with completed work.
