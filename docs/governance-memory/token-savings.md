# AKOS Token Savings Doctrine

Status: Active Draft
Version: 0.1.0
Created: 2026-07-07

## Purpose

This document defines how AKOS reduces token waste without weakening quality.

## Core Rule

Token savings should come from structure, not from omitting necessary truth.

## Primary Savings Methods

### 1. Storage-Time Structuring

Capture object identity, source, status, relationships, and next action when memory is created.

Structured capture prevents expensive reconstruction later.

### 2. Template Reuse

Use templates for recurring work instead of reasoning from scratch every time.

Examples:

- lane entries
- repo manifests
- connector records
- Pro-Code reviews
- handoff records

### 3. Context Tiering

Separate context into tiers:

- Hot: current task
- Warm: active project
- Cold: historical reference
- Frozen: canonical or archival truth

### 4. Selective Retrieval

Retrieve only the layer needed for the task.

Do not load entire history when a current-state file and ledger entry are enough.

### 5. Compiled Procedures

When a workflow proves itself, compile it into a short recipe.

The model should execute the recipe and only reason deeply around exceptions.

## Quality Constraint

Compression must preserve:

- identity
- source
- status
- confidence
- unresolved conflicts
- next action

## Machine Summary

```json
{
  "document": "token-savings",
  "version": "0.1.0",
  "methods": ["storage_time_structuring", "template_reuse", "context_tiering", "selective_retrieval", "compiled_procedures"],
  "quality_constraint": ["identity", "source", "status", "confidence", "conflicts", "next_action"]
}
```
