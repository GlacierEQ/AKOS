# AKOS Current State

Status: Active Draft  
Version: 0.3.0  
Updated: 2026-07-21

## Purpose

This is the single read-first state file for AKOS sessions.

Read it after `README.md`, `AKOS_MANIFEST.yaml`, and `BUILD_INDEX.md` before
making changes.

## Canonical Repository

```text
GlacierEQ/AKOS
```

## Current Position

AKOS is the proposed governance root for the CASEBRAIN powerup federation and
the canonical home for Operational Cognition contracts.

It owns identities, contracts, lifecycle, quality gates, promotion, capability
selection, execution gates and receipt requirements—not case facts, evidence
originals or unverified runtime truth.

The federation is review ready on a branch. It is not production live.
Operational Cognition is implemented on branch with tests and machine contracts;
it is not connector-wired or promoted to working canon yet.

## Current Build Layer

```text
Receipt-driven operational cognition over truth-safe repository federation
```

## Locked System Roles

1. GitHub: canonical contracts, schemas and code.
2. CASEBRAIN: validated source-linked memory index.
3. Notion: navigation, worker review queues and receipt pointers.
4. ClickUp: manual execution visibility.
5. Drive/source systems: source and preparation pointers, not automatic truth
   canon.
6. Supabase: optional staging/query projection after hardening.
7. AKOS Operational Cognition: capability selection, authority gates,
   orchestration, verification, persistence and handoff policy.

## Active Read Path

1. `README.md`
2. `AKOS_MANIFEST.yaml`
3. `BUILD_INDEX.md`
4. `CURRENT_STATE.md`
5. `specs/AKOS-OC-001_OPERATIONAL_COGNITION.md`
6. `operational_cognition/README.md`
7. `contracts/AKOS-FEDERATION-CONTRACT-001.md`
8. `manifests/federations/CASEBRAIN_POWERUP_FEDERATION.json`
9. `docs/federation/CASEBRAIN_POWERUP_FEDERATION.md`
10. Relevant integration spec

## Operational Cognition Status

```text
Implemented on Branch — Unit-Tested Locally — CI and Connector Receipts Pending
```

Implemented:

- deterministic capability selection favoring authoritative, verifiable and
  persistent tools;
- explicit source routing for connected private sources, Files, current public
  sources and local runtimes;
- operator authorization and explicit approval gates by operation class;
- provider-receipt requirement for claimed writes;
- validation and persistence requirements before completion;
- monotonic runtime pipeline and artifact lifecycle;
- Architect Assertion preservation as an active allegation without false
  promotion to independently verified fact;
- machine schema, runtime manifest, tests and CI workflow.

Promotion still requires one audited read-only connector probe and one
receipt-backed reversible write probe.

## CASEBRAIN Federation Status

```text
Review Ready — Production Writes Blocked
```

Completed in the proposed pack:

- self-validating AKOS manifest repair;
- strict federation registry schema;
- commit-pinned repository and worker registry;
- transport, resource, dispatch, result, storage and human-gate contracts;
- repository quarantine and activation boundaries;
- Notion worker-control-plane mapping;
- append-only build ledger entry.

## ClickUp Integration Status

```text
Manual Stage Complete — Automation Candidate Blocked
```

ClickUp may reflect execution state. It may not overwrite GitHub canon, bulk
generate tasks or automatically mutate connected systems.

## Critical Blockers

- Rotate the memory credential exposed in AEON history.
- Reconcile CASEBRAIN project discovery and indexing.
- Resolve overlapping AEON pull requests without weakening PR 51 truth rules.
- Reconcile SUPERLUMINAL pull requests 51 and 52.
- Replace Aspen local paths and simulated health with receipt-backed probes.
- Harden Aspen Supabase RLS, case scoping, hashing and service-role boundaries.
- Bring lowercase `pro-code` dispatch/auth/tracing implementation up to its
  documented contract.
- Rotate plaintext credentials exposed in Notion pages.
- Validate AKOS-OC-001 through one read-only and one reversible-write provider
  receipt path before promotion.

## Highest-Leverage Next Action

Review and merge the federation contract and Operational Cognition change, rotate
the exposed credentials, then run one hashed court record through a read-only
Casebuilder adapter under AKOS-OC-001 and verify the recalled hash and ledger
receipt.

## Machine Summary

```json
{
  "document": "CURRENT_STATE",
  "version": "0.3.0",
  "status": "active_draft",
  "current_layer": "receipt_driven_operational_cognition_over_truth_safe_federation",
  "operational_cognition": "implemented_branch_ci_and_connector_receipts_pending",
  "casebrain_federation": "review_ready_production_writes_blocked",
  "clickup_status": "manual_stage_complete_automation_candidate_blocked",
  "highest_leverage_next_action": "merge governed changes, rotate credentials, run one audited read-only source-to-recall probe through AKOS-OC-001"
}
```
