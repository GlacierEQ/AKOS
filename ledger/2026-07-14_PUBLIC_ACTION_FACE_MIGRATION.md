# AKOS Ledger — Public Action Face Migration

**Date:** 2026-07-14  
**Pipeline:** Intake → Bind → Route → Execute → Validate → Review → Release → Ledger → Handoff

## Intake

Casey corrected the execution architecture: no GitHub Actions may run in private repositories. The public runner team must be the visible and billed Actions face.

## Bind

- Canonical architecture: `GlacierEQ/AKOS`
- Sole action face: `GlacierEQ/public-actions-runner-host`
- Private control plane: `GlacierEQ/llm-runner-teams`
- Private workload examined: `GlacierEQ/mastermind`

## Route correction

The prior private-repository verification workflow was removed from `GlacierEQ/mastermind` in commit:

```text
dfdffb014a3357c87550999a7fddd981f76895ee
```

The private verification PR was closed without merge.

## Execute

### Public action face

Installed:

- API-backed action-face identity and visibility guard.
- Canonical public action-face contract.
- Extended event planner covering fourteen events.
- Public issue and push-queue planners.
- Dedicated APEX verification, Node CI, and Python CI adapters.
- Timeout, missing-executable, and process-start hardening.
- Step-scoped control-plane credentials.
- Updated public workflow using `ubuntu-latest`.
- Updated public README identifying the repository as the sole Actions face.

Reviewed public revision:

```text
7ec193d811fd5d25d7f7de3aac4682367f76ba33
```

Review commit:

```text
e09749691c4887c9a566ede9e64d4caa47180d86
```

### Private control plane

Preserved all former workflow paths and blob SHAs in:

```text
docs/migrations/2026-07-14-private-actions-retirement.json
```

Retired thirteen executable workflows:

- nine pillar workflows;
- Gateway CI;
- Media Queue;
- WhisperX execution;
- Comet Agent CI.

Installed:

- private control-plane contract;
- no-private-actions policy;
- documentation-only `.github/workflows/README.md`;
- rewritten README and dispatch guide routing all execution to the public face.

Reviewed private revision:

```text
36c9281fd10ba3c0a1934c241f1118132aed12af
```

### AKOS

Canonized the architecture in:

```text
docs/architecture/PUBLIC_ACTION_FACE.md
```

Architecture commit:

```text
e3d3ce7d22d331297fc51390452b41efc7759e2a
```

Release-decision commit:

```text
971321b8aff99b8d64249e37be44d31f57b557da
```

## Validate

### Passed

- Public/private ownership split is explicit.
- Private `mastermind` verification workflow is absent.
- All thirteen private control-plane workflow YAML files are removed from current `main`.
- Public action face exposes nine pillar events plus five migrated events.
- Public workflow runs on GitHub-hosted `ubuntu-latest`.
- Public visibility guard fails closed.
- Private checkout does not persist credentials.
- Control-plane credentials are unavailable to workload execution.
- Detailed results return privately.
- Public output is sanitized.
- Pillars G and I retain private dual-confirmation gates.
- CI and verification adapters convert missing executables, timeouts, and process errors into governed result records.

### Not yet proven

- Successful public action-face runtime.
- Private checkout token availability.
- Private result publication token availability.
- End-to-end APEX verification result receipt.

## Review

Review state:

```text
Architecture ownership: PASS
Private workflow retirement: PASS
Security hardening: PASS
Runtime activation: BLOCKED
```

## Release

```text
Decision: BLOCK ACTIVATION
```

GitHub currently reports:

```text
GlacierEQ/public-actions-runner-host visibility: private
GlacierEQ/llm-runner-teams visibility: private
```

The control-plane visibility is correct. The action-face visibility is incorrect.

The action face must be changed to public before execution. The installed guard intentionally blocks a private host.

## Truth boundary

- No successful public action-face run is claimed.
- No deployment approval is granted.
- No repository visibility change is claimed.
- No secret values were written to source, issue, log, or chat.
- No private Actions route remains approved.

## Handoff

Required external correction:

```text
GlacierEQ/public-actions-runner-host
→ Settings
→ General
→ Danger Zone
→ Change repository visibility
→ Public
```

Then submit one metadata-only verification event:

```json
{
  "event_type": "apex-verification",
  "client_payload": {
    "job_id": "verify-20260714-001",
    "source_ref": "main"
  }
}
```

Next restart point:

```text
Confirm public visibility
→ trigger public action-face smoke run
→ inspect public steps and sanitized status
→ inspect private result receipt
→ review quality/function/security/hardening evidence
→ update AKOS release decision
```
