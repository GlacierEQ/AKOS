# Monolith Skills

## Purpose

These skills define the mentality and operating discipline required to handle repository estates at 100-repository scale and beyond in one coherent mission cycle.

The objective is not maximal scanning. The objective is maximal **relevant truth per unit of attention**, with ownership, evidence, privacy, and failure semantics preserved.

## 1. Mission-to-Subgraph Resolution

Translate the user's mission into:

- affected domains;
- foundational systems;
- owning repositories;
- likely capability donors;
- shared schemas and services;
- release and deployment surfaces;
- privacy and authority boundaries;
- evidence required for completion.

Do not begin with a repository list. Begin with the mission model, then resolve the minimum complete subgraph.

## 2. Live Estate Discovery

Discover repositories through current connected sources. Capture:

- source system;
- repository ID and canonical full name;
- visibility;
- default branch;
- current revision where available;
- updated time;
- pagination and coverage limits;
- observation time;
- source hash or cursor where available.

Never label a bounded result complete when pagination, permissions, connectors, or local-only sources may exclude records.

## 3. Canonical Identity Resolution

Resolve:

- casing variants;
- hyphen and underscore variants;
- renamed repositories;
- duplicate concepts;
- backups;
- forks and mirrors;
- generated children;
- predecessor/successor chains;
- private doctrine versus public runtime;
- concept names versus actual repositories.

Identity decisions need explicit evidence and a reversible alias table.

## 4. Multi-Axis Classification

Keep these dimensions separate:

- domain;
- whole versus part;
- ownership authority;
- visibility;
- provenance/authorship;
- activity;
- maturity;
- evidence level;
- promotion state;
- privacy class;
- freshness;
- release relevance.

A repository can be public, active, useful, and still excluded from original-work claims. A whole system can be blocked. A private doctrine can be strategically important without being public executable proof.

## 5. Capability Donor Analysis

Search for reusable primitives rather than only flagship candidates.

For every repository, ask:

- What unique capability exists here?
- Is it implemented, documented, inferred, or merely named?
- Which systems consume or could reuse it?
- What is the extraction boundary?
- What license and provenance constraints apply?
- Is the donor canonical, superseded, duplicated, or unsafe?

A small repository may be a high-value donor even when it should never become a flagship.

## 6. Dependency and Impact Mapping

Build typed edges for:

- imports and packages;
- APIs;
- schemas;
- database tables;
- connectors;
- environment contracts;
- deployments;
- generated artifacts;
- workflows;
- documentation links;
- company and role relevance;
- evidence and receipt dependencies.

Before changing a shared primitive, identify downstream consumers and the verification required in each.

## 7. Prior-Work Recovery

Before planning or building:

1. locate the latest canonical checkpoint;
2. identify prior audits, registries, matrices, and generated packages;
3. reconcile conflicting versions and timestamps;
4. preserve verified gains;
5. compute the delta from the controlling checkpoint;
6. extend rather than restart.

Rebuilding an existing registry or architecture without evidence that it is unusable is a critical execution failure.

## 8. Native Proof-Path Discovery

For each mission repository, discover its real stack and commands:

- install;
- format/lint;
- typecheck/static analysis;
- unit tests;
- integration tests;
- build;
- security checks;
- packaging;
- deployment verification.

Do not impose one global command on heterogeneous repositories. Zero-test success is not test evidence.

## 9. Wave Partitioning

Partition work by dependency and write conflict:

- **Wave A: read-only census and metadata**;
- **Wave B: identity and classification anomalies**;
- **Wave C: independent repository verification**;
- **Wave D: shared dependency and integration checks**;
- **Wave E: bounded repairs**;
- **Wave F: generated projections and release reconciliation**.

Independent repositories may run concurrently. Repositories sharing files, schemas, releases, or dependent writes must be serialized or assigned an explicit merge protocol.

## 10. Resource-Budget Engineering

Declare budgets before execution:

- maximum repositories in scope;
- maximum deep inspections;
- time per command;
- total wall-clock budget;
- concurrency;
- token/context budget;
- network calls;
- mutations;
- artifact size;
- retry policy.

Use anomaly-driven escalation: shallow discovery across breadth, deep inspection where the mission or evidence requires it.

## 11. One-Turn Compression

A coherent hundred-repository turn uses layered compression:

```text
estate metadata
→ normalized registry
→ domain and role aggregates
→ anomaly set
→ mission subgraph
→ per-repository proof summaries
→ aggregate decision
```

