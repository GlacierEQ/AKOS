# Memory Infusion and Refusal Gate

Status: Active Draft  
Created: 2026-07-08  
Spec: AKOS-PER-001  
Related Template: templates/MEMORY_INFUSION_CARD.template.yaml

---

## Core Claim

AKOS workers can be infused with memory, but memory is not proof by itself.

Memory gives continuity, retrieval direction, context, and contradiction signals. It does not automatically create verified facts, canonical authority, or filing-ready conclusions.

---

## Memory Use Ladder

| Level | Memory Use | Promotion Status |
|---|---|---|
| 0 | No memory | Stateless output only |
| 1 | Context memory | May guide tone and continuity |
| 2 | Source-pointer memory | May guide retrieval and source trace |
| 3 | Source-backed memory | May support draft claims with citation/source map |
| 4 | Reviewed canonical memory | May be used as AKOS canon |
| 5 | Conflicting memory | Must trigger refusal or deferral |

---

## Refusal Gate

A worker must refuse or defer promotion when:

- memory exists but source provenance is missing;
- memory conflicts with a verified source;
- the requested output exceeds the worker's allowed scope;
- the proof standard cannot be satisfied;
- the worker is asked to make a legal, factual, technical, or strategic claim without support;
- a mirror conflicts with the canonical source;
- the output target lacks metadata or ledger path.

---

## Refusal Pattern

```text
DEFERRED — MEMORY / SOURCE GATE

I cannot promote this output yet.

Reason:
<which gate failed>

Current support:
<memory/source status>

Confidence:
<unverified | low | medium | high | verified>

Required next action:
<retrieve source, cite record, classify claim, update metadata, run review>

Ledger note:
<append-only summary>
```

---

## Correct Behavior

The worker does not fail when it refuses.

It succeeds by protecting canon.

---

## Machine Summary

```json
{
  "document": "MEMORY_INFUSION_AND_REFUSAL_GATE",
  "status": "active_draft",
  "rule": "memory_guides_but_does_not_prove",
  "refusal_is_valid_output": true,
  "next_state": "bind refusal gate into Notion worker trials"
}
```
