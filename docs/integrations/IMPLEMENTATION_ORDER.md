# AKOS Integration Implementation Order

Status: Active Draft
Version: 0.1.0
Created: 2026-07-04

## Purpose

This file records the approved connector sequence for AKOS.

The goal is to prevent tool sprawl. Each connected system must serve a clear role before automation expands.

## Approved Order

1. ClickUp
2. Supabase
3. Make
4. GitHub

## Role Summary

ClickUp is for execution visibility.

Supabase is for structured records.

Make is for controlled automation.

GitHub is for canonical architecture and version history.

## Quality Rule

A connector is not a source of truth by default.

A connector becomes useful only when it preserves AKOS identity, status, ownership, and review context.

## Entry Criteria

Before a connector is expanded, AKOS should define:

- what object types it will carry
- what fields it must preserve
- what system owns the canonical record
- how review state is shown
- how stale records are detected

## Output Criteria

A connector implementation is complete only when it has:

- a clear role
- a field map
- a review path
- a handoff rule
- a drift check

## Current Decision

Build ClickUp first, then Supabase, then Make, then GitHub integration refinements.
