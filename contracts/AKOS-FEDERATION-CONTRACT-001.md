# AKOS-FEDERATION-CONTRACT-001

Status: active draft  
Version: 1.0.0  
Family: FAM-CASEBRAIN  
Updated: 2026-07-14

## Purpose

This contract federates CASEBRAIN powerups without confusing documentation,
model output, projections, or connector presence with verified case truth or
runtime health. GitHub owns code and contract canon. CASEBRAIN owns validated
memory records. Notion and ClickUp are review and execution projections.

## Authority boundaries

- `GlacierEQ/AKOS` owns repository identity, roles, lifecycle, quality gates,
  adoption and promotion.
- `GlacierEQ/AEON-777` pull request 51 owns the proposed CASEBRAIN truth,
  provenance and human-action rules.
- Original evidence remains in its source system. Every derivative is a
  projection and may never replace the original.
- Casebuilder, Aspen Grove, Make-It-Heavy, Token Saver and Pro-Code may provide
  bounded capabilities only through this contract.
- A repository, worker or connector is not live merely because it is named,
  configured, initialized, reachable or described as live. `verified_live`
  requires a dated run receipt in the Verification Ledger.

## Repository adoption

Every participating repository must carry a valid AKOS adoption manifest with:

- canonical ID and `family_id: FAM-CASEBRAIN`;
- semantic version and allowed lifecycle status;
- purpose and architectural layer;
- all seven AKOS Pro-Code quality gates;
- explicit dependencies and mirror/supersession relationships;
- confidence, verification status, full hash and review date;
- dependencies pinned by repository, commit SHA and path.

Floating `main` references and machine-local absolute paths are prohibited in
production dispatches.

## CASEBRAIN transport envelope

The strict CASEBRAIN payload schemas remain unchanged. Adapters wrap a valid
payload in this immutable transport envelope:

```json
{
  "envelope_version": "1.0.0",
  "trace_id": "00000000-0000-4000-8000-000000000000",
  "idempotency_key": "producer/resource/payload-sha256",
  "producer": {
    "repo": "GlacierEQ/repository",
    "commit_sha": "0000000000000000000000000000000000000000",
    "component": "read-only-adapter"
  },
  "payload_schema_id": "urn:casebrain:schema:case-event:1.0.0",
  "payload_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "emitted_at": "2026-07-15T08:30:00Z",
  "payload": {}
}
```

Before routing, the payload must validate against the pinned schema and its
canonical JSON bytes must match `payload_sha256`.

## Canonical resource mesh

```json
{
  "resource_id": "stable-resource-id",
  "case_id": "1FDV-23-0001009",
  "kind": "court_record",
  "source": {
    "canonical_uri": "provider://stable-id",
    "source_kind": "original",
    "locator": "page-or-timestamp",
    "sha256": "64-hex-digest",
    "version": "provider-version",
    "last_checked_at": "2026-07-15T08:30:00Z"
  },
  "projections": [
    {
      "system": "casebrain",
      "uri": "casebrain://resource-id",
      "role": "index",
      "status": "linked",
      "sha256": "64-hex-digest",
      "last_synced_at": "2026-07-15T08:30:00Z"
    }
  ],
  "sensitivity": "restricted_case_data",
  "review_gate": "human_review_required",
  "supersedes": [],
  "updated_at": "2026-07-15T08:30:00Z"
}
```

There is one canonical source. GitHub, CASEBRAIN, Notion, ClickUp, Supabase and
Drive entries are explicit originals, working views, indexes, filing packages
or backups. Projections never overwrite originals.

## Worker dispatch

```json
{
  "task_id": "00000000-0000-4000-8000-000000000000",
  "trace_id": "00000000-0000-4000-8000-000000000000",
  "case_id": "1FDV-23-0001009",
  "capability": "extract_case_event",
  "input_resource_ids": ["resource-id"],
  "producer": {
    "repo": "GlacierEQ/AKOS",
    "commit_sha": "0000000000000000000000000000000000000000"
  },
  "constraints": {
    "read_only": true,
    "external_actions": false,
    "allowed_tools": [],
    "max_runtime_seconds": 300,
    "max_cost": 0
  },
  "output_schema_id": "urn:casebrain:schema:case-event:1.0.0",
  "idempotency_key": "stable-dispatch-key"
}
```

Every worker result remains non-authoritative until reviewed:

```json
{
  "task_id": "00000000-0000-4000-8000-000000000000",
  "status": "completed",
  "outputs": [],
  "claim_class": "model_inference",
  "verification_status": "pending_review",
  "citations": [],
  "errors": [],
  "metrics": {}
}
```

Workers may propose; they may not promote themselves or their output.

## Storage adapters

Supabase, Notion, CASEBRAIN and other adapters accept validated envelopes only.
Each stored projection must include stable `resource_id`, `case_id`, claim class,
verification status, source pointers, full SHA-256, sensitivity, human-review
requirement, trace ID, idempotency key and producer commit SHA.

Storage requirements:

- unique `(case_id, resource_id, payload_sha256)`;
- append-only audit;
- idempotent retry;
- authenticated operator and case-scoped access;
- no service-role credential in a UI, client or MCP surface;
- no unrestricted `using (true)` case-data policy;
- no evidence record without source and full hash.

Notion receives pointers, queues and receipts—not evidence bodies or secrets.
ClickUp reflects manual execution state but never overwrites GitHub canon.

## Human gates

The lifecycle is `draft -> check -> verify -> finalize -> save -> push`.
Explicit, named approval is mandatory for filing, service, court contact,
evidence release, publication, external escalation, deadline confirmation,
fact promotion, production writes and connector activation.

Threat signals always set external action authorization to false, preserve
alternative explanations and route to a human decision.

## Activation states

- `contract_pending`: inspected but no compatible adoption contract.
- `sandbox_candidate`: bounded read-only experiment may be built.
- `repair_required`: inspected defects block activation.
- `review_ready`: contract or PR is ready for human review, not production.
- `blocked`: a security, provenance or runtime prerequisite is unmet.
- `quarantined`: content may be researched but cannot seed verified truth.
- `verified_live`: a dated deployment and run receipt passed its verification
  rule; this state exists in the Worker Registry, not by documentation claim.

## Prohibited federation behavior

No component may automatically file, serve, publish, contact a court or person,
release evidence, escalate externally, assert an unconfirmed deadline, convert
an allegation or model inference into verified fact, or propagate credentials.

## First accepted integration slice

1. Merge a valid AKOS manifest and this reviewed federation contract.
2. Rotate the credential exposed in AEON history and reconcile indexing.
3. Pin the reviewed AEON schema commit.
4. Select one primary court record and compute a local full SHA-256.
5. Run one read-only Casebuilder adapter to produce one CASE_EVENT envelope.
6. Validate the envelope, write to hardened staging, recall it, compare hashes
   and append an immutable receipt.
7. Only then consider promoting a single worker from `design` to `dry_run`.
