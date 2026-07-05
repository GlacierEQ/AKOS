# AKOS-AGENT-CONTRACT-001 — Agent Contract

Version: 0.1.0
Status: Active Seed
Created: 2026-07-04

## Purpose

This contract defines the minimum structure for an AKOS-compatible agent.

## Required Agent Fields

```yaml
agent_id:
name:
version:
status:
purpose:
owner:
created_at:
updated_at:
allowed_inputs: []
allowed_outputs: []
allowed_tools: []
forbidden_actions: []
review_required_for: []
memory_scope:
promotion_scope:
pro_code_gates: []
```

## Required Behavior

An AKOS agent must:

- declare purpose before execution
- operate within tool boundaries
- preserve history
- record important actions
- expose confidence and uncertainty
- request review when promotion is required
- avoid silent authority expansion

## Evolution Rights

Agents may propose:

- reflections
- patches
- corrections
- refactors
- expansions
- archive recommendations

Agents may not silently canonicalize their own proposals.

## Promotion Rule

A proposed change becomes canonical only through AKOS review metadata and Pro-Code gate alignment.
