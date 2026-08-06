"""Verify the Resume Master + PSYSOC-X + Web Design Pro candidate loadout."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from infinity_stones import StoneRegistry, compose_loadout
from infinity_stones.receipts import digest, write_atomic_json


REQUIRED_RESOURCE_PATHS = (
    "stones/resume-master/personas/personas.json",
    "stones/resume-master/skills/SKILLS.md",
    "stones/resume-master/resources/casey-barton.resume-master.v18.json",
    "stones/resume-master/resources/resource-registry.json",
    "stones/resume-master/tools/tools.json",
    "stones/resume-master/connectors/connectors.json",
    "stones/resume-master/templates/master-resume.md",
    "stones/resume-master/templates/ats-resume.txt",
    "stones/resume-master/tests/cases.json",
    "stones/web-design-pro/personas/personas.json",
    "stones/web-design-pro/skills/SKILLS.md",
    "stones/web-design-pro/resources/design-system.json",
    "stones/web-design-pro/tools/tools.json",
    "stones/web-design-pro/connectors/connectors.json",
    "stones/web-design-pro/templates/index.html",
    "stones/web-design-pro/templates/styles.css",
    "stones/web-design-pro/tests/cases.json",
    "upgrades/resume-do-it-again/upgrade.json",
    "gauntlets/resume-master-psysoc-x-web-design-pro.json",
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain an object")
    return data


def verify(root: Path) -> dict[str, Any]:
    registry = StoneRegistry.load(root)
    plan = compose_loadout(
        registry,
        stones=("PSYSOC-X", "resume master", "web design pro"),
        upgrades=("resume do it again",),
    )
    missing = [path for path in REQUIRED_RESOURCE_PATHS if not (root / path).is_file()]

    gauntlet = _load_json(
        root / "gauntlets" / "resume-master-psysoc-x-web-design-pro.json"
    )
    resume_data = _load_json(
        root / "stones" / "resume-master" / "resources" /
        "casey-barton.resume-master.v18.json"
    )
    design_system = _load_json(
        root / "stones" / "web-design-pro" / "resources" / "design-system.json"
    )
    html = (
        root / "stones" / "web-design-pro" / "templates" / "index.html"
    ).read_text(encoding="utf-8")
    css = (
        root / "stones" / "web-design-pro" / "templates" / "styles.css"
    ).read_text(encoding="utf-8")

    checks = {
        "resources_present": not missing,
        "gauntlet_digest_matches": gauntlet["verification"]["loadout_digest"] == plan.digest,
        "facts_invariant": resume_data.get("facts_invariant") is True,
        "artifact_hashes_well_formed": all(
            len(item.get("sha256", "")) == 64
            for item in resume_data.get("artifacts", [])
        ),
        "zero_script_budget": design_system["budgets"]["client_scripts"] == 0,
        "zero_tracker_budget": design_system["budgets"]["trackers"] == 0,
        "html_script_free": "<script" not in html.lower(),
        "semantic_landmarks": all(
            marker in html.lower()
            for marker in ("<header", "<main", "<section", "<footer")
        ),
        "responsive_css": "@media" in css and "grid-template-columns" in css,
        "accessibility_markers": (
            ":focus-visible" in css and "prefers-reduced-motion" in css
        ),
        "artifact_links_present": all(
            marker in html
            for marker in (
                "/downloads/Casey_Barton_Resume.pdf",
                "/downloads/Casey_Barton_Resume.docx",
                "/resume/ats.txt",
            )
        ),
    }
    conclusion = "VERIFIED" if all(checks.values()) else "FAILED"
    receipt = {
        "schema": "glaciereq.resume-master-stones-verification.v1",
        "conclusion": conclusion,
        "loadout": {
            "stones": plan.stones,
            "upgrades": plan.upgrades,
            "digest": plan.digest,
        },
        "checks": checks,
        "missing_resources": missing,
        "evidence_level": "TEST" if conclusion == "VERIFIED" else "UNVERIFIED",
        "non_claims": [
            "production deployment",
            "ATS-vendor acceptance",
            "accessibility certification",
            "recruiter response or hiring outcome",
        ],
    }
    receipt["receipt_digest"] = digest(receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = verify(args.root.resolve())
    if args.output:
        write_atomic_json(args.output, receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["conclusion"] == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
