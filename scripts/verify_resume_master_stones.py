"""Verify the Resume Master + PSYSOC-X + Web Design Pro loadout."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from infinity_stones import StoneRegistry, compose_loadout
from infinity_stones.models import ManifestError
from infinity_stones.receipts import digest, write_atomic_json


LOADOUT_STONES = ("PSYSOC-X", "resume master", "web design pro")
LOADOUT_UPGRADES = ("resume do it again",)
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
APPROVED_ARTIFACT_SHA256 = {
    "CASEY_BARTON_RESUME_MASTER_PSYSOC_X_V18_WEB_DESIGN_PRO_2026-08-06.docx":
        "a458bf7b79aaeb83675cfa1c87305fb8a6c52d3515f26a738fc94a52d9942cbe",
    "CASEY_BARTON_RESUME_MASTER_PSYSOC_X_V18_WEB_DESIGN_PRO_2026-08-06.pdf":
        "56799cbe9d8ed2a65e72e504490ac94ee3c28a08ead81a81ce577bf59b321ab5",
    "CASEY_BARTON_RESUME_MASTER_PSYSOC_X_V18_ATS.txt":
        "7296e3b1fd952b2a313d4e6ea253346be851e9cee83179516cc041a7cd86cb05",
    "CASEY_BARTON_RESUME_MASTER_PSYSOC_X_V18_MANIFEST.json":
        "f98c39f9bddb7b511b7a634f25992512762dfef6b6685e1420386075f0b680b8",
    "CASEY_BARTON_RESUME_MASTER_PSYSOC_X_V18_WEB_DESIGN_PRO_2026-08-06.zip":
        "d92ed3260e003567a6a7a6756504bfb4838b611dd34ed746f4d301454fc593a9",
}
REQUIRED_RESOURCE_PATHS = (
    "stones/resume-master/personas/personas.json",
    "stones/resume-master/skills/SKILLS.md",
    "stones/resume-master/resources/casey-barton.resume-master.v18.json",
    "stones/resume-master/resources/resource-registry.json",
    "stones/resume-master/resources/web-projection.v18.json",
    "stones/resume-master/tools/tools.json",
    "stones/resume-master/connectors/connectors.json",
    "stones/resume-master/templates/master-resume.md",
    "stones/resume-master/templates/ats-resume.txt",
    "stones/resume-master/tests/cases.json",
    "stones/web-design-pro/personas/personas.json",
    "stones/web-design-pro/skills/SKILLS.md",
    "stones/web-design-pro/resources/design-system.json",
    "stones/web-design-pro/resources/experience-graph.json",
    "stones/web-design-pro/tools/tools.json",
    "stones/web-design-pro/connectors/connectors.json",
    "stones/web-design-pro/templates/index.html",
    "stones/web-design-pro/templates/styles.css",
    "stones/web-design-pro/tests/cases.json",
    "stones/web-design-pro/tests/multidimensional-cases.json",
    "upgrades/resume-do-it-again/upgrade.json",
    "gauntlets/resume-master-psysoc-x-web-design-pro.json",
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain an object")
    return data


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _artifact_checks(resume_data: dict[str, Any]) -> tuple[bool, bool]:
    artifacts = resume_data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        return False, False

    actual: dict[str, str] = {}
    for item in artifacts:
        if not isinstance(item, dict):
            return False, False
        name = item.get("name")
        sha256 = item.get("sha256")
        if not isinstance(name, str) or not isinstance(sha256, str):
            return False, False
        if HEX_64.fullmatch(sha256) is None:
            return False, False
        actual[name] = sha256
    return True, actual == APPROVED_ARTIFACT_SHA256


def _declared_case_checks(
    cases_data: dict[str, Any], html: str, css: str
) -> dict[str, bool]:
    cases = cases_data.get("cases")
    if not isinstance(cases, list) or not cases:
        return {"declared-cases-present": False}

    combined = f"{html}\n{css}"
    results: dict[str, bool] = {}
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            results["malformed-case"] = False
            continue
        expected = case.get("expected_markers", [])
        forbidden = case.get("forbidden_markers", [])
        valid_expected = isinstance(expected, list) and all(
            isinstance(marker, str) and marker in combined for marker in expected
        )
        valid_forbidden = isinstance(forbidden, list) and all(
            isinstance(marker, str) and marker.lower() not in combined.lower()
            for marker in forbidden
        )
        results[case["id"]] = valid_expected and valid_forbidden
    return results


def _multidimensional_contract_is_well_formed(data: dict[str, Any]) -> bool:
    cases = data.get("cases")
    return (
        data.get("schema") == "glaciereq.web-design-pro.multidimensional-cases.v1"
        and data.get("status") == "CANDIDATE"
        and isinstance(cases, list)
        and bool(cases)
        and all(
            isinstance(case, dict)
            and all(
                isinstance(case.get(field), str) and bool(case[field].strip())
                for field in ("id", "requirement", "failure")
            )
            for case in cases
        )
    )


def verify(root: Path) -> dict[str, Any]:
    missing = [path for path in REQUIRED_RESOURCE_PATHS if not (root / path).is_file()]
    errors: list[str] = []
    plan = None

    try:
        registry = StoneRegistry.load(root)
        plan = compose_loadout(
            registry,
            stones=LOADOUT_STONES,
            upgrades=LOADOUT_UPGRADES,
        )
    except (FileNotFoundError, KeyError, TypeError, ValueError, ManifestError) as exc:
        errors.append(f"registry-or-composition: {type(exc).__name__}: {exc}")

    gauntlet: dict[str, Any] = {}
    resume_data: dict[str, Any] = {}
    design_system: dict[str, Any] = {}
    web_projection: dict[str, Any] = {}
    cases_data: dict[str, Any] = {}
    multidimensional_cases: dict[str, Any] = {}
    html = ""
    css = ""

    if not missing:
        resources = {
            "gauntlet": (
                root / "gauntlets" /
                "resume-master-psysoc-x-web-design-pro.json",
                "json",
            ),
            "resume-data": (
                root / "stones" / "resume-master" / "resources" /
                "casey-barton.resume-master.v18.json",
                "json",
            ),
            "design-system": (
                root / "stones" / "web-design-pro" / "resources" /
                "design-system.json",
                "json",
            ),
            "web-projection": (
                root / "stones" / "resume-master" / "resources" /
                "web-projection.v18.json",
                "json",
            ),
            "web-cases": (
                root / "stones" / "web-design-pro" / "tests" / "cases.json",
                "json",
            ),
            "multidimensional-cases": (
                root / "stones" / "web-design-pro" / "tests" /
                "multidimensional-cases.json",
                "json",
            ),
            "html": (
                root / "stones" / "web-design-pro" / "templates" / "index.html",
                "text",
            ),
            "css": (
                root / "stones" / "web-design-pro" / "templates" / "styles.css",
                "text",
            ),
        }
        loaded: dict[str, Any] = {}
        for name, (path, kind) in resources.items():
            try:
                loaded[name] = _load_json(path) if kind == "json" else _read_text(path)
            except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError) as exc:
                errors.append(f"{name}: {type(exc).__name__}: {exc}")
        gauntlet = loaded.get("gauntlet", {})
        resume_data = loaded.get("resume-data", {})
        design_system = loaded.get("design-system", {})
        web_projection = loaded.get("web-projection", {})
        cases_data = loaded.get("web-cases", {})
        multidimensional_cases = loaded.get("multidimensional-cases", {})
        html = loaded.get("html", "")
        css = loaded.get("css", "")

    hashes_well_formed, artifact_identities_match = _artifact_checks(resume_data)
    required_text = web_projection.get("required_text", [])
    required_links = web_projection.get("required_links", [])
    source_digest = digest(resume_data) if resume_data else ""
    projection_source_digest = web_projection.get("canonical_resume_digest")
    source_digest_marker = (
        f'name="glaciereq-resume-source-sha256" content="{source_digest}"'
    )
    declared_case_checks = _declared_case_checks(cases_data, html, css)

    checks = {
        "resources_present": not missing,
        "resources_parse": not errors,
        "gauntlet_digest_matches": bool(plan) and (
            gauntlet.get("verification", {}).get("loadout_digest") == plan.digest
        ),
        "facts_invariant": resume_data.get("facts_invariant") is True,
        "artifact_hashes_well_formed": hashes_well_formed,
        "artifact_identities_match": artifact_identities_match,
        "zero_script_budget": (
            design_system.get("budgets", {}).get("client_scripts") == 0
        ),
        "zero_tracker_budget": (
            design_system.get("budgets", {}).get("trackers") == 0
        ),
        "html_script_free": "<script" not in html.lower(),
        "semantic_landmarks": all(
            marker in html.lower()
            for marker in ("<header", "<main", "<section", "<footer")
        ),
        "responsive_css": all(
            marker in css for marker in ("@media", "grid-template-columns", "clamp(")
        ),
        "accessibility_markers": (
            ":focus-visible" in css and "prefers-reduced-motion" in css
        ),
        "web_projection_declared": (
            web_projection.get("schema") == "glaciereq.resume-web-projection.v1"
            and isinstance(required_text, list) and bool(required_text)
            and isinstance(required_links, list) and bool(required_links)
        ),
        "web_projection_bound_to_canonical": (
            isinstance(projection_source_digest, str)
            and projection_source_digest == source_digest
        ),
        "web_content_consistent": (
            isinstance(required_text, list)
            and all(isinstance(marker, str) and marker in html for marker in required_text)
            and isinstance(required_links, list)
            and all(isinstance(link, str) and link in html for link in required_links)
            and source_digest_marker in html
        ),
        "declared_web_cases_pass": (
            bool(declared_case_checks) and all(declared_case_checks.values())
        ),
        "multidimensional_contract_declared": (
            _multidimensional_contract_is_well_formed(multidimensional_cases)
        ),
    }

    conclusion = "VERIFIED" if all(checks.values()) and not errors else "FAILED"
    receipt = {
        "schema": "glaciereq.resume-master-stones-verification.v2",
        "conclusion": conclusion,
        "loadout": {
            "stones": plan.stones if plan else list(LOADOUT_STONES),
            "upgrades": plan.upgrades if plan else list(LOADOUT_UPGRADES),
            "digest": plan.digest if plan else None,
        },
        "checks": checks,
        "declared_case_checks": declared_case_checks,
        "missing_resources": missing,
        "errors": errors,
        "canonical_resume_digest": source_digest or None,
        "evidence_level": "TEST" if conclusion == "VERIFIED" else "UNVERIFIED",
        "non_claims": [
            "production deployment",
            "ATS-vendor acceptance",
            "accessibility certification",
            "recruiter response or hiring outcome",
            "browser execution of multidimensional candidate behaviors",
            "production reconstruction of the multidimensional candidate extension",
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
