# AKOS Current State

Status: Active Draft  
Version: 0.4.1  
Updated: 2026-07-21

## Purpose

This is the single read-first state file for AKOS sessions. Read it after `README.md`, `AKOS_MANIFEST.yaml`, and `BUILD_INDEX.md` before making changes.

## Canonical Repository

```text
GlacierEQ/AKOS
```

## Current Position

AKOS is the proposed governance root for the CASEBRAIN federation and the canonical home for Operational Cognition contracts.

It owns identities, contracts, lifecycle, quality gates, promotion, capability selection, verified system topology, execution gates, and receipt requirements—not case facts, evidence originals, or unverified runtime truth.

Operational Cognition is implemented on branch with executable tests and machine contracts. Private workflow execution has been removed. Validation is routed through the APEX public action face. System-first topology cognition now prevents AKOS from mistaking wrong-plane failures or memory gaps for missing infrastructure.

## Current Build Layer

```text
System-first, receipt-driven operational cognition over truth-safe repository federation
```

## Locked System Roles

1. GitHub repositories: canonical contracts, schemas, code, and source revisions.
2. CASEBRAIN: validated source-linked memory index.
3. Notion: navigation, worker review queues, and receipt pointers.
4. ClickUp: manual execution visibility.
5. Drive/source systems: source and preparation pointers, not automatic truth canon.
6. Supabase: optional staging/query projection after hardening.
7. AKOS Operational Cognition: capability selection, topology discovery, authority gates, orchestration, verification, persistence, and handoff policy.
8. `GlacierEQ/public-actions-runner-host`: sole GitHub Actions execution face for private workloads.
9. `GlacierEQ/llm-runner-teams`: private policy, approval, claim, and immutable-result plane; no executable Actions workflows.

## Active Read Path

1. `README.md`
2. `AKOS_MANIFEST.yaml`
3. `BUILD_INDEX.md`
4. `CURRENT_STATE.md`
5. `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md`
6. `docs/operational_cognition/SYSTEM_FIRST_MENTALITY.md`
7. `manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json`
8. `operational_cognition/README.md`
9. `contracts/AKOS-FEDERATION-CONTRACT-001.md`
10. Relevant integration spec

## Operational Cognition Status

```text
Implemented on Branch — System-First Guards Added — Public Runner Registration Pending Merge and Receipt
```

Implemented:

- deterministic capability selection favoring authoritative, verifiable, and persistent tools;
- explicit source routing for connected private sources, Files, current public sources, repositories, and local runtimes;
- operator authorization and explicit approval gates by operation class;
- provider-receipt requirement for claimed writes;
- validation and persistence requirements before completion;
- monotonic runtime pipeline and artifact lifecycle;
- Architect Assertion preservation as an active allegation without false promotion to independently verified fact;
- machine schemas, runtime manifests, unit tests, architecture tests, topology tests, and `pytest.ini` discovery;
- enforcement that private AKOS owns no executable GitHub Actions workflows;
- public runner action registration proposed as `akos-operational-cognition-ci` under Pillar C;
- system-first topology runtime that resolves source, canonical, control, execution, and receipt planes;
- rejection of private workflows, replacement runners, and duplicate control planes when an existing route or extensible plane exists;
- bounded-extension rule: add one catalog action, adapter, or route binding before creating infrastructure;
- correction-to-cognition rule: every material correction becomes policy, executable guard, regression test, repaired route, and append-only receipt.

## System-First Sequence

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

AKOS must inspect canonical manifests, catalogs, adapters, open pull requests, connected capabilities, and receipt stores before declaring a blocker.

A failed attempt in the wrong plane is not proof that the correct plane is absent. A conversation-memory failure is not proof that the architecture is absent. When the execution plane exists but the exact lane is missing, AKOS extends the existing public face rather than building a parallel runner.

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

## CASEBRAIN Federation Status

```text
Review Ready — Production Writes Blocked
```

Completed in the proposed pack:

- self-validating AKOS manifest repair;
- strict federation registry schema;
- commit-pinned repository and worker registry;
- transport, resource, dispatch, result, storage, and human-gate contracts;
- repository quarantine and activation boundaries;
- Notion worker-control-plane mapping;
- append-only build ledger entry.

## Critical Blockers

- Merge the public runner action registration and obtain its immutable private receipt.
- Rotate the memory credential exposed in AEON history.
- Reconcile CASEBRAIN project discovery and indexing.
- Resolve overlapping AEON pull requests without weakening PR 51 truth rules.
- Reconcile SUPERLUMINAL pull requests 51 and 52.
- Replace Aspen local paths and simulated health with receipt-backed probes.
- Harden Aspen Supabase RLS, case scoping, hashing, and service-role boundaries.
- Bring lowercase `pro-code` dispatch/auth/tracing implementation up to its documented contract.
- Rotate plaintext credentials exposed in Notion pages.
- Validate AKOS-OC-001 through one read-only and one reversible-write provider receipt path before promotion.

## Highest-Leverage Next Action

Merge the public runner registration, dispatch `akos-operational-cognition-ci` against the exact AKOS branch SHA, preserve the private result receipt, then run one hashed court record through a read-only Casebuilder adapter under AKOS-OC-001.

## Machine Summary

```json
{
  "document": "CURRENT_STATE",
  "version": "0.4.1",
  "status": "active_draft",
  "current_layer": "system_first_receipt_driven_operational_cognition",
  "operational_cognition": "implemented_system_first_guards_added_public_runner_receipt_pending",
  "system_first_sequence": ["discover", "map", "reuse", "extend", "execute", "verify", "persist"],
  "public_action": "akos-operational-cognition-ci",
  "execution_face": "GlacierEQ/public-actions-runner-host",
  "receipt_plane": "GlacierEQ/llm-runner-teams",
  "casebrain_federation": "review_ready_production_writes_blocked",
  "highest_leverage_next_action": "merge runner registration, dispatch exact AKOS ref, preserve immutable receipt"
}
```
