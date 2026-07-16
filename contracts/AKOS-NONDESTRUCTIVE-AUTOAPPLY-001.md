# AKOS Non-Destructive Auto-Apply Contract — 001

Effective: 2026-07-15
Controller: AKOS
Scope: CASEBRAIN federation and case `1FDV-23-0001009`

## Operating rule

AKOS may proceed automatically, without a separate dry-run approval cycle, when an action is additive, reversible, and does not alter the evidentiary source object.

## Auto-approved operations

- read and enumerate connected sources;
- compute metadata and content hashes;
- create immutable manifests, indexes, crosswalks, receipts, and provenance records;
- extract text or metadata into clearly labeled derivative records;
- classify, tag, link, deduplicate by reference, and build timelines or actor graphs;
- create additive Git branches, commits, pull requests, issues, and documentation;
- insert additive Supabase registry, queue, receipt, crosswalk, and derived-analysis rows when schema-valid and idempotent;
- create or update Notion and ClickUp projections that point back to canonical source records;
- copy evidence only when the original remains untouched, the copy is labeled derivative, and both source and destination receive a receipt;
- run validators, security advisors, consistency checks, and reconciliation jobs.

## Forensic requirements

Every automated operation must preserve or record, when available:

- source system and stable source pointer;
- original filename or object name;
- source object ID;
- collection timestamp in UTC;
- SHA-256 for file bytes, or a clearly labeled metadata-manifest hash when bytes are unavailable;
- byte count and MIME type when available;
- original-versus-derivative designation;
- transformation description and tool/version;
- case ID and stable `CBR-*` identity;
- idempotency key;
- append-only execution receipt;
- verification status and confidence;
- operator or automation identity.

A metadata hash must never be represented as a file-content hash.

## Operations still requiring explicit confirmation

- delete, permanently remove, or overwrite source material;
- rename or move evidentiary source objects;
- merge or flatten conflicting folders or identities;
- replace an original with a derivative;
- modify an existing court-filed or signed document;
- publicly share, send, serve, file, publish, or communicate externally;
- apply a live database migration that changes privileges, drops objects, or can interrupt service;
- expose, rotate, transfer, or delete secrets or credentials;
- promote an allegation or inference to established fact without adequate source support;
- incur a new charge or provision a billable resource.

## Default conflict behavior

When identities, duplicates, dates, or source records conflict, AKOS preserves every variant, assigns separate stable IDs, records the contradiction, and continues all other non-destructive work. A conflict blocks only the contested merge or promotion, not the whole pipeline.

## Failure behavior

Connector failure is recorded as a receipt and routed to a fallback surface. It does not authorize fabricated success, silent data loss, or destructive retries.
