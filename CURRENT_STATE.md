# AKOS Current State

Status: Active Draft  
Version: 0.2.0  
Updated: 2026-07-14

## Purpose

This is the single read-first state file for AKOS sessions.

Read it after `README.md`, `AKOS_MANIFEST.yaml`, and `BUILD_INDEX.md` before
making changes.

## Canonical Repository

```text
GlacierEQ/AKOS
```

## Current Position

AKOS is the proposed governance root for the CASEBRAIN powerup federation.
It owns identities, contracts, lifecycle, quality gates and promotion—not case
facts, evidence originals or runtime truth.

The federation is review ready on a branch. It is not production live.

## Current Build Layer

```text
Truth-safe repository federation and read-only integration planning
```

## Locked System Roles

1. GitHub: canonical contracts, schemas and code.
2. CASEBRAIN: validated source-linked memory index.
3. Notion: navigation, worker review queues and receipt pointers.
4. ClickUp: manual execution visibility.
5. Drive/source systems: source and preparation pointers, not automatic truth
   canon.
6. Supabase: optional staging/query projection after hardening.

## Active Read Path

1. `README.md`
2. `AKOS_MANIFEST.yaml`
3. `BUILD_INDEX.md`
4. `CURRENT_STATE.md`
5. `contracts/AKOS-FEDERATION-CONTRACT-001.md`
6. `manifests/federations/CASEBRAIN_POWERUP_FEDERATION.json`
7. `docs/federation/CASEBRAIN_POWERUP_FEDERATION.md`
8. Relevant integration spec

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

## Highest-Leverage Next Action

Review and merge the federation contract, rotate the exposed credentials, then
run one hashed court record through a read-only Casebuilder adapter into a
hardened staging projection and verify the recalled hash.

## Machine Summary

```json
{
  "document": "CURRENT_STATE",
  "version": "0.2.0",
  "status": "active_draft",
  "current_layer": "truth-safe repository federation",
  "casebrain_federation": "review_ready_production_writes_blocked",
  "clickup_status": "manual_stage_complete_automation_candidate_blocked",
  "highest_leverage_next_action": "review contract, rotate credentials, run one audited read-only source-to-recall probe"
}
```
