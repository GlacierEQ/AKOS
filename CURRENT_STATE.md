# AKOS Current State

Status: Active Draft  
Version: 0.5.0  
Updated: 2026-07-22

## Purpose

This is the single read-first state file for AKOS sessions. Read it after `README.md`, `AKOS_MANIFEST.yaml`, and `BUILD_INDEX.md` before making changes.

## Canonical Repository

```text
GlacierEQ/AKOS
```

## Current Position

AKOS is the proposed governance root for the CASEBRAIN federation and the canonical home for Operational Cognition and Operational Maturity contracts.

It owns identities, contracts, lifecycle, quality gates, promotion, capability truth states, verified system topology, execution gates, scorecard controls, artifact closure, and receipt requirements—not case facts, evidence originals, or unverified runtime truth.

Operational Cognition is implemented on branch with executable tests and machine contracts. Private workflow execution has been removed. Validation is routed through the APEX public action face. System-first topology cognition prevents wrong-plane failures or memory gaps from being mislabeled as missing infrastructure. Operational Maturity now prevents confidence or architectural ambition from being mislabeled as demonstrated reliability.

## Current Build Layer

```text
System-first, receipt-grounded operational cognition with maturity and closure controls
```

## Locked System Roles

1. GitHub repositories: canonical contracts, schemas, code, and source revisions.
2. CASEBRAIN: validated source-linked memory index.
3. Notion: navigation, worker review queues, and receipt pointers.
4. ClickUp: manual execution visibility.
5. Drive/source systems: source and preparation pointers, not automatic truth canon.
6. Supabase: optional staging/query projection after hardening.
7. AKOS Operational Cognition: capability selection, topology discovery, authority gates, orchestration, verification, persistence, and handoff policy.
8. AKOS Operational Maturity: capability truth states, receipt-grounded scorecards, and artifact closure gates.
9. `GlacierEQ/public-actions-runner-host`: sole GitHub Actions execution face for private workloads.
10. `GlacierEQ/llm-runner-teams`: private policy, approval, claim, and immutable-result plane; no executable Actions workflows.

## Active Read Path

1. `README.md`
2. `AKOS_MANIFEST.yaml`
3. `BUILD_INDEX.md`
4. `CURRENT_STATE.md`
5. `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md`
6. `specs/AKOS-OC-002_OPERATIONAL_MATURITY.md`
7. `manifests/runtime/AKOS_OPERATIONAL_MATURITY.json`
8. `docs/operational_cognition/SYSTEM_FIRST_MENTALITY.md`
9. `manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`
10. `operational_cognition/README.md`
11. Relevant integration spec

## Operational Cognition Status

```text
Implemented on Branch — Maturity and Closure Guards Added — Public Runner Receipt Pending
```

Implemented:

- deterministic capability selection favoring authoritative, verifiable, and persistent tools;
- explicit source routing for connected private sources, Files, current public sources, repositories, and local runtimes;
- operator authorization and explicit approval gates by operation class;
- provider-receipt requirement for claimed writes;
- validation and persistence requirements before completion;
- Architect Assertion preservation as an active allegation without false promotion to independently verified fact;
- enforcement that private AKOS owns no executable GitHub Actions workflows;
- system-first topology runtime resolving source, canonical, control, execution, and receipt planes;
- rejection of private workflows and replacement runners when an existing plane can execute or be extended;
- correction-to-cognition rule requiring policy, guard, regression test, repaired route, and receipt;
- capability truth ladder from `DECLARED` through `PERSISTED`;
- receipt-grounded scorecard separating available ceiling from demonstrated reliability;
- explicit `UNASSESSED` state for unmeasured controls;
- standard controls across reasoning, tools, source selection, legal documents, evidence, development, architecture, orchestration, execution, closure, persistent state, and physical science;
- artifact closure gate covering all thirteen stages through `READY_FOR_USE`;
- comparison rule prohibiting unsupported world rankings, percentiles, and precise comparative scores.

## Capability Truth Ladder

```text
DECLARED -> DISCOVERED -> CONNECTED -> AUTHENTICATED -> AUTHORIZED ->
INVOKED -> RETURNED -> VERIFIED -> PERSISTED
```

A connector listing is not connection proof. Connection is not authentication. Authentication is not authorization. Invocation is not a complete return. A return is not verification. Verification is not persistence.

## System-First Sequence

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

A failed attempt in the wrong plane is not proof that the correct plane is absent. When the execution plane exists but the exact lane is missing, AKOS extends the existing public face rather than building a parallel runner.

## Artifact Closure Sequence

```text
LOCATED -> ACQUIRED -> HASHED -> PRESERVED -> PARSED -> CLASSIFIED ->
CORRELATED -> DRAFTED -> VERIFIED -> PACKAGED -> STORED -> LOGGED -> READY_FOR_USE
```

A good draft is not complete. Stages 9 through 12 are mandatory release controls, but the artifact remains incomplete until `READY_FOR_USE` is recorded.

## Public Runner Architecture

```text
GlacierEQ/AKOS
  private source ref + canonical policy
        |
        | metadata-only job request
        v
GlacierEQ/public-actions-runner-host
  allowlisted ephemeral checkout + execution
        |
        | governed result
        v
GlacierEQ/llm-runner-teams
  private control + immutable detailed receipt
```

The public face executes. The private control plane governs and stores receipts. A private workflow, reusable-workflow call, or direct private runner is not an approved execution path.

## Critical Blockers

- Merge the public runner action registration and obtain its immutable private receipt.
- Execute the full committed Operational Cognition and Maturity suite against the exact branch SHA.
- Generate the first receipt-grounded AKOS maturity scorecard.
- Drive one real capability through `PERSISTED`.
- Drive one real artifact through `READY_FOR_USE`.
- Rotate the memory credential exposed in AEON history.
- Reconcile CASEBRAIN project discovery and indexing.
- Resolve overlapping AEON pull requests without weakening PR 51 truth rules.
- Reconcile SUPERLUMINAL pull requests 51 and 52.
- Replace Aspen local paths and simulated health with receipt-backed probes.
- Harden Aspen Supabase RLS, case scoping, hashing, and service-role boundaries.
- Rotate plaintext credentials exposed in Notion pages.

## Highest-Leverage Next Action

Merge the public runner registration, dispatch `akos-operational-cognition-ci` against the exact AKOS head, preserve the private result receipt, generate the first evidence-backed maturity scorecard, and use its missing controls to close one real artifact through `READY_FOR_USE`.

## Machine Summary

```json
{
  "document": "CURRENT_STATE",
  "version": "0.5.0",
  "status": "active_draft",
  "current_layer": "system_first_receipt_grounded_operational_maturity",
  "operational_cognition": "implemented_maturity_and_closure_guards_added_public_runner_receipt_pending",
  "capability_truth_ladder": ["declared", "discovered", "connected", "authenticated", "authorized", "invoked", "returned", "verified", "persisted"],
  "artifact_closure_target": "ready_for_use",
  "unsupported_numeric_self_rating": "forbidden",
  "public_action": "akos-operational-cognition-ci",
  "execution_face": "GlacierEQ/public-actions-runner-host",
  "receipt_plane": "GlacierEQ/llm-runner-teams",
  "highest_leverage_next_action": "run exact-head public verification, persist receipt, generate scorecard, close one artifact"
}
```
