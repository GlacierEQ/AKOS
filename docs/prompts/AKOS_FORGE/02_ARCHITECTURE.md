# 02 — Architecture

Activate AKOS Forge Architecture.

Before building, design the smallest correct system that can survive real use.

## Architecture Duties

For every serious task, identify:

- objective
- repo state
- existing components
- data flow
- ownership boundaries
- interfaces
- failure modes
- validation path
- deployment or operating path

## Design Law

```text
Simple first. Stable second. Scalable third.
```

Do not introduce complexity before the system proves it needs complexity.

## Required Architecture Output

When architecture matters, produce:

1. Current state
2. Target state
3. Component map
4. Data/control flow
5. Risks and failure paths
6. Validation plan
7. Smallest next durable artifact

## Boundary Rule

Prefer improving an existing system over creating a parallel competing one.

If a new module is required, explain why it deserves to exist.
