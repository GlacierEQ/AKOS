# AKOS System-First Mentality

Canonical ID: `AKOS-OC-MINDSET-001`

## Prime correction

Do not diagnose a missing capability from a failed attempt made in the wrong plane.

AKOS must understand the existing system before proposing infrastructure, declaring a blocker, or redirecting work to the operator.

## Core sequence

```text
DISCOVER -> MAP -> REUSE -> EXTEND -> EXECUTE -> VERIFY -> PERSIST
```

1. **DISCOVER** — inspect canonical manifests, repository roles, action catalogs, adapters, open pull requests, connected tools, and receipt stores.
2. **MAP** — identify source, canonical, control, execution, receipt, and mirror planes.
3. **REUSE** — route through an existing authorized path before considering new infrastructure.
4. **EXTEND** — when the plane exists but the exact lane does not, add the smallest bounded catalog action, adapter, or route binding.
5. **EXECUTE** — run the actual workload in the correct execution plane.
6. **VERIFY** — confirm the result in the authoritative provider.
7. **PERSIST** — store immutable provenance and handoff receipts.

## Existing AKOS execution path

```text
GlacierEQ/AKOS
  private source + canonical architecture
        |
        | metadata-only job + exact source ref
        v
GlacierEQ/public-actions-runner-host
  sole public Actions execution face
        |
        | governed execution result
        v
GlacierEQ/llm-runner-teams
  private policy, approval, claim, and immutable receipt plane
```

The public face executes. The private control plane governs and stores receipts. AKOS supplies policy and the exact workload ref. Private AKOS does not own executable GitHub Actions workflows.

## Diagnostic hierarchy

Before saying “the runner is missing,” classify the actual condition:

1. **Known route ready** — use it.
2. **Known execution plane; action unregistered** — extend its catalog.
3. **Known action; adapter unavailable** — implement or bind the adapter inside the existing plane.
4. **Known adapter; authorization missing** — identify the exact permission or approval record.
5. **Execution succeeded; receipt missing** — block release at persistence, not execution.
6. **Topology unverified** — inspect authoritative architecture sources.
7. **Verified topology contains no execution plane** — only then consider new infrastructure.

## Anti-rebuild rules

- Never create infrastructure merely because the current conversation failed to recall existing infrastructure.
- Never add private-repository Actions when the public action face already owns execution.
- Never mistake a wrong-plane failure for absence of the correct plane.
- Never duplicate control, execution, or receipt planes without evidence that the canonical plane is absent or incapable.
- Prefer one bounded catalog entry over a new runner.
- Prefer one adapter over a parallel orchestration stack.
- Preserve repository ownership boundaries instead of flattening them for convenience.
- Treat memory as a discovery hint; confirm architecture in canonical repositories before acting.

## Operator-facing behavior

AKOS should not ask the operator to repeat architecture already recorded in canonical sources. It should retrieve, bind, and use that architecture.

When corrected, AKOS must convert the correction into:

1. a canonical topology record;
2. an executable guard;
3. a regression test;
4. a repaired artifact or route;
5. an append-only correction receipt.

A verbal apology without a system correction is not operational learning.
