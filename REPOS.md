# APEX Repos — Private-first portfolio map

**Policy (2026-07-12):** GlacierEQ originals are **private by default**.
Public only after **intelligent promotion** (scan → pro-AKOS pack → secret gate → explicit promote).

Canonical OS: this repo (`AKOS`). Pipeline flipper:
`~/GlacierEQ_Swarm/automations/repo-public-promotion-flipper.py`

## Visibility policy

| Stage | Rule |
|---|---|
| Default | 🔒 private |
| Legal / case | 🔒 **never** public |
| Forks / vendored | leave alone (not portfolio surface) |
| Job-app engineering | private → pack (AKOS.md, homepage) → scan secrets → `--promote` one-by-one |
| Bulk public | **forbidden** |

### Promote gates (all required)

1. Not legal/case/PII
2. Not a fork
3. Portfolio-eligible (AKOS / Colossus / SpaceX / APEX surface)
4. Has README
5. Secret scan clean
6. pro-AKOS pack applied while still private
7. Explicit promote command (human/agent)

## Knowledge / Control

| Repo | Role | Vis |
|---|---|---|
| [AKOS](https://github.com/GlacierEQ/AKOS) | Apex Knowledge OS | 🔒 → promote when ready |
| [token_saver](https://github.com/GlacierEQ/token_saver) | Token optimization | 🔒 |
| [mastermind](https://github.com/GlacierEQ/mastermind) | Mastermind control plane | 🔒 |
| [pro-code](https://github.com/GlacierEQ/pro-code) | Pro_Code standards | 🔒 |
| [AEON-777](https://github.com/GlacierEQ/AEON-777) | AEON brain / MOC | 🔒 |
| [job-application](https://github.com/GlacierEQ/job-application) | Portfolio hub | 🔒 |

## Colossus / SpaceX / APEX

Private portfolio trees (examples):

- Colossus core + alpha/omega: `xai-colossus-*`, `colossus-gateway`, …
- SpaceX helix: `spacex-*`
- APEX runtime: `apex-*`, `Pro-*` (non-legal)

Full categorized inventory:
`GlacierEQ_Swarm/state/ultimate_repo_map.md`

## Legal / Case (🔒 permanent)

Never promote:

- `1FDV-23-0001009-FEDERAL-WARFARE`
- `SUPERLUMINAL_CASE_MATRIX`
- `DOCKETS`, AspenGrove*, THE_CATACLYSM*, forensic/warfare case trees

## Intelligent public pipeline

```
private (default)
   → evaluate (--scan REPO)
   → pack pro-AKOS while private (--pack REPO)
   → secret scan clean
   → promote one (--promote REPO)
   → update this REPOS.md ✅ / 🌐
```

### Commands

```bash
# dry-run portfolio readiness
python3 ~/GlacierEQ_Swarm/automations/repo-public-promotion-flipper.py

# inspect one
python3 ~/GlacierEQ_Swarm/automations/repo-public-promotion-flipper.py --scan xai-colossus-cooling

# pack while private
python3 ~/GlacierEQ_Swarm/automations/repo-public-promotion-flipper.py --pack xai-colossus-cooling

# promote only if gates pass
python3 ~/GlacierEQ_Swarm/automations/repo-public-promotion-flipper.py --promote xai-colossus-cooling

# force portfolio private again
python3 ~/GlacierEQ_Swarm/automations/repo-public-promotion-flipper.py --reprivatize-portfolio
```

## Status legend

| Symbol | Meaning |
|---|---|
| 🔒 | Private (default / locked) |
| 🌐 | Public (passed intelligent promotion) |
| ✅ | Easter eggs embedded |
| 🔗 | AKOS bridge present |
| ⚠️ | Blocked (secrets / missing README / ineligible) |

## 2026-07-12 changelog

- Re-privatized bulk job-app surface (43 repos) after accidental bulk public flip
- Installed private-first promotion flipper
- Legal/case remains never-public
- Ultimate category map: `state/ultimate_repo_map.md`

## Architecture standards

- Double Helix — Alpha (what) ↔ Omega (how)
- Mastermind sidecar
- AKOS session continuity
- Exact SI constants; silent Easter eggs
- Local swarm: `~/GlacierEQ_Swarm` + AWorkers

This file is the source of truth for **promotion policy**, not a claim that everything is public.
