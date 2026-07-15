# CASEBRAIN Blocker Reconciliation — 2026-07-15

## Scope

Read-only connector discovery performed through AKOS. No evidence was moved, renamed, copied, deleted, shared, or modified. No Supabase migration was applied.

## Supabase

Previous state: no visible projects.

Current verified state:
- Organization: `casey's projects`
- Organization ID: `vercel_icfg_eWX1sAAKEYqrLzXO3GjFkyY3`
- Project: `supabase-backend-ops`
  - Project ID: `dyhprklicgewmrimecey`
  - Region: `us-east-1`
  - Status: `ACTIVE_HEALTHY`
- Project: `supabase-glaciereq`
  - Project ID: `kjebemdgvjvuutzvhbtp`
  - Region: `us-east-1`
  - Status: `ACTIVE_HEALTHY`

Reconciled blocker: project discovery is no longer blocked. Deployment remains gated on selecting the intended staging target, reviewing existing tables/migrations, applying `supabase/migrations/0001_casebrain_core.sql` only to an approved non-production target, and running security/performance advisors.

## Google Drive

Root discovery completed read-only.

Strong case-specific candidate roots:
- `LEGAL-CASE-1FDV` — `1UBkpPVSp9U9bTSSrepMK-1kz_0CeRUeH`
- `EVIDENCE-AND-FORENSICS` — `1Wp4PJOyUtl341BeN4Tu9i8_XK_eaqAVD`
- `0_CASE_MASTER` — `1Z_B3NB46wYtFpxpjSCZ4NdLORZ2x5vOW`
- `🔐 PILLAR 3: EVIDENCE VAULT — 600 Recordings + 235 Exhibits` — `1Ovk8RrhMBeQObcMxRN6b0YiMx3XhKm5U`
- `01_LEGAL_CASE` — `1dDqQJIDmtn-Q2hSppbEfwgR0nYsoEBVe`
- `01_EXHIBITS` — `1QQ3Yj5swykKh0CXuFPV58ZY6JaYfxOHE`

Reconciled blocker: candidate roots are now known. Activation remains gated on choosing one canonical case root and one canonical evidence root, then running a read-only manifest/hash pass before any organization proposal.

## Dropbox

Root discovery completed read-only.

Visible mounted roots:
- `/Kahalainspector Team Folder` — `id:M3qKixNrNsgAAAAAAAAACg`
- `/Kahala Home Inspectors` — `id:M3qKixNrNsgAAAAAAAAACA`

Reconciled blocker: Dropbox connectivity works, but neither root is safe to designate as a legal intake root. A verified case-specific child path must be identified or created under explicit approval before indexing.

## ClickUp

Known CASEBRAIN execution task: `86ajhtzgc`.

The connector again advertised `clickup_create_task_comment`, but invocation returned `Tool clickup_create_task_comment not found`. No comment was created and no status was changed.

Reconciled blocker: this is a connector action-routing defect, not a missing task or missing workspace object. AKOS/GitHub remains the durable receipt surface until the ClickUp action becomes callable.

## Next governed slice

1. Inspect both Supabase projects read-only: tables, migrations, branches, functions, extensions, and advisors.
2. Select the safer staging target based on observed contents; do not assume by project name.
3. Inspect the six Drive candidate folders one level deep and produce a root-selection scorecard.
4. Inspect each Dropbox mount one level deep for an existing case-specific child folder.
5. Update the AKOS runtime manifest with verified identifiers and connector health.
6. Apply no destructive or evidence-changing operation without explicit approval.
