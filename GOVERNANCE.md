# AKOS Governance

Status: Active Draft
Version: 0.1.0
Created: 2026-07-04

## Purpose

This file defines how AKOS architecture files are reviewed and promoted.

## Principle

Build in layers. Preserve history. Promote stable work. Mark older work historical when replaced.

## Status Values

- draft
- working
- working_canonical
- canonical
- historical
- archived

## Promotion Requirements

A file should not become canonical unless it has:

- clear name
- version
- status
- purpose
- owner or source
- review state
- relationship to the AKOS stack

## Pro-Code Gates

AKOS review uses seven gates:

- Naming
- Architecture
- Failure Handling
- Maintainability
- Authenticity
- Observability
- Documentation

## Source Rule

GitHub is the source for AKOS architecture files.

Other systems may mirror or summarize AKOS, but mirrors should point back to this repository.

## Review Rule

Prefer small, traceable commits.

Each important change should record what changed and why.
