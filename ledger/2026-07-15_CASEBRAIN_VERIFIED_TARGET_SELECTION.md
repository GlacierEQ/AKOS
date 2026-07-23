# CASEBRAIN Verified Target Selection — 2026-07-15

Mode: read-only inspection; no evidence mutation; no Supabase migration applied.

## Supabase

Primary governed migration target: `supabase-backend-ops` (`dyhprklicgewmrimecey`).

Basis:
- previously designated primary operational truth;
- contains connector registry, memory cards, sync runs, events, cursors, dedupe, jobs, case/document/entity structures;
- all inspected public tables report RLS enabled.

Pre-deployment security repairs required:
- lock mutable function search paths;
- revoke unintended anon/authenticated execution of SECURITY DEFINER RPCs;
- shorten email OTP expiry;
- upgrade Postgres security patch level.

Secondary read-only source: `supabase-glaciereq` (`kjebemdgvjvuutzvhbtp`).

Quarantine basis for new canonical writes:
- three SECURITY DEFINER legal views;
- mutable search paths on legal/vector functions;
- `pg_net` installed in public;
- one RLS-enabled table lacks policy;
- `apex_secrets` contains 39 persistent secret values and needs separate vault/rotation review.

## Google Drive verified roots

Case root: `LEGAL-CASE-1FDV` — folder `1UBkpPVSp9U9bTSSrepMK-1kz_0CeRUeH`.

Verified children: `Active`, `Archive`, `Evidence`, `Motions`, and duplicate `0_CASE_MASTER` children requiring later identity reconciliation rather than flattening.

Evidence root: `EVIDENCE-AND-FORENSICS` — folder `1Wp4PJOyUtl341BeN4Tu9i8_XK_eaqAVD`.

Verified children: `FORENSIC-ORGANIZER-BRIDGE`, `Evidence Proofs Master`, `FORENSIC_ARCHIVE_2026`, `Forensic_Albums`.

Specialized audio root: `PILLAR 3: EVIDENCE VAULT` — folder `1Ovk8RrhMBeQObcMxRN6b0YiMx3XhKm5U`.

Verified children: recording library and transcription pipeline.

## Dropbox verified roots

Team mount: `/Kahala Home Inspectors`.

Canonical case surface: `/Kahala Home Inspectors/CASE_1FDV-23-0001009` (`id:M3qKixNrNsgAAAAAAATRRg`).

Verified children: `00_FILING`, `01_MOTIONS`, `02_EVIDENCE`, `03_FORENSIC`, `04_LEGAL`, `05_DEFENDANTS`.

Untrusted intake surface: `/Kahala Home Inspectors/FileBoss_Inbox` (`id:M3qKixNrNsgAAAAAAAL4zg`).

No Dropbox objects were moved, renamed, copied, created, shared, or deleted.

## Result

AKOS runtime manifest advanced to v1.1.0 with exact project IDs, folder IDs, namespace paths, file IDs, security gates, and next executable read-only steps.
