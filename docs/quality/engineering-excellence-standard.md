# AKOS Engineering Excellence Standard

Status: Active Draft
Version: 0.1.0
Created: 2026-07-07

## Purpose

This standard defines what high-quality AKOS work means.

It applies to specs, schemas, templates, connectors, tasks, runtime actions, reviews, and ledger entries.

## Prime Rule

If it cannot be named, bounded, tested, observed, and recorded, it is not ready for operational use.

## Quality Bar

Every operational AKOS artifact should satisfy these requirements:

1. Clear identity
2. Clear owner or actor
3. Clear source
4. Clear boundary
5. Clear input
6. Clear output
7. Clear validation path
8. Clear failure path
9. Clear next action
10. Clear ledger location

## Readiness Levels

| Level | Meaning |
|---|---|
| Concept | Useful idea, not yet structured |
| Draft | Structured but not reviewed |
| Manual Ready | Can be executed manually with visible result |
| Manual Proven | Manual test passed |
| Automation Candidate | Manual path is proven and repeatable |
| Automation Ready | Rules, failure modes, and validation are complete |
| Operational | Used in live workflow with monitoring |
| Canonical | Accepted source of truth after review |

## Promotion Rule

Do not promote an artifact because it is useful once.

Promote only after repeatability, validation, and record discipline are shown.

## Failure Rule

Failure is acceptable.

Silent failure is not acceptable.

Every meaningful failure should produce:

- visible status
- reason
- source
- target
- attempted action
- next action

## Compression Rule

Short is allowed only when it remains traceable.

A compressed record must preserve identity, source, status, boundary, result, and next action.

## Machine Summary

```json
{
  "document": "engineering-excellence-standard",
  "version": "0.1.0",
  "prime_rule": "name, bound, test, observe, record",
  "readiness_levels": ["Concept", "Draft", "Manual Ready", "Manual Proven", "Automation Candidate", "Automation Ready", "Operational", "Canonical"]
}
```
