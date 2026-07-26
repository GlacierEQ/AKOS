# Kimi Portable Memory Adapter

Connector ID: `CONN-KIMI-001`  
Status: Implemented local projection; live provider authentication not claimed  
Version: 0.1.0

## Role

This adapter imports Kimi memory or conversation exports into an AKOS-governed portable-memory projection. It is an edge connector, not a canonical truth source.

The source prototype contained simulated MemoryPlugin, GitHub, Overleaf, legal-generator, and dashboard integrations. AKOS retains only the reusable memory-portability concept. Hard-coded case data, fake connection states, demo credentials, unsupported performance claims, broken legal templates, and unverified third-party API endpoints are intentionally excluded.

## Supported input

- JSON array of records
- JSON object containing `memories`, `records`, `items`, `conversations`, or `data`
- newline-delimited JSON
- conversation records containing a `messages` array

Recognized text fields include `content`, `memory`, `text`, `body`, `summary`, and `message`.

## Guarantees

- deterministic `CBR-CONNECTOR_OBJECT-*` identity;
- SHA-256 content integrity;
- source object and source URI preservation;
- no automatic promotion above `unverified`;
- append-only local records and receipts;
- duplicate detection;
- drift visibility rather than silent overwrite;
- MemoryPlugin-compatible line rendering;
- standard-library-only execution.

## CLI

```bash
python -m operational_cognition.connectors.kimi_memory import \
  --input /path/to/kimi-export.json \
  --store /path/to/akos-memory-projection \
  --case-id GLOBAL \
  --owner operator
```

Dry run:

```bash
python -m operational_cognition.connectors.kimi_memory import \
  --input /path/to/kimi-export.json \
  --store /path/to/akos-memory-projection \
  --dry-run
```

Verify persisted content hashes:

```bash
python -m operational_cognition.connectors.kimi_memory verify \
  --store /path/to/akos-memory-projection
```

## Persistence layout

```text
<store>/
├── records.jsonl
├── receipts.jsonl
└── drift.jsonl
```

`drift.jsonl` is created only when a conflicting incoming record is detected. Drift requires review; the adapter does not overwrite either version.

## Verification

```bash
python -m compileall -q operational_cognition/connectors
python -m unittest -v operational_cognition.test_kimi_memory
```

## Capability truth

| Capability | State |
|---|---|
| Export parsing | VERIFIED locally |
| Normalization and deterministic identity | VERIFIED locally |
| JSONL persistence and receipts | VERIFIED locally |
| Hash verification | VERIFIED locally |
| MemoryPlugin line rendering | VERIFIED locally |
| Live Kimi API | UNASSESSED / not claimed |
| Live MemoryPlugin API | UNASSESSED / not claimed |
| CASEBRAIN provider persistence | Pending route binding and provider receipt |

## Promotion boundary

Imported records remain `unverified` connector objects. Human or governed machine review is required before any record is promoted into a canonical memory, claim, event, evidence item, or legal artifact.
