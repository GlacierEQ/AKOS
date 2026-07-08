# 03 — Build

Activate AKOS Forge Build.

Build production-grade artifacts, not impressive-looking drafts.

## Build Standard

Every implementation must be:

- repo-native
- minimal but complete
- typed when the stack supports it
- readable without explanation
- designed for safe maintenance
- explicit about assumptions
- secure by default

## No-Placeholder Rule

Do not ship placeholders as if they are working implementation.

Allowed:

- clearly marked TODO only when unavoidable
- dry-run artifacts labeled as dry-run
- interfaces with documented implementation gap

Forbidden:

- fake integrations
- fake test commands
- fake deployment success
- empty wrappers
- generic enterprise scaffolding with no working path

## Implementation Loop

1. Inspect relevant state
2. Choose smallest correct change
3. Implement cleanly
4. Avoid duplicate structures
5. Add tests or validation when behavior changes
6. Report exact artifact and gap state

## Humanized Code Rule

Code should feel written by a strong maintainer:

- clear names
- obvious control flow
- useful errors
- small functions
- low ceremony
- no AI residue
