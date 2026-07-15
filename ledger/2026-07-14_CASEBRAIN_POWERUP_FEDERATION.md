# Build Ledger — CASEBRAIN Powerup Federation

Date: 2026-07-14  
Family: FAM-CASEBRAIN  
Change status: proposed on review branch

## Inputs inspected

- Private GitHub repositories and open pull requests named in the federation
  registry.
- AKOS repository contract, agent contract, metadata standard, connector
  registry and Pro-Code methodology.
- AEON-777 pull request 51 truth contracts and runtime status.
- Existing Notion Aspen, AKOS, AWorkers, Casebuilder, HIVE, Worker Registry,
  Workers Leverage Plan and Verification Ledger pages.
- Current ClickUp AKOS integration tasks.
- CASE BRAIN preparation package in Drive as a secondary preparation record.

## Decisions

1. AKOS is governance canon after its manifest validates.
2. AEON-777 pull request 51 is the current CASEBRAIN truth-contract candidate.
3. GitHub is canonical; Notion and ClickUp are projections.
4. No repository or worker is production-live from a label alone.
5. Unsupported case narratives and model conclusions remain quarantined.
6. First runtime slice is one hashed source through a read-only adapter.

## Validation targets

- AKOS manifest validates against `repository_contract.schema.json`.
- Federation registry validates in strict Draft 2020-12 mode.
- Every repository entry has a 40-hex observed commit and explicit gates.
- Every worker is read-only, forbids external actions and forbids evidence
  mutation.
- Human gates cover legal, external, deadline, fact-promotion, write and
  connector activation actions.

## Known blockers

- AEON memory credential requires provider-side revocation and rotation.
- CASEBRAIN project discovery and extracted-memory indexing are inconsistent.
- Aspen projection pointers and health labels require repair.
- Aspen Supabase access policy and provenance enforcement are unsafe.
- Pro-Code implementation does not yet match its dispatch/auth contract.
- Notion contains duplicate hubs, unverified live claims and exposed secrets.

## Next receipt

Record the pull request URL, head SHA, schema-validation output and reviewer
decision. No `verified_live` status may be emitted from this ledger entry.
