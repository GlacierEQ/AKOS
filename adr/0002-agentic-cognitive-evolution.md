# ADR-0002 — Agentic Cognitive Evolution Layer

Date: 2026-07-04
Status: Accepted

## Decision

AKOS will include an Agentic Cognitive Evolution layer governed by contracts, metadata, Pro-Code gates, and append-only records.

## Context

AKOS needs agents that can improve the system over time without becoming uncontrolled, unreviewable, or disconnected from canon.

## Decision Rule

Agents may propose evolution. AKOS governs promotion.

## Consequences

- Every agent requires a manifest.
- Every agent requires declared boundaries.
- Every evolution event should be recordable.
- Canonical promotion requires review metadata.

## First Agents

- Memory Curator
- Repository Steward
- Pro-Code Reviewer

## Pro-Code Check

- Naming: clear
- Architecture: bounded
- Failure Handling: authority limits declared
- Maintainability: simple seed structure
- Authenticity: matches AKOS purpose
- Observability: manifests and cycle templates expose state
- Documentation: decision lives in repo
