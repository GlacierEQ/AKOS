# AKOS Public Action Face Architecture

**Status:** Active governing architecture  
**Effective:** 2026-07-14

## Canonical roles

| Role | Repository | Required visibility | GitHub Actions posture |
|---|---|---:|---:|
| Public action face and execution plane | `GlacierEQ/public-actions-runner-host` | Public | Sole execution owner |
| Private runner-team control plane | `GlacierEQ/llm-runner-teams` | Private | No executable workflows |
| Private workload repositories | Approved `GlacierEQ/*` sources | Private or public | No Actions when private |
| AKOS | `GlacierEQ/AKOS` | Private | Canonical policy and routing truth |

## Prime law

> All GitHub Actions execution, public run identity, workflow badges, and sanitized status belong to `GlacierEQ/public-actions-runner-host`.

`GlacierEQ/llm-runner-teams` is the private policy, approval, and result brain. It must not become the workflow owner, billed execution owner, or public run face.

## Full route

```text
Intake
  external connector / public issue / public repository_dispatch
Bind
  job ID + pillar + action + source ref + approval ID where required
Route
  GlacierEQ/public-actions-runner-host
Execute
  GitHub-hosted ubuntu-latest + allowlisted adapter + ephemeral workload checkout
Validate
  quality / function / security / hardening evidence
Review
  sanitized public status + detailed private receipt
Release
  release, release with limitations, or block
Ledger
  GlacierEQ/llm-runner-teams results and AKOS continuity record
Handoff
  exact next repair or deployment stage
```

## Security invariants

1. The public action face must be public. A visibility guard blocks execution if it is private.
2. The private control plane contains no executable `.yml` or `.yaml` files under `.github/workflows/`.
3. Private workload repositories do not run Actions or use a private `workflow_call` chain.
4. Public job envelopes contain metadata only.
5. Evidence, document contents, prompts, credentials, messages, private logs, and detailed output remain private.
6. Private checkout credentials are not persisted.
7. Control-plane tokens are scoped only to approval verification and private result publication, never workload execution.
8. Pillars G and I require an exact private dual-confirmation record.
9. Detailed results return to `GlacierEQ/llm-runner-teams`; public status remains sanitized.

## Public events

The public action face owns the nine pillar events plus migrated execution events:

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
```

## Release gate

Execution is blocked when any of the following is true:

- `GlacierEQ/public-actions-runner-host` is not public;
- executable workflows exist in `GlacierEQ/llm-runner-teams`;
- a private workload repository is the Actions owner;
- a public envelope contains protected content;
- secrets are available to workload code;
- a dual-gated operation lacks matching private approval;
- detailed results cannot return privately.

## Governing implementation

- Public contract: `GlacierEQ/public-actions-runner-host/docs/ACTION_FACE_CONTRACT.md`
- Public workflow: `GlacierEQ/public-actions-runner-host/.github/workflows/apex-pillar-runner.yml`
- Private contract: `GlacierEQ/llm-runner-teams/docs/ACTION_FACE_CONTROL_PLANE.md`
- Private policy: `GlacierEQ/llm-runner-teams/policy/no-private-actions.json`
- Retirement evidence: `GlacierEQ/llm-runner-teams/docs/migrations/2026-07-14-private-actions-retirement.json`

No private-repository Actions exception exists.
