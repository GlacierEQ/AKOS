# ADR-0001 — AKOS Canonical Architecture Repository

Date: 2026-07-04
Status: Accepted

## Decision

`GlacierEQ/AKOS` is the canonical architecture repository for the Apex Knowledge Operating System.

## Context

Earlier AKOS scaffolding existed inside `GlacierEQ/mastermind`. That work remains useful as build history, but the dedicated AKOS repository is now the primary home for core architecture.

## Consequences

- Core AKOS specs live here.
- `mastermind` may mirror or reference AKOS, but should not silently diverge.
- Future AKOS-compatible repositories should reference this repo as the architecture source.

## Pro-Code Check

- Naming: clear
- Architecture: bounded
- Maintainability: acceptable
- Documentation: lives with decision
