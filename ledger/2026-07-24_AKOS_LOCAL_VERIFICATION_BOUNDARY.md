# AKOS Ledger — Repository-Local Verification Boundary

**Date:** 2026-07-24  
**Scope:** `GlacierEQ/AKOS` integrity verification and public-action-face consistency

## Intake

The AKOS integrity watchdog existed without a repository-wide status gate. The first proposed gate exposed a contradiction with the 2026-07-16 public-action-face architecture, which described AKOS as private and treated the public action face as the owner of all Actions execution.

GitHub currently exposes AKOS as a public repository. AKOS also already contained a bounded Finisher workflow. The governing text and live repository posture had drifted.

## Decision

Separate two execution classes:

1. **Governed cross-repository workload execution** remains exclusively owned by `GlacierEQ/public-actions-runner-host` and retains the private claim/approval/receipt lifecycle.
2. **Public repository-local verification** may run in the source repository only when it is read-only, secret-free, non-deploying, non-orchestrating, and does not create action-face claims or receipts.

No private-repository Actions exception was created.

## Security boundary

The AKOS local integrity workflow:

- requests only `contents: read`;
- disables persisted checkout credentials;
- receives no APEX, control-plane, deployment, or broad PAT credentials;
- compiles tracked Python files;
- runs adversarial repository-integrity tests;
- compares the checkout directly against the Git anchor;
- produces CI evidence only;
- performs no deployment, release, external publication, cross-repository orchestration, or private receipt write.

## Architecture update

`docs/architecture/PUBLIC_ACTION_FACE.md` now:

- records AKOS as public;
- preserves the public action face as the sole governed cross-repository execution owner;
- defines the narrow repository-local verification exception;
- treats credential persistence, broader permissions, cross-repository execution, bridge credentials, claims, receipts, deployment, or private-detail publication as release-blocking violations.

## Truth boundary

This amendment does not claim that public action-face canary activation has passed. Repository-local CI success does not substitute for `action-face-canary` or `apex-verification` evidence.

## Receipt target

The amendment and integrity repair are complete only when:

1. the PR head passes the AKOS Integrity Gate;
2. all material review findings are resolved;
3. the repair is integrated into `main`;
4. the post-merge `main` integrity run passes.
