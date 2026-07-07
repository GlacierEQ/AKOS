# AKOS Memory Layers

Status: Active Draft
Version: 0.1.0
Created: 2026-07-07

## Purpose

This document defines the primary memory layers for AKOS.

## Layer 1 — Episodic Memory

Episodic memory stores raw events, session history, audit trails, and temporal records.

Properties:

- append-oriented
- time-stamped
- source-aware
- useful for recovery and provenance

Best use:

- session logs
- ledger entries
- evidence intake
- operational deltas

## Layer 2 — Semantic Memory

Semantic memory stores interpreted meaning, patterns, relationships, summaries, and reusable knowledge.

Properties:

- relationship-rich
- compressible
- retrievable by meaning
- useful for reasoning and context reconstruction

Best use:

- object summaries
- architecture patterns
- canonical rules
- relationship graph entries

## Layer 3 — State Memory

State memory stores the current operating condition.

Properties:

- mutable
- current
- low-latency
- must be clearly separated from historical truth

Best use:

- current task state
- active priorities
- latest connector status
- open blockers

## Layer Rule

Do not confuse current state with permanent truth.

State can change quickly. Canon requires review.

## AKOS Mapping

| Memory Layer | AKOS Surface |
|---|---|
| Episodic | ledger, session logs, lane deltas |
| Semantic | specs, doctrine, object model, graph relationships |
| State | CURRENT_STATE.md, ClickUp task state, active dashboards |

## Machine Summary

```json
{
  "document": "memory-layers",
  "version": "0.1.0",
  "layers": ["episodic", "semantic", "state"],
  "rule": "do not confuse current state with permanent truth"
}
```