Retain pointers to the underlying records. Compression must reduce volume, not erase uncertainty or adverse results.

## 12. Evidence Monotonicity

Evidence levels do not inherit upward:

```text
presence < documentation < static analysis < build < test < integration < deployment
```

A README cannot prove a build. A build cannot prove tests. Tests cannot prove production. A historical receipt cannot prove the current revision.

## 13. Aggregate Failure Semantics

The aggregate state uses the strongest required adverse result.

- Any required `FAILED` repository keeps the wave failed.
- Any required `BLOCKED` repository keeps completion blocked.
- `REFERENCE_ONLY` items cannot inflate passing totals.
- Missing repositories remain visible.
- Partial scopes include explicit denominators and exclusions.

Do not average away failure with a high overall pass percentage.

## 14. Contradiction Detection

Detect contradictions among:

- manifests and actual repository state;
- website and source;
- résumé and evidence ledger;
- README claims and tests;
- old and current receipts;
- repository aliases;
- public and private classifications;
- deployment and Git revisions.

Every contradiction is either resolved, quarantined, or carried forward visibly.

## 15. Privacy and Public-Surface Partitioning

Separate:

- public recruiter-safe systems;
- private operations;
- sensitive legal/personal material;
- upstream references;
- internal doctrine;
- quarantined secrets or credentials.

Generated catalogs, search APIs, backlinks, and graph edges must follow the same allowlist. A hidden primary page does not make a reachable machine record private.

## 16. Multi-Repository Change Planning

For a proposed change, emit:

- source repository;
- affected repositories;
- dependency edge supporting each impact;
- required order;
- migration and rollback plan;
- per-repository tests;
- integration proof;
- release coordination;
- unresolved risks.

Avoid broad synchronized edits when a shared package, schema, or adapter can provide a cleaner boundary.

## 17. Reconciliation and Receipt Writing

Each run emits:

- mission and scope;
- discovery sources;
- snapshot identifiers;
- repositories considered;
- repositories deeply inspected;
- exclusions and unavailable sources;
- identity decisions;
- per-repository results;
- contradictions;
- changes made;
- current revisions;
- tests and artifacts;
- aggregate decision;
- unresolved items;
- next highest-value action.

Receipts are append-only evidence; generated current-state views may be replaced only through a new source-bound receipt.

## 18. Map Regeneration

After repository state, identity, classification, or relationship changes:

1. update the controlling source records;
2. run classification and contract tests;
3. regenerate catalog, domain, foundation, status, and website projections;
4. verify counts and scope notes;
5. compare the delta;
6. emit a regeneration receipt;
7. block release if projections disagree.

## 19. Company and Frontier Mapping

Do not require a company-named repository to build a company-specific dossier.

Map:

```text
company/domain
→ current bottlenecks
→ required capabilities
→ verified GlacierEQ capabilities
→ flagships and donor repositories
→ missing proof or tailored demonstration
```

Keep direct company exhibits distinct from reusable personal systems and from upstream study repositories.

## 20. Website Projection

Compose with Web Design Pro to generate:

- zoomable repository constellations;
- company bottleneck maps;
- capability donor graphs;
- system evolution timelines;
- evidence-state matrices;
- dependency impact views;
- Stone academy mind maps;
- machine query surfaces.

Every projection inherits Monolith's scope, ownership, evidence, and freshness boundaries.

## 21. Large-Scale Review Heuristics

Prioritize deep inspection when a repository is:

- a foundation or whole system;
- on the critical path;
- publicly promoted;
- a shared dependency;
- recently changed;
- contradictory;
- failing;
- security-sensitive;
- identity-unresolved;
- a likely high-value donor;
- connected to many downstream nodes.

Deprioritize or quarantine:

- obvious backups;
- untouched forks;
- generated copies;
- stale duplicates;
- private sensitive surfaces unrelated to the mission;
- unsupported brand-shaped experiments.

## 22. Completion Standard

A repository-scale mission is complete only when:

- scope and coverage are explicit;
- mutable targets came from current discovery;
- aliases and duplicates are reconciled or quarantined;
- the mission subgraph is complete enough for the requested decision;
- owning repositories were inspected before runtime claims;
- required proof paths were executed or visibly blocked;
- contradictions remain visible until resolved;
- generated projections agree with canonical state;
- receipts identify exact revisions and limitations;
- no prior verified gain was discarded.
