# AKOS Public Action Face Architecture

**Status:** Active governing architecture; runtime activation blocked pending public visibility and canary evidence  
**Effective:** 2026-07-16

## Canonical roles

| Role | Repository | Required visibility | GitHub Actions posture |
|---|---|---:|---:|
| Public action face and execution plane | `GlacierEQ/public-actions-runner-host` | Public | Sole execution owner |
| Private runner-team control plane | `GlacierEQ/llm-runner-teams` | Private | No executable workflows |
| Private workload repositories | Catalog-approved `GlacierEQ/*` sources | Private or public | No Actions when private |
| AKOS | `GlacierEQ/AKOS` | Private | Canonical policy and routing truth |

## Prime law

> All GitHub Actions execution, public run identity, workflow badges, and sanitized status belong to `GlacierEQ/public-actions-runner-host`.

`GlacierEQ/llm-runner-teams` is the private policy, approval, atomic-claim, and immutable-result brain. It must not become the workflow owner, billed execution owner, or public run face.

No private-repository Actions exception exists.

## Full pipeline

```text
Intake
  authorized owner issue / owner dispatch / pure public queue commit
Bind
  immutable action-face identity + actor login/ID + strict metadata envelope
Route
  GlacierEQ/public-actions-runner-host
Gate
  public visibility + dedicated credentials + private control-plane invariants
Claim
  atomically create claims/<job_id>.json before checkout
Approve
  verify private dual confirmation for pillars G and I
Execute
  immutable checkout pin + catalog-approved workload + isolated ubuntu-latest adapter
Validate
  quality / function / security / hardening / lifecycle evidence
Synthesize
  create a blocked result when approval, checkout, or adapter startup prevents execution
Record
  publish one immutable results/<job_id>.json receipt bound to the claim
Review
  sanitized public status + detailed private result
Release
  release, release with limitations, or block
Ledger
  private claim/receipt + AKOS continuity record
Handoff
  exact next repair, canary, verification, or deployment stage
```

## Immutable public identity

The action face is bound to:

```text
repository: GlacierEQ/public-actions-runner-host
repository ID: 1265621488
owner: GlacierEQ
owner ID: 194243768
default branch: main
visibility: public required
fork: false
archived: false
disabled: false
```

Any mismatch blocks execution before workload planning.

## Authorized principal law

Public accessibility is not execution authority.

The action face validates:

- actor login;
- immutable numeric actor ID;
- event-specific actor role;
- issue `OWNER` association;
- exact issue-title job ID matching the envelope;
- owner-only dispatch and queue routes.

Unauthorized public issue authors never reach workload planning.

## Strict metadata envelope

Only these fields are accepted:

```text
job_id
pillar
action
source_repo
source_ref
task
approval_id
```

The envelope is bounded to 4096 bytes, rejects unknown fields and control characters, prevents action overrides, hardens refs, and restricts base-task repositories to the catalog-derived allowlist.

A queue commit must change exactly one direct `jobs/<job_id>.json` file and nothing else. The filename, issue title where applicable, and envelope job ID must agree.

## Dedicated credentials

No broad PAT fallback is permitted.

- `APEX_PRIVATE_READ_TOKEN`: contents-read checkout of catalog-approved private workloads only.
- `APEX_CONTROL_TOKEN`: private control-plane policy/approval/claim/receipt access only.

The public workflow pins checkout to an immutable action revision and uses `persist-credentials: false`. Bridge-token names and `GITHUB_TOKEN` are removed from workload process environments.

## Private control-plane invariants

Before creating a claim, the action face verifies that `GlacierEQ/llm-runner-teams`:

1. is the correct private, enabled, non-forked repository on `main`;
2. contains no executable workflow YAML;
3. actively forbids GitHub Actions in the control plane and private workloads;
4. points execution to the public action face;
5. requires one atomic claim and one immutable receipt per job ID;
6. forbids claim/result overwrite and deletion;
7. requires provenance and payload-hash receipt fields.

## Atomic claims and immutable receipts

The first authorized run to create:

```text
claims/<job_id>.json
```

wins the job ID. Concurrent or later attempts fail before checkout.

Every governed claimed attempt produces or attempts to produce:

```text
results/<job_id>.json
```

A synthesized blocked result records approval denial, checkout failure, or adapter non-start when the pipeline can continue. Abrupt external interruption leaves the immutable claim as evidence of an incomplete attempt; retry requires a new job ID.

The private receipt binds:

```text
canonical payload SHA-256
claim path and claim blob SHA
canonical plan SHA-256
publication timestamp
workflow run ID and attempt
public runner commit SHA
execution repository
trigger actor and actor ID
source repository and source ref
stage and adapter result
```

Workload success without private receipt success is a blocked release.

## Public events

```text
case-evidence
document-processing
coding-deploy
evolution-optimize
memory-sync
infra-gateway
case-ops
orchestrate
intl-case-ops
media-queue
whisperx-exec
gateway-ci
comet-agent-ci
apex-verification
action-face-canary
```

## Canary gate

Runtime trust requires two stages:

1. `action-face-canary` verifies syntax, JSON contracts, schema alignment, identity/authorization denial paths, immutable checkout pinning, workflow invariants, secret isolation, catalog uniqueness, atomic-claim wiring, append-only receipt wiring, and subprocess output isolation.
2. `apex-verification` runs the target quality/function/security/hardening suite after Stage 1 passes.

No deployment reliance is approved before both stages are reviewed.

## Public/private truth boundary

Public status is limited to identifiers, lane, state, private-ledger state, and public run URL.

Evidence, source contents, legal narratives, document contents, prompts, messages, credentials, private approvals, claims, and detailed result logs remain private.

## Release-blocking conditions

- Public action face is private or its immutable identity changes.
- Private control plane becomes public, forked, archived, disabled, or gains executable workflows.
- A private repository owns an Actions run.
- Dedicated bridge credentials are missing or over-broad.
- Unauthorized ingress reaches planning.
- Invalid, oversized, mixed-path, or conflicting metadata is accepted.
- Workload code receives bridge credentials.
- A job can execute without an atomic private claim.
- A claim or result can be overwritten or deleted.
- A dual-gated operation lacks matching private approval.
- A claimed attempt cannot produce a governed private lifecycle result when the workflow remains operational.
- Detailed results appear publicly.
- Canary, target verification, or private publication fails.

## Governing implementation

- Public contract: `GlacierEQ/public-actions-runner-host/docs/ACTION_FACE_CONTRACT.md`
- Public canary: `GlacierEQ/public-actions-runner-host/docs/CANARY_PROTOCOL.md`
- Public workflow: `GlacierEQ/public-actions-runner-host/.github/workflows/apex-pillar-runner.yml`
- Public secret contract: `GlacierEQ/public-actions-runner-host/config/required-secrets.json`
- Private control contract: `GlacierEQ/llm-runner-teams/docs/ACTION_FACE_CONTROL_PLANE.md`
- Private claim/receipt protocol: `GlacierEQ/llm-runner-teams/docs/IMMUTABLE_CLAIM_RECEIPT_PROTOCOL.md`
- Private no-Actions policy: `GlacierEQ/llm-runner-teams/policy/no-private-actions.json`
- Private immutable-result policy: `GlacierEQ/llm-runner-teams/policy/immutable-results.json`
- Retirement evidence: `GlacierEQ/llm-runner-teams/docs/migrations/2026-07-14-private-actions-retirement.json`
