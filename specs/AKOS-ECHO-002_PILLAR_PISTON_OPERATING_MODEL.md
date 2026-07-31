# AKOS-ECHO-002 — Pillar–Piston Operating Model

Canonical ID: AKOS-ECHO-002
Version: 1.0.0
Status: Active
Updated: 2026-07-30

## Identity

- **AKOS:** Apex Knowledge Operating System
- **ECHO:** Engine for Continuity, History, and Orchestration
- **AKOS identity:** `SYS-AKOS-001`
- **ECHO identity:** `SYS-ECHO-001`

## Foundational architecture

AKOS and ECHO form a complementary operating pair.

```text
AKOS — THE PILLAR                    ECHO — THE PISTON
identity                             continuity
truth                                history
provenance                           normalization
authority                            synchronization
contracts                            recall
evidence                             routing
maturity                             execution flow
promotion                            retries
completion truth                     operational receipts
```

AKOS provides the stable structural axis. ECHO provides governed motion around that axis.

AKOS without ECHO risks becoming stable but operationally static. ECHO without AKOS risks becoming active but ungrounded. The pair is complete only when durable governance and continuous orchestration remain connected through explicit contracts and receipts.

## Separation without obstruction

ECHO is separately deployable, independently testable, and permission-isolated. It is not conceptually outside AKOS, nor physically embedded inside AKOS. It occupies a first-class paired-system position:

```text
          AKOS POLICY + TRUTH
                  |
                  v
          ECHO ORCHESTRATION
                  |
                  v
       ACTION + CONTINUITY RECEIPTS
                  |
                  v
          AKOS VERIFICATION
                  |
                  +----> PERSIST / PROMOTE / REPAIR
```

This boundary prevents both loss and obstruction:

- ECHO cannot disappear as an undocumented external dependency.
- AKOS cannot obstruct ECHO by absorbing its product runtime.
- ECHO cannot bypass AKOS authority through uncontrolled motion.
- AKOS cannot claim completion without ECHO execution receipts where motion is required.

## Non-negotiable piston invariants

1. Every durable object has a stable identity and provenance.
2. Every mutation is idempotent or explicitly non-idempotent and gated.
3. Every orchestration attempt returns a receipt or exact blocker.
4. Retries are bounded, observable, and preserve canonical state.
5. Provider degradation cannot destroy local continuity, recall, or export.
6. Provider claims cannot advance beyond current evidence.
7. History is append-preserving; corrections supersede rather than erase.
8. ECHO dynamically reroutes only within AKOS authority.
9. Self-evolution recommendations cannot self-authorize irreversible change.
10. The AKOS–ECHO contract is versioned and independently verified on both sides.

## Full operating cycle

```text
REMEMBER -> RECONCILE -> AUTHORIZE -> ROUTE -> EXECUTE -> RECEIPT ->
VERIFY -> PERSIST -> OBSERVE -> REPAIR -> IMPROVE -> REPEAT
```

## Dynamic excellence

ECHO continuously measures continuity coverage, failed jobs, retry exhaustion, stale provider state, contract drift, orphaned history, and unverified capability claims. It produces prioritized improvement recommendations.

AKOS evaluates those recommendations against authority, safety, evidence, and objective preservation. Approved improvements return to ECHO for implementation and receipt generation.

The system therefore self-evolves without surrendering governance:

```text
ECHO OBSERVES -> AKOS GOVERNS -> ECHO IMPROVES -> AKOS VERIFIES
```

## Completion rule

The pair may claim an operational capability only when:

- AKOS defines its identity, authority, contract, and evidence requirements;
- ECHO implements and executes the capability;
- ECHO emits a verifiable receipt;
- AKOS validates and persists the resulting state; and
- regression gates protect the capability from silent loss.

Architecture alone is not operation. Motion alone is not trustworthy operation. Verified pillar–piston circulation is completion.