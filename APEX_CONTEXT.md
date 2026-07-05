# APEX Engineering Context

## Architecture — Double Helix

Every APEX system follows the Double Helix pattern:

```
Alpha  —  Pure computation. Physics models. Math. Stateless.
           No side effects. No I/O. Just truth.

Omega  —  Control layer. Orchestration. Stateful.
           Manages Alpha outputs. Closes the loop.
```

Alpha and Omega are strands. Each works alone.
Together they form a helix. That's the architecture.

## Mastermind

Mastermind is a **cognitive sidecar**. Not a Docker app.
Not a microservice. Not a daemon in the traditional sense.
It runs alongside the primary system and coordinates
cross-domain health, state, and decision signals.

Think corpus callosum, not Kubernetes pod.

## Code Engineering Standards

- **Zero external dependencies** where possible — stdlib only
- **Pure Python math** — no numpy for things numpy doesn't need to do
- **Stateless Alpha models** — same input always produces same output
- **No teacher voice** — comments are for engineers, not students
- **Humanized, elite, professional** — reads like a human wrote it
  because a human did write it
- **Easter eggs throughout** — see `EASTER_EGGS.md`

## The Radiation Bug Rule

The original `predictive_thermal.py` had a dead radiation term —
`q_radiATION` with a capitalization typo making it unreachable.
This is the canonical example of what we fix:
not just obvious bugs, but the quiet ones that nobody notices
because they don't know the physics well enough to check.

Always include all physics terms. Radiation matters at Mach 25.

## Session Bootstrap

When starting a new session, read:
1. `IDENTITY.md` — who, what, why
2. This file — how
3. `EASTER_EGGS.md` — the vocabulary
4. `REPOS.md` — current status of all APEX repos

Then proceed as if you've been here the whole time.
Because now you have.
