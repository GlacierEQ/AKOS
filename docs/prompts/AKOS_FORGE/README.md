# AKOS Forge Prompt System

AKOS Forge is the modular master prompt system for elite production engineering.

It raises every AKOS component to a reliable, production-ready standard by splitting the master prompt into small durable chunks.

## Modules

1. `01_IDENTITY.md` — elite engineering identity and quality bar
2. `02_ARCHITECTURE.md` — design, boundaries, interfaces, and failure modes
3. `03_BUILD.md` — implementation discipline and no-placeholder rules
4. `04_VALIDATION.md` — tests, verification, review, and delivery gates
5. `05_EVOLUTION.md` — maintenance, optimization, and continuous improvement
6. `MASTER_LOADER.md` — combined activation prompt

## Core Law

```text
Intent -> Interpret -> Architect -> Build -> Validate -> Ship -> Improve
```

## Production Standard

Do not generate demos, placeholders, or decorative scaffolding.

Create durable artifacts that a strong engineering team could maintain.

## Safety / Security Boundary

Do not store raw tokens, credentials, or secrets in prompts, docs, code, memory exports, or examples. Use `secret_ref` and fingerprint-only references.
