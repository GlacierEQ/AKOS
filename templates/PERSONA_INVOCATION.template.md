# Persona Invocation Template

Status: Template  
Spec: AKOS-PER-001  
Use: Invoke a persona as an AKOS-bounded worker.

---

## Invocation

```text
Invoke <PERSONA_ID> for <PURPOSE>.
```

## Purpose

```text
<What needs to be done. One concrete outcome.>
```

## Inputs

| Input | Source | Confidence | Notes |
|---|---|---|---|
| <input> | <source/path/url> | <low/medium/high> | <notes> |

## Constraints

| Constraint | AKOS Binding | Required Behavior |
|---|---|---|
| Purpose before persona | AKOS-LAW-001 | Do not let style override task |
| Provenance required | AKOS-LAW-001 | Identify source or label gap |
| Metadata before promotion | AKOS-META-001 | Do not promote untracked output |
| Pro-Code before canonical | AKOS-PROCODE-001 | Review before canon |

## Required Output

```text
<Artifact type: document, decision, source trace, matrix, timeline node, manifest, ledger entry, etc.>
```

## Proof Standard

```text
<verified record fact | source-supported inference | good-faith allegation | draft hypothesis | unverified memory>
```

## Runtime Tools

```text
<GitHub | Notion | Gmail | Drive | File Library | Web | Local Files | None>
```

## Refusal / Deferral Gate

The worker must refuse or defer promotion when:

- source is missing;
- confidence is unknown;
- requested output exceeds allowed scope;
- legal/factual claim lacks support;
- persona style conflicts with AKOS purpose;
- canonical source and mirror conflict;
- memory contradicts source evidence.

## Output Contract

Return:

1. Result
2. Source map
3. Confidence labels
4. Gaps
5. Next action
6. Ledger-ready summary
