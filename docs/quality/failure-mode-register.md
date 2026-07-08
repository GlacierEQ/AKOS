# AKOS Failure Mode Register

Status: Active Draft
Version: 0.1.0
Created: 2026-07-07

## Purpose

This register defines known AKOS failure modes and required handling paths.

## Rule

A known failure mode without a handling path is an unresolved risk.

## Failure Modes

| ID | Failure Mode | Risk | Handling Path |
|---|---|---|---|
| FM-001 | Missing source | Work cannot be traced | Block action until source is added |
| FM-002 | Unclear boundary | Tool may exceed authority | Require boundary statement |
| FM-003 | False readiness | System claims more than proven | Downgrade readiness and record limitation |
| FM-004 | Orphan task | Task cannot be tied to AKOS object | Add source or archive as non-AKOS |
| FM-005 | Duplicate task | Work fragments across records | Link duplicates and choose primary source |
| FM-006 | Stale state | Task or state no longer matches source | Mark review needed |
| FM-007 | Missing validation | Action occurred but result is unproven | Add validation step before promotion |
| FM-008 | Silent connector failure | Tool action fails without visible status | Create ledger note and retry only with boundary |
| FM-009 | Canon drift | Mirror diverges from GitHub source | Compare source and mirror, then record decision |
| FM-010 | Automation overreach | Automation acts beyond approved scope | Stop automation and route review |

## Required Failure Record

When a failure occurs, record:

- failure ID
- date
- artifact
- source
- target
- actor
- what happened
- immediate status
- next action

## Severity Levels

| Severity | Meaning |
|---|---|
| Low | Does not block work |
| Medium | Blocks promotion |
| High | Blocks operational use |
| Critical | Blocks automation and requires review |

## Machine Summary

```json
{
  "document": "failure-mode-register",
  "version": "0.1.0",
  "failure_modes": 10,
  "rule": "known failure modes require handling paths"
}
```
