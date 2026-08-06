# AKOS Infinity Stone Forge — Reversible Intelligence, Not Prompt Theater

> Manufactures named AI instincts into versioned, composable, testable runtime specializations without mutating the base model or promoting style into truth.

**Verified baseline:** `0.1.0` at repository-local evidence level `TEST` for PSYSOC-X + Do It Again.  
**Current branch candidate:** `0.2.0-candidate` adds Resume Master + Web Design Pro.  
**Candidate evidence state:** `UNVERIFIED` until exact-head CI and a promotion receipt exist.

## The Difference Between a Prompt and a Power

A sentence can summon a stone. A skill can inhabit it. A protocol can govern it. The stone is the complete specialization package: identity, domain, judgment, interfaces, boundaries, composition rules, personas, skills, resources, tools, connectors, templates, tests, rollback semantics, and receipts.

The verified baseline contains **PSYSOC-X** and the **Do It Again Protocol**. The current candidate adds:

- **Resume Master** — one canonical resume fact graph, evidence states, ATS/human/machine projections, artifact identity, and release receipts;
- **Web Design Pro** — information architecture, design tokens, semantic HTML, responsive CSS, accessibility checks, SEO metadata, and deployment verification;
- **Resume Do It Again** — preserve the newest canonical package, reconcile deltas, test every affected projection, and persist new hashes;
- **Resume Master · PSYSOC-X · Web Design Pro Gauntlet** — one governed loadout across all of the above.

## Inside the Forge

The forge supplies:

- validated stone and upgrade manifests;
- safe registry paths and alias-collision detection;
- deterministic loadout composition and SHA-256 digests;
- explicit compatibility and precedence checks;
- bounded PSYSOC-X calibration;
- persona, skill, resource, tool, connector, and template registries;
- atomic verification receipts;
- positive, boundary, refusal, artifact, semantic, responsive, and composition tests;
- exact read-only, secretless workflow authority.

## Enter Through the Registry

```bash
python -m pip install -e ".[dev]"
pytest -q tests/test_infinity_stones.py tests/test_psysoc_x.py
pytest -q tests/test_resume_master_stones.py
python scripts/verify_resume_master_stones.py \
  --output artifacts/ci/resume-master-stones.json
```

Canonical candidate resources:

- [`../registry/stones.json`](../registry/stones.json)
- [`../stones/psysoc-x/stone.json`](../stones/psysoc-x/stone.json)
- [`../stones/resume-master/stone.json`](../stones/resume-master/stone.json)
- [`../stones/web-design-pro/stone.json`](../stones/web-design-pro/stone.json)
- [`../upgrades/resume-do-it-again/upgrade.json`](../upgrades/resume-do-it-again/upgrade.json)
- [`../gauntlets/resume-master-psysoc-x-web-design-pro.json`](../gauntlets/resume-master-psysoc-x-web-design-pro.json)
- [`../docs/RESUME_MASTER_PSYSOC_X_WEB_DESIGN_PRO.md`](../docs/RESUME_MASTER_PSYSOC_X_WEB_DESIGN_PRO.md)

Candidate loadout identity:

```text
stone-psysoc-x
+ stone-resume-master
+ stone-web-design-pro
+ upgrade-resume-do-it-again

SHA-256: 68ff7e79d7127bd568d27e700bf3189660ce721b15bf420d17f63ebec298131d
```

## The Gauntlet Is a Composition, Not a Costume

```text
AKOS kernel + canonical evidence
              │
              ▼
          PSYSOC-X
 human reception • logic • dignity • limits
              │
              ▼
        Resume Master
 facts • claims • ATS • artifacts • hashes
              │
              ▼
       Web Design Pro
 hierarchy • semantics • responsive • accessibility
              │
              ▼
     Resume Do It Again
 preserve gains • reconcile • test • persist
              │
              ▼
resume-master-psysoc-x-web-design-pro gauntlet
```

## Evidence Boundary

The PSYSOC-X v0.1.0 baseline remains the only currently promoted Forge scope. The Resume Master and Web Design Pro resources on this branch are candidates. Their presence, completeness, or local structural validity does not equal exact-head CI success, production deployment, ATS-vendor acceptance, accessibility certification, recruiter response, hiring outcome, or business impact.
