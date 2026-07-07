# AKOS Automation Ecosystem

Status: Active Draft
Version: 0.1.0
Created: 2026-07-07

## Purpose

This document defines the AKOS approach to automations that generate or coordinate other automations.

## Core Idea

A manager automation should receive a goal, select a validated template, create bounded work units, and route execution through reviewable steps.

## Required Components

| Component | Role |
|---|---|
| Manager Automation | Receives goal and chooses path |
| Template Registry | Stores approved automation patterns |
| Generator | Creates bounded child automations or tasks |
| Executor | Runs the selected action path |
| Reviewer | Checks result against gates |
| Ledger | Records action, result, and drift |

## Quality Rule

Self-creating automation must not mean uncontrolled automation.

Every generated item needs:

- purpose
- boundary
- owner
- source
- status
- review path
- stop condition

## Template Rule

Templates are the main token savings engine.

A template converts repeated reasoning into reusable structure.

## Stop Condition

An automation should stop or escalate when:

- source is missing
- identity is unclear
- task boundary is unclear
- review path is missing
- result conflicts with canonical state

## AKOS Fit

This ecosystem should not be automated before connector identity and review gates are stable.

## Machine Summary

```json
{
  "document": "automation-ecosystem",
  "version": "0.1.0",
  "components": ["manager", "template_registry", "generator", "executor", "reviewer", "ledger"],
  "rule": "self-creating automation must remain bounded and reviewable"
}
```
