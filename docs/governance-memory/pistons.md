# AKOS Pillar Pistons

Status: Active Draft
Version: 0.1.0
Created: 2026-07-07

## Purpose

This document defines the piston systems that move each governance pillar.

A pillar is structural. A piston is the repeatable cycle that makes the pillar work.

## Piston 1 — Governance Control Piston

Supports:

Automated Governance

Cycle:

```text
Receive request
Check identity
Check authority
Check boundary
Check budget or limit
Allow, reject, or escalate
Record result
```

## Piston 2 — Quality Gate Piston

Supports:

Quality Assurance

Cycle:

```text
Receive artifact
Check required metadata
Run Pro-Code gates
Record issues
Approve, revise, or reject
Record result
```

## Piston 3 — Observability Piston

Supports:

Monitoring and Observability

Cycle:

```text
Read current state
Compare to expected state
Detect drift
Flag stale or broken items
Route review
Record result
```

## Cross-Pillar Piston

When all pillars work together:

```text
Govern action
Validate output
Monitor drift
Update canon
```

## Rule

A piston must be simple enough to repeat and strict enough to prevent silent failure.

## Machine Summary

```json
{
  "document": "pistons",
  "version": "0.1.0",
  "pistons": ["governance_control", "quality_gate", "observability", "cross_pillar"],
  "rule": "simple enough to repeat and strict enough to prevent silent failure"
}
```
