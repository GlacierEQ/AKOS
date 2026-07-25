# AKOS-GIT-001 — Master Strand Repository Architecture

**Status:** active draft  
**Version:** 0.1.1  
**Owner:** GlacierEQ / AKOS  
**Effective:** 2026-07-24

## Prime rule

For a single-operator GlacierEQ repository, the default branch is the visible working face and the canonical living system.

Branches are not alternate realities, waiting rooms, or long-term storage. A non-default branch is only a temporary ingestion surface whose unique value must be resolved into one of four outcomes:

1. **ABSORB** — integrate the functional improvement into the repository's canonical mainline.
2. **TRANSPLANT** — move the improvement to the canonical mainline of the repository where it actually belongs.
3. **QUARANTINE** — preserve the exact commit and reason outside the active working face when the content is unsafe, secret-bearing, synthetic, corrupt, or not yet trustworthy.
4. **DISCARD** — remove a duplicate, superseded, empty, bot-noise, or nonfunctional branch after proving it contains no unique retained value.

No fifth state exists. There is no indefinite “maybe later” branch.

## Master Strand

The canonical default branch is the **Master Strand**:

- all real logic is visible there;
- all accepted power is runnable there;
- all verified improvements are integrated there;
- all provenance and rollback points are recorded there;
- all system readers and agents treat it as the current truth.

For AKOS and operator-owned GlacierEQ repositories, `main` is the preferred canonical name. Repositories inherited from upstream may temporarily retain another default branch only until their role and migration path are explicitly resolved.

## Alpha–Omega Double Helix

Every accepted capability is promoted as a paired strand:

### Alpha strand — Function

- executable logic;
- schemas and interfaces;
- tests and acceptance criteria;
- operational configuration;
- user-visible capability.

### Omega strand — Truth and continuity

- source commit and origin repository;
- author and timestamp;
- provider receipt;
- verification result;
- hashes and artifact locations;
- supersession and rollback path;
- destination decision.

Function without provenance is unstable. Provenance without functioning code is archival only. The Master Strand carries both.

## Pillars and pistons

**Pillars** are stable repository responsibilities: policy, memory, execution, evidence, interface, orchestration, research, or domain-specific service.

**Pistons** are bounded capabilities that create working power.

A piston is placed where it strengthens the correct pillar:

- when it improves the current repository's core responsibility, absorb it here;
- when it is valuable but belongs to another repository, transplant it there;
- when it duplicates an existing stronger piston, preserve lineage and discard the weaker duplicate;
- when it crosses repository boundaries, extract a reusable package or contract rather than copying uncontrolled versions.

Repository consolidation is functional, not merely numerical. Fewer repositories and branches are valuable only when the surviving architecture becomes clearer, stronger, and easier to operate.

## Controlled branch extinction sequence

```text
INVENTORY
→ COMPARE AGAINST CANONICAL MAINLINE
→ IDENTIFY UNIQUE FUNCTION
→ CLASSIFY OWNERSHIP
→ ABSORB / TRANSPLANT / QUARANTINE / DISCARD
→ VERIFY DESTINATION MAINLINE
→ RECORD RECEIPT AND LINEAGE
→ CLOSE ASSOCIATED PR
→ ALIGN OLD REF TO CANONICAL HEAD
→ DELETE OLD REF
```

Deletion is the final operation, never the first.

## Conflict rule

A merge conflict does not preserve a branch indefinitely and does not justify blindly overwriting the mainline.

When the functional delta is valuable but the branch cannot merge cleanly:

1. identify the exact valuable files, commits, tests, interfaces, and behavior;
2. reapply that delta directly to the correct canonical mainline;
3. verify the resulting behavior;
4. record the source branch and commit as lineage;
5. align and delete the obsolete branch.

The function survives. The hidden alternate reality does not.

## Repository destination rule

A capability belongs in the repository whose declared responsibility, interfaces, data ownership, and operational lifecycle best match that capability.

Destination selection must consider:

- canonical purpose;
- existing interfaces and dependencies;
- data and security boundaries;
- execution plane;
- operator workflow;
- duplication risk;
- long-term maintenance cost;
- whether extraction creates a reusable shared package.

A branch is never kept merely because the correct destination has not yet been considered. The exact blocker and candidate destinations must be recorded.

## Bot and dependency branches

Automated update branches are not automatically valuable and are not automatically discarded.

They are evaluated by effect:

- security fix with compatible tests: absorb;
- superseded by a newer update: discard the older branch;
- conflicting duplicate update sets: select one coherent upgrade path;
- unverified major-version jump: quarantine or reconstruct on main with explicit verification;
- release metadata that reflects already-integrated function: write the correct metadata directly to main and discard the release branch.

## Branch extinction gate

A branch may be deleted only when one of these is true:

1. its unique functional delta is verified on the correct destination mainline;
2. its head is already reachable from the destination mainline;
3. its remaining delta is documented as duplicate, superseded, unsafe, corrupt, or intentionally rejected;
4. its exact commit SHA and disposition receipt have been preserved.

The gate returns an exact blocker when deletion is unsafe.

## Pull-request rule

Pull requests are not the canonical work surface for a single-operator repository.

Existing PRs are treated as branch discovery records. Their functional content is resolved into the Master Strand, then the PR is closed or marked merged. A new PR or temporary branch is permitted only by operator direction or when a bounded verification/review gate is required before canonical integration; it must be resolved promptly after the gate completes.

## Organization-wide objective

The GlacierEQ estate converges toward:

- one visible canonical mainline per active repository;
- explicit repository responsibilities;
- shared contracts instead of copied drift;
- no branch with unique unintegrated progress;
- no stale PR preserving hidden work;
- no release or bot branch outranking the working face;
- receipts proving where every retained capability went.

## Machine implementation

- Runtime: `operational_cognition/master_strand.py`
- Tests: `operational_cognition/test_master_strand.py`
- Manifest: `manifests/runtime/AKOS_MASTER_STRAND.json`
- Consolidation ledger: `ledger/2026-07-24_MASTER_STRAND_CONSOLIDATION.md`

## Truth boundary

This specification governs consolidation. It does not claim the entire GlacierEQ branch estate is already merged or deleted.

Completion requires an inventory of every owned repository and non-default ref, a recorded disposition for each unique branch, verified destination commits, closed PRs, and provider-confirmed branch deletion or an exact tooling blocker.
