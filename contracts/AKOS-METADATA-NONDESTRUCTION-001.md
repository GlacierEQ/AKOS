# AKOS Metadata Non-Destruction Contract — 001

Status: active
Scope: all CASEBRAIN and AKOS connector workflows

## Rule

Source metadata is evidence context and must not be silently rewritten, normalized in place, replaced, collapsed, or discarded.

AKOS preserves the originally observed metadata as an immutable source snapshot and records later interpretations, corrections, normalizations, and reconciliations as separate versioned overlays.

## Protected metadata

This contract covers, at minimum:

- original filename and extension;
- source path, namespace path, folder identity, and parent relationships;
- provider object ID, revision ID, version ID, and connector-native identifier;
- created, modified, uploaded, accessed, observed, and captured timestamps;
- timezone and timestamp precision;
- MIME type, byte size, checksums, and provider content hashes;
- owner, custodian, creator, modifier, sender, recipient, and account attribution;
- permissions, sharing state, labels, tags, comments, and retention state;
- EXIF, document properties, message headers, court-filing metadata, and embedded metadata;
- connector response metadata and acquisition context;
- source visibility, access limitations, pagination state, and extraction errors.

## Allowed automatic operations

AKOS may automatically:

- capture and hash metadata snapshots;
- add canonical IDs and crosswalks;
- create normalized search fields beside original values;
- append corrections, aliases, classifications, and confidence scores;
- link duplicate or conflicting metadata without merging it;
- record supersession and reconciliation relationships;
- generate derivative indexes, manifests, timelines, and receipts.

## Prohibited automatic operations

AKOS must not automatically:

- overwrite an original metadata value;
- replace source timestamps with normalized timestamps;
- rename source objects merely to enforce a naming convention;
- collapse competing object IDs, paths, people, dates, or case identifiers;
- delete metadata judged irrelevant or duplicative;
- remove permissions, labels, comments, or revision history;
- present an inferred or corrected value as the original value;
- conceal connector errors, missing fields, or precision loss.

## Overlay model

Each metadata observation must retain:

- `source_value`;
- `normalized_value`, when applicable;
- `interpretation`, when applicable;
- `source_pointer`;
- `observed_at_utc`;
- `connector_id` and connector-native object ID;
- `content_hash` or metadata-snapshot hash;
- `verification_status`;
- `confidence`;
- `supersedes` or `conflicts_with` relationship when applicable;
- append-only receipt ID.

Corrections do not erase the prior value. They create a new metadata assertion linked to the earlier assertion.

## Destructive gate

Any action that changes source metadata in Drive, Dropbox, GitHub, Supabase, Notion, ClickUp, or another connected system—including rename, timestamp rewrite, permission change, label removal, parent change, metadata overwrite, or revision deletion—requires explicit user approval and a reversible mutation plan.

## Forensic result

The system must always be able to reconstruct:

1. what the source reported originally;
2. when and how AKOS observed it;
3. every later normalization or correction;
4. who or what authorized any source-side change;
5. the receipts and hashes tying the chain together.
