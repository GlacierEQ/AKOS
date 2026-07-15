# CASEBRAIN Powerup Federation

Status: review ready, not production  
Updated: 2026-07-14  
Canonical family: `FAM-CASEBRAIN`

## Outcome

The private-repository powerups now have one proposed topology, explicit claim
boundaries, pinned source revisions and a safe activation order. “Activated”
means contract-adopted and receipt-verified; it does not mean bulk merged or
automatically executed.

## Topology

1. AKOS governs identity, contracts, lifecycle and promotion.
2. AEON-777 pull request 51 governs CASEBRAIN truth and provenance.
3. Aspen Grove owns resource and repository pointers after repair.
4. Casebuilder and Make-It-Heavy provide bounded read-only worker candidates.
5. Token Saver provides content-addressed pointer concepts after round-trip
   testing.
6. Notion mirrors review queues and receipts; ClickUp mirrors manual execution.
7. Pro-Code is the operator UI only after signed dispatch is implemented.

## Canon and projection rules

| System | Federated role | Authority |
|---|---|---|
| GitHub | Contracts, schemas, code and immutable review history | canonical |
| CASEBRAIN | Validated memory index | canonical only for records that pass pinned schemas |
| Notion | Navigation, work packets, review queue and receipt links | projection |
| ClickUp | Manual execution visibility | projection |
| Drive/source systems | Originals and preparation pointers | source-dependent; not automatically factual canon |
| Supabase | Optional query projection after hardening | blocked |

## Safe activation order

1. Review the AKOS manifest repair and federation contract.
2. Rotate the exposed AEON credential and reconcile project discovery/indexing.
3. Resolve overlaps around AEON pull requests 49–51; preserve pull request 51's
   strict truth contracts.
4. Reconcile SUPERLUMINAL pull requests 51 and 52 as the Casebuilder
   runtime/governance candidate.
5. Build one hashed, read-only Casebuilder source adapter and retain all output
   as pending review.
6. Harden Aspen Supabase RLS, provenance fields and service-role boundaries.
7. Add signed dispatch, case ID, trace ID, deployment receipts and an actual
   kill switch to the lowercase `pro-code` UI.
8. Sandbox Make-It-Heavy and Token Saver behind budgets, hashes and citations.
9. Keep `apex-bootup-core` blocked until it has a dry run, explicit allowlist,
   exit checks and rollback.

## Notion worker control plane

Reuse the current Aspen SSOT, AKOS Engineering Hub, AWorkers, Casebuilder
Cathedral, HIVE Command and Worker Registry. Do not create another competing
master hub.

The Worker Registry needs these additions:

- Worker ID, layer L0–L4, manager, case/lane and capability;
- status: Design, Dry Run, Verified Live, Paused, Failed or Retired;
- risk class, run mode, repo and commit, deployment ID;
- input/output schema references and evidence-mutation permission;
- external-side-effect flag, human gate and kill switch;
- last run and last verified receipt.

Add linked Work Packets, immutable Worker Runs, Source/Memory Pointers and Human
Review/Exceptions. The existing Verification Ledger is the only proof gate for
`Verified Live`.

## Quarantine notes

- The Notion “UNIFIED CASE BRAIN — SUPERINTELLIGENCE ORCHESTRATOR” contains
  unsupported live-status, docket-count, fraud-confidence, escalation and
  outcome claims. Preserve it read-only and migrate only primary-source-backed
  rows.
- Casebuilder relationship/narrative outputs and the case-specific Aspen README
  contain allegations, correlations and unsupported percentages. They cannot
  seed verified memories.
- Plaintext credentials were observed in repository history and Notion pages.
  Rotate them provider-side and never ingest their values into CASEBRAIN.
- `apex-bootup-core` and `apex-boot-core` are distinct repositories.
- `Pro_Code` is the standards brain mirror; lowercase `pro-code` is the UI.

## Initial worker fleet

Only read-only workers are proposed: Source Intake/Hasher, Timeline Normalizer,
Contradiction Candidate, Memory Distiller, Notion Review Mirror and Operator
Control. Every model-derived result is `model_inference/pending_review`.

No automatic filing, service, publication, court contact, evidence release,
external escalation, deadline assertion or fact promotion is permitted.
