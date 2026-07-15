# CASEBRAIN repair promotion — 2026-07-15

Status: source repairs merged; runtime activation remains gate-controlled.

## Merged repair receipts

| Repository | Pull request | Main commit | Verified repair |
|---|---:|---|---|
| GlacierEQ/AKOS | #1 | `538942cd196ae1f0fd04b3de09b5eb4f3ced2693` | federation contract, schema, registry and human gates |
| GlacierEQ/AEON-777 | #51 | `b176d0b66358f5e59d0bd37f167160828be3dad6` | source-linked CASEBRAIN schemas, claim classes and human-action gates |
| GlacierEQ/token_saver | #1 | `9700e8205455ca912edc6e7333eabd48c19fb0a0` | full SHA-256 pointers, verified resolution and measured accounting |
| GlacierEQ/apex-bootup-core | #1 | `139380144087f8df79c53a92e109d60dd0a2527f` | dry-run default, explicit allowlist, rollback and signal cleanup |
| GlacierEQ/pro-code | #3 | `0379564b33f6b5ec8f32cdad23fb599216e6cbbc` | typed fail-closed worker dispatch and explicit runtime acknowledgements |
| GlacierEQ/aspen-grove-supabase | #1 | `f3a10759a4f754335bc600934b7204233c1afe97` | case-scoped RLS, provenance, append-only audit and secured functions |
| GlacierEQ/make-it-heavy | #1 | `49c7868f323155012a13194fa305260308a05b7e` | role-bound read-only workers, explicit tool registry and bounded timeouts |

## Promotion boundary

Merging source code does not prove a deployed runtime. Runtime-facing lanes remain blocked until their gates produce dated receipts.

- AEON/CASEBRAIN: rotate the exposed historical memory-service credential, repair project discovery/indexing, then complete one audited write/recall loop.
- Aspen Supabase: rotate the exposed historical Mem0 credential, rehearse migration on staging, provision the first owner, remediate legacy provenance gaps, run the live catalog verifier, and configure function secrets.
- Pro-Code: configure a trusted signer and verify Nexus-side signature, case isolation, idempotency and approval receipt enforcement.
- Make-It-Heavy: provide the operator API key and run a bounded, read-only live smoke test.
- APEX Bootup: audit any host-specific script before explicitly selecting it for execution.
- Token Saver: configure allowed roots and measure savings on the actual workload.

No filing, service, court contact, evidence release, publication, external escalation, deadline confirmation, fact promotion, production write or connector activation is authorized by this ledger.
