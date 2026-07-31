# ADR-0012 — ECHO as a Standalone AKOS-Governed Product

- **Status:** Accepted
- **Date:** 2026-07-30
- **Decision owners:** GlacierEQ / AKOS
- **Canonical ECHO identity:** `SYS-ECHO-001`
- **Intended repository:** `GlacierEQ/ECHO`

## Context

ECHO is the cross-platform conversation and memory-portability product intended to search, label, summarize, export, correlate, and reconnect conversations across ChatGPT, Claude, Gemini, and other supported systems.

AKOS is the governance and operational-cognition layer. It should govern ECHO, but it should not absorb ECHO's product runtime, user interfaces, provider adapters, storage implementation, release lifecycle, or deployment surface.

Embedding ECHO directly into AKOS would simplify initial discovery but would weaken separation of concerns, independent deployment, product-focused testing, permission isolation, and future reuse. Making ECHO fully independent without an AKOS contract would create a disconnected product island and duplicate governance logic.

## Decision

ECHO will be a **standalone product repository governed by AKOS**.

The best-of-all-worlds structure is:

```text
AKOS
  owns identity, governance, authority, provenance, evidence,
  maturity, interoperability, promotion, and completion contracts
                         │
                         │ governs through versioned contracts
                         ▼
ECHO
  owns capture, normalization, indexing, search, labeling,
  summarization, export, synchronization, portability, and UX
```

AKOS will retain:

- the canonical ECHO system identity;
- the AKOS–ECHO integration contract;
- authority and evidence requirements;
- compatibility and maturity expectations;
- topology relationships and promotion receipts;
- cross-repository completion criteria.

ECHO will retain:

- product code and provider adapters;
- conversation and memory schemas specific to product behavior;
- user-facing interfaces and APIs;
- release packaging and deployment configuration;
- provider-specific tests and operational telemetry;
- product documentation and product roadmap.

## Best-of-All-Worlds analysis

### Strengths preserved from embedding ECHO in AKOS

- discoverability from the canonical operating system;
- consistent identity, governance, evidence, and completion semantics;
- shared authority and promotion rules;
- explicit mesh relationship with other GlacierEQ systems.

### Strengths preserved from a standalone repository

- independent versioning and deployment;
- narrow permissions and blast radius;
- product-focused CI and release cadence;
- replaceable provider adapters;
- clearer recruiter, expert, and AI-facing documentation;
- future use outside the AKOS repository without copying governance code.

### Weaknesses removed

- no monolithic AKOS product runtime;
- no duplicated governance implementation inside ECHO;
- no unsupported claim that an ECHO repository already exists;
- no hidden coupling through undocumented shared state.

## Consequences

1. AKOS must not claim ECHO is deployed until a provider receipt proves the standalone repository and runtime exist.
2. The ECHO repository must consume or implement the versioned AKOS–ECHO contract.
3. Shared schemas belong in the repository that owns the concept; mirrored schemas must retain canonical-source metadata.
4. Product secrets and provider credentials remain outside AKOS.
5. Cross-repository changes require independent verification receipts from both sides of the contract.
6. ECHO may evolve independently, but contract-breaking changes require an explicit compatibility transition.

## Promotion gate

ECHO may advance from `DECLARED` only after evidence establishes:

```text
DECLARED -> REPOSITORY_CREATED -> CONTRACT_BOUND -> TESTED ->
CONNECTED -> AUTHENTICATED -> AUTHORIZED -> DEPLOYED -> VERIFIED -> PERSISTED
```

## Rejected alternatives

### Embed ECHO entirely inside AKOS

Rejected because it collapses governance and product-runtime boundaries and creates avoidable coupling.

### Create ECHO as a completely independent repository

Rejected because it would duplicate or omit governance, evidence, authority, and completion semantics already owned by AKOS.

### Treat ECHO as documentation only

Rejected because ECHO is intended to be an executable product, not merely an architectural label.
