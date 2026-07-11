# AKOS Runtime Changelog

All notable runtime changes are recorded here. Validation claims remain pending until directly observed in GitHub Actions or a reproducible local run.

## 0.3.0-rc.1 — 2026-07-11

### Added

- Strict TypeScript runtime package for Node.js 20+
- Canonical AKOS object, verification, source-class, pillar, and lifecycle contracts
- Secret-pattern detection with fingerprint-only quarantine output
- Deterministic Unicode/text normalization, SHA-256 identity, and idempotency keys
- Immutable source-pointer requirements for repository and primary-record promotion
- Case, evidence, architecture, task, and quarantine routing
- Atomic contradiction-edge generation
- Deterministic evidence-manifest roots
- Human-readable Markdown and machine-readable JSON artifact twins
- Court-facing verified-record guard
- HTTP health, piston-registry, and execution endpoints
- Nine trust-pipeline and HTTP integration tests
- Multi-stage non-root Docker image with health check
- GitHub Actions validation, container build, and container smoke test

### Corrected before review

- Production start path now matches TypeScript output at `dist/src/index.js`
- A mutable `github:` pointer can no longer self-promote to `verified_record`
- Secret scanning covers title, content, and source pointer rather than body content alone

### Explicitly not included

- Live GitHub, Supabase, Notion, or memory writes
- Credential lifecycle management
- Production deployment
- Automatic merge into `main`

### Validation status

`pending_ci_and_review` — this changelog records implementation scope, not a successful test claim.
