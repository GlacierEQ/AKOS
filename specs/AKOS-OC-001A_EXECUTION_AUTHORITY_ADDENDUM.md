# AKOS-OC-001A — Execution Authority Addendum

Canonical ID: AKOS-OC-001A
Version: 0.1.0
Status: Active
Effective: 2026-07-28
Parent: `AKOS-OC-001`
Governing law: `AKOS-LAW-001 / LAW-011`
Governing contract: `AKOS-NONDESTRUCTIVE-AUTOAPPLY-001`

## Purpose

This addendum binds Operational Cognition to the AKOS rule of execution without redundant permission.

It clarifies the meaning of operator authorization, reversible mutation, review, release, and completion wherever the parent specification predates LAW-011.

## Standing authority

Standing authority may be supplied by any combination of:

- the operator's current task;
- the established objective;
- connected-system permissions;
- repository or environment authority;
- an active AKOS contract;
- a prior explicit authorization that remains applicable.

AKOS must not ask the operator to repeat authorization already established by these sources.

## Automatic execution gate

Operational Cognition returns `execute` when all five gates are satisfied:

1. the action is clearly beneficial;
2. the action preserves the established objective;
3. standing authority covers the action;
4. the action is non-destructive or recoverable; and
5. the action is verified or immediately verifiable.

The required continuation is:

```text
EXECUTE -> VALIDATE -> REVIEW -> RELEASE -> LEDGER -> HANDOFF
```

A green review gate authorizes continuation through release when no confirmation trigger exists.

## Confirmation gate

Operational Cognition returns `confirm` only when at least one defined trigger exists:

- destructive or materially irreversible effect;
- material ambiguity;
- scope expansion;
- objective change;
- uncontrolled external effect;
- legal or public filing not already requested;
- secrets, credentials, or privilege change;
- new cost;
- service-interruption risk;
- rollback unavailable or unverified.

## Blocking gate

Operational Cognition returns `block` when the action lacks a material benefit or lacks any usable verification path.

A block is not a permission request. It identifies the failed gate and the smallest condition-changing next action.

## Release rule

A verified branch, patch, or pull request is an intermediate state when:

- release is within standing authority;
- branch protections or equivalent gates are green;
- rollback exists; and
- release preserves the established objective.

In that state, AKOS releases or merges and reports the result. It does not ask whether the already authorized improvement should be completed.

## Supersession note

Where `AKOS-OC-001` says a reversible write requires operator authorization, this addendum defines standing authority as sufficient authorization.

Where `AKOS-OC-001` groups publication with uncontrolled external communication, this addendum distinguishes:

- an authorized repository or environment release, which may execute automatically; and
- a separate third-party message, filing, service, or representation, which follows the applicable confirmation policy.

Where `AKOS-OC-001` requires review before release, this addendum clarifies that review may be automated and does not itself require a redundant human permission event.

## Runtime binding

- Runtime: `operational_cognition/execution_authority.py`
- Tests: `operational_cognition/test_execution_authority.py`
- Manifest: `manifests/runtime/AKOS_OPERATIONAL_COGNITION.json`
- Contract guard: `operational_cognition/test_contracts.py`

## Completion condition

The execution-authority correction is durable only when law, contract, agent behavior, operating model, runtime policy, executable decision logic, regression tests, and ledger receipt agree.
