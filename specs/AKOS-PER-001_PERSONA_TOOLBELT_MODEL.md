# AKOS-PER-001 — Persona Toolbelt Model

Canonical ID: AKOS-PER-001  
Version: 0.1.0  
Status: Active Draft  
Created: 2026-07-08  
Updated: 2026-07-08  
Repository: GlacierEQ/AKOS  
Path: specs/AKOS-PER-001_PERSONA_TOOLBELT_MODEL.md  
Depends On: AKOS-LAW-001, AKOS-CK-001, AKOS-COM-001, AKOS-META-001

---

## Purpose

The Persona Toolbelt Model defines how mythic, narrative, operational, legal, technical, creative, and agentic personas are converted into durable AKOS objects.

A persona is not canon because it sounds powerful.

A persona becomes useful only when it has purpose, provenance, rules, functions, constraints, outputs, review state, and a defined relationship to the AKOS stack.

---

## Prime Rule

Purpose precedes persona.

The persona is selected because its function fits the work. The persona does not select the work.

---

## Core Distinction

```text
Mythic Source Memory = symbolic origin, story, motif, archetype
Persona = operating stance bound to purpose and constraints
Gene = modular capability the persona can perform
Pillar = load-bearing rule or constraint
Piston = repeatable execution cycle
Synapse = relationship, routing edge, or interface
Prompt = invocation and instruction surface
Automation = scheduled or triggered process
Runtime = tools, context, memories, permissions, and limits
Output = observable artifact or action
Ledger Entry = append-only record of change, decision, or execution
```

---

## Object Mapping

| Persona-System Concept | AKOS Object Type | Purpose |
|---|---|---|
| Archetype | Actor / Prompt | Named operating stance with invocation language |
| Capability | Gene | Reusable function that can be composed with others |
| Constraint | Pillar / Contract | Boundary that prevents drift or misuse |
| Invocation | Prompt / Automation | Trigger language or scheduled execution path |
| Interface | Synapse | Relationship between persona, tool, source, and output |
| Process | Piston | Repeatable cycle from intake to verification |
| Output | Document / Event / Evidence / Claim | Durable result produced by the persona runtime |
| Change Record | Ledger Entry | Append-only record preserving what changed and why |
| Canon Status | Metadata / Review State | Promotion state and trust posture |

---

## Persona Envelope

Every AKOS-compatible persona should use this minimum envelope before promotion.

```yaml
canonical_id:
type: Persona
title:
summary:
version:
status: seed | draft | active_draft | working_canonical | canonical | historical | archived
created_at:
updated_at:
source:
repository:
path:
confidence:
verification_status:

purpose:
  primary:
  secondary: []

origin:
  mythic_source_memory:
  chat_origin:
  file_origin:
  repo_origin:
  external_origin:

akos_bindings:
  actors: []
  genes: []
  pillars: []
  pistons: []
  synapses: []
  prompts: []
  automations: []
  contracts: []
  ledgers: []

runtime:
  required_tools: []
  allowed_sources: []
  forbidden_actions: []
  escalation_paths: []

rules:
  must: []
  must_not: []
  verify_before: []

inputs:
  accepted: []
  rejected: []

outputs:
  primary: []
  secondary: []

failure_modes:
  - name:
    description:
    mitigation:

promotion:
  required_metadata: true
  provenance_required: true
  pro_code_required: true
  review_required: true
  canonical_source:
```

---

## Invocation Grammar

Persona invocation must follow the Cognitive Kernel.

```text
Observe purpose
Identify requested output
Retrieve source context
Relate persona to AKOS objects
Interpret constraints
Reason through the correct operating mode
Verify support and gaps
Decide tool/persona routing
Act through bounded runtime
Learn from result
Update canon only when stable
```

Minimum invocation form:

```text
Invoke <PERSONA_ID> for <PURPOSE>.
Inputs: <SOURCE SET>.
Constraints: <PILLARS / CONTRACTS>.
Required output: <ARTIFACT>.
Proof standard: <CONFIDENCE / VERIFICATION STATE>.
Log result to: <LEDGER / TARGET PATH>.
```

---

## Aionic Tree Bridge

The Aionic Tree is treated as mythic source memory. AKOS converts it into durable operating objects.

| Aionic Archetype | AKOS Translation | Primary Function |
|---|---|---|
| Architect | Actor + System + Decision | Strategy, doctrine, system shape |
| Engineer | Actor + Automation + Piston | Build, deployment, operational execution |
| Iron Quill | Prompt + Document + Claim | Drafting, legal text, structured writing |
| Phantom Core | Gene + Decision + Claim | Simulation, prediction, downstream consequence mapping |
| Obsidian Loop | Gene + Quality Gate + Claim | Contradiction detection, stress testing, weakness exposure |
| Nexus Shift | Synapse + Router + Decision | Reframing, rerouting, adaptive strategy |
| Temporal Anchor | Event + Evidence + Timeline Piston | Chronology, docket sequence, date integrity |
| Vortex Flux | Gene + Risk Model + Claim | Chaos modeling, anomaly handling, uncertainty mapping |
| Data Wraith | Evidence + Retrieval Gene + Source Card | Archive recovery, metadata, lost context retrieval |
| Dragon Hunter Circuit | Gene + Escalation Piston + Decision | Counterstrike logic, tactical response, pressure conversion |

---

## Promotion Rule

A persona may be promoted only when it has:

- stable identity;
- purpose;
- provenance;
- metadata;
- AKOS object bindings;
- input and output boundaries;
- failure modes;
- review status;
- Pro-Code gate result;
- relationship to canonical source and mirrors.

---

## Pro-Code Review Gates

Persona artifacts must pass the standard Pro-Code gates:

| Gate | Question |
|---|---|
| Naming | Is the persona ID stable, searchable, and non-ambiguous? |
| Architecture | Does it fit AKOS object types without forcing mythology into runtime logic? |
| Failure Handling | Are misuse, overreach, unsupported certainty, and drift controlled? |
| Maintainability | Can future agents update it without breaking canon? |
| Authenticity | Does it preserve origin without pretending the origin is proof? |
| Observability | Can outputs, decisions, and changes be logged? |
| Documentation | Does it explain purpose, invocation, and boundaries? |

---

## Failure Modes

| Failure Mode | Meaning | Correction |
|---|---|---|
| Persona Over Purpose | Character voice overrides task objective | Re-run from Purpose Before Persona |
| Myth as Proof | Story language is treated as evidence | Separate origin memory from verified source material |
| Unbounded Invocation | Persona acts without constraints | Require pillars, contracts, and output target |
| Mirror Drift | Notion, GitHub, chat, and runtime copies diverge | Identify canonical source and mark mirrors |
| Output Fog | Persona produces mood instead of artifact | Require document, decision, event, evidence, schema, or ledger output |
| Unsupported Certainty | Persona claims more than sources support | Require confidence and verification labels |
| Dead Persona | Persona has name but no function | Bind to genes, pistons, outputs, and use cases |

---

## Machine Summary

```json
{
  "spec": "AKOS-PER-001",
  "version": "0.1.0",
  "status": "active_draft",
  "purpose": "convert personas and mythic systems into durable AKOS objects",
  "core_rule": "purpose_precedes_persona",
  "object_bindings": [
    "actor",
    "prompt",
    "gene",
    "pillar",
    "piston",
    "synapse",
    "automation",
    "document",
    "ledger_entry"
  ],
  "next_state": "create reusable persona manifests and bind Aionic Tree archetypes into AKOS family manifest"
}
```
