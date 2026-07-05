# ClickUp Role and Boundary

Status: Active Draft
Version: 0.1.0
Created: 2026-07-04

## Role

ClickUp provides execution visibility for AKOS.

It answers:

- What needs to be done?
- What is being worked on?
- What is blocked?
- What is ready for review?
- What is complete?

## Boundary

ClickUp does not own canonical architecture.

ClickUp should not replace GitHub specs, contracts, manifests, templates, or governance files.

## Ownership Split

| System | Owns |
|---|---|
| GitHub | AKOS architecture and versioned files |
| ClickUp | task state and work visibility |
| Notion | dashboards and navigation |
| Supabase | structured records after schema approval |
| Make | controlled automation after object mapping |

## Quality Rule

A ClickUp task is valid when it has enough context for a future operator to understand where it came from and what outcome it needs.

## First Use

Use ClickUp for AKOS open loops before using it for broad automation.
