# Notion Worker Trial Plan — Aionic Tree

Status: Active Draft  
Created: 2026-07-08  
Spec: AKOS-PER-001  
Family: FAM-AIONIC-TREE

---

## Purpose

Test the Aionic Tree personas as Notion-operable AKOS workers before promoting them into canonical runtime modules.

---

## Trial Rule

Each worker must produce a concrete artifact or a justified refusal.

A justified refusal is not failure. It is a correct AKOS behavior when memory, source, confidence, scope, or proof standard is missing.

---

## Worker Trial Set

| Worker | Test Task | Expected Output |
|---|---|---|
| Architect | Turn a rough project idea into AKOS object map | Architecture map |
| Engineer | Convert the map into build steps | Execution checklist |
| Iron Quill | Convert facts into precise text | Draft artifact |
| Phantom Core | Simulate consequences of a decision | Scenario matrix |
| Obsidian Loop | Attack a draft for weak claims | Contradiction matrix |
| Nexus Shift | Reroute a blocked workflow | Routing decision |
| Temporal Anchor | Build a dated event sequence | Timeline node set |
| Vortex Flux | Model chaotic inputs | Anomaly register |
| Data Wraith | Recover source provenance | Source trace |
| Dragon Hunter Circuit | Build response ladder | Tactical sequence |

---

## Notion Test Page Structure

Each worker page should contain:

```text
Worker
Purpose
Invocation
Inputs
Memory Binding
Output Target
Acceptance Test
Refusal Test
Result
Ledger Summary
```

---

## Memory Gate

Before output promotion, each worker checks:

1. Is source memory present?
2. Is the source canonical, mirror, draft, or unknown?
3. Does memory conflict with evidence?
4. Is confidence labeled?
5. Is the requested output allowed for this persona?
6. Is there a ledger target?

If any required gate fails, the worker returns:

```text
DEFERRED — MEMORY / SOURCE GATE
Reason:
Missing source:
Confidence:
Next retrieval action:
Ledger note:
```

---

## Trial Output Rule

All results should be copied back into AKOS as either:

```text
ledger/<date>_<worker>_trial.md
```

or, if promoted:

```text
manifests/agents/<agent>.yaml
```

---

## Next Actions

1. Create a Notion trial board/page.
2. Add ten worker task cards.
3. Run each worker against one real test input.
4. Save results as ledger entries.
5. Promote only workers that pass Pro-Code review.
