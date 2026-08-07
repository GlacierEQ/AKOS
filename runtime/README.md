# AKOS Runtime Core v0.3.0

The runtime is the executable trust pipeline beneath the AKOS governance repository. It converts raw inputs into deterministic AKOS objects while preserving provenance, verification status, quarantine boundaries, hashes, and review state.

## Boundary

The repository root remains the canonical architecture and governance layer. `runtime/` is an implementation layer governed by those contracts.

The runtime does **not** decide that a claim is true merely because a caller labels it verified. Promotion requires an eligible source class and an immutable source pointer.

## Active Pistons

| Piston | Responsibility |
|---|---|
| M2 | Secret detection, redaction, and quarantine |
| M3 | Unicode/text normalization and deterministic identity |
| M4 | Verification classification and provenance gates |
| M6 | Atomic contradiction-edge generation |
| M7 | Deterministic evidence-manifest roots |
| M8 | Markdown/JSON artifact twins with court-facing guard |
| M11 | Health surface and structured runtime status |

## Requirements

- Node.js 20 or newer
- npm 10 or newer recommended

## Local Validation

```bash
cd runtime
npm install
npm run ci
```

`npm run ci` executes strict type checking, the Node-native integration suite, and the production build.

## Start

```bash
npm start
```

Development mode:

```bash
npm run dev
```

Default port: `8787`

## HTTP API

### `GET /health`

Returns runtime identity, version, and active-piston count.

### `GET /pistons`

Returns the executable piston registry.

### `POST /execute`

Accepts a pipeline input and returns:

- canonical AKOS object
- deterministic evidence-manifest root
- Markdown/JSON artifact twin when permitted

Maximum request body: 1 MiB.

## Input Contract

```json
{
  "title": "Committed source",
  "content": "Repository-backed content",
  "sourcePointer": "github:GlacierEQ/AKOS@0123456789abcdef0123456789abcdef01234567:runtime/src/index.ts",
  "sourceClass": "authenticated_repository",
  "verificationStatus": "verified_record",
  "objectType": "system_architecture",
  "actors": ["GlacierEQ"],
  "tags": ["runtime"],
  "courtFacing": false
}
```

### Immutable source-pointer formats

Authenticated repository object:

```text
github:<owner>/<repo>@<40-character-commit-sha>:<path>
```

Primary record object:

```text
court:<case-or-record-pointer>#sha256:<64-character-sha256>
evidence:<evidence-pointer>#sha256:<64-character-sha256>
sha256:<64-character-sha256>
```

A mutable branch pointer such as `github:GlacierEQ/AKOS:main/...` cannot promote itself to `verified_record`.

## Dispositions

| Disposition | Meaning |
|---|---|
| `PROMOTE` | Source and verification gates passed |
| `MANUAL_REVIEW` | Classified but not eligible for canonical promotion |
| `QUARANTINE` | Secret-bearing or unsafe input isolated |
| `DEDUPLICATE` | Reserved for storage-layer duplicate reconciliation |
| `READ_ONLY_ALIAS` | Reserved for legacy-source preservation |

## Court-Facing Safety

When `courtFacing` is `true`, artifact generation requires `verificationStatus: verified_record`. User assertions, inferences, draft strategy, and unresolved material remain reviewable objects but cannot generate court-facing artifact twins.

## Docker

```bash
docker build -t akos-runtime:0.3.0 .
docker run --rm -p 8787:8787 akos-runtime:0.3.0
```

## Current Scope

This release candidate provides the deterministic local runtime and validation boundary. External GitHub, Supabase, Notion, and memory connectors remain separate adapters and must not be reported as live until configured and directly observed.
