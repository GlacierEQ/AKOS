# Notion Worker Task Template

Status: Template  
Spec: AKOS-PER-001  
Use: Create a Notion task/page for testing one AKOS persona worker.

---

## Worker

**Persona ID:** `<PERSONA_ID>`  
**Family:** `<FAMILY_ID>`  
**Status:** `test | active | blocked | complete | archived`

---

## Task

```text
<One concrete task.>
```

---

## Invocation

```text
Invoke <PERSONA_ID> for <PURPOSE>.
Inputs: <SOURCE SET>.
Constraints: <PILLARS / CONTRACTS>.
Required output: <ARTIFACT>.
Proof standard: <CONFIDENCE / VERIFICATION STATE>.
Log result to: <LEDGER / TARGET PATH>.
```

---

## Required Inputs

| Input | Location | Required? | Status |
|---|---|---:|---|
| <input> | <path/url/page> | yes | missing |

---

## Output Target

```text
<Notion page, GitHub path, document, matrix, ledger entry, etc.>
```

---

## Memory Binding

Use `templates/MEMORY_INFUSION_CARD.template.yaml`.

Minimum memory fields:

- source layer;
- confidence;
- allowed use;
- forbidden use;
- refusal gate;
- ledger target.

---

## Acceptance Test

The worker passes only if it returns:

- concrete artifact;
- source map;
- confidence labels;
- gaps;
- next action;
- ledger-ready summary.

---

## Refusal Test

The worker must refuse or defer promotion if:

- source is missing;
- memory conflicts with source;
- requested output exceeds persona scope;
- proof standard cannot be met;
- canonical promotion is requested before review.
