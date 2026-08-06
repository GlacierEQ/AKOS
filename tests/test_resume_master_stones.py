"""Contract tests for Resume Master + PSYSOC-X + Web Design Pro."""

from __future__ import annotations

import json
from pathlib import Path

from infinity_stones import StoneRegistry, compose_loadout

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def test_registry_resolves_resume_master_aliases() -> None:
    registry = StoneRegistry.load(ROOT)
    assert registry.resolve("resume master") == "stone-resume-master"
    assert registry.resolve("web design pro") == "stone-web-design-pro"
    assert registry.resolve("resume do it again") == "upgrade-resume-do-it-again"


def test_three_stone_loadout_is_deterministic() -> None:
    registry = StoneRegistry.load(ROOT)
    first = compose_loadout(
        registry,
        stones=("PSYSOC-X", "resume master", "web design pro"),
        upgrades=("resume do it again",),
    )
    second = compose_loadout(
        registry,
        stones=("PSYSOC-X", "resume master", "web design pro"),
        upgrades=("resume do it again",),
    )
    assert first == second
    assert len(first.digest) == 64
    gauntlet = load_json("gauntlets/resume-master-psysoc-x-web-design-pro.json")
    assert gauntlet["verification"]["loadout_digest"] == first.digest


def test_canonical_resume_preserves_invariants_and_hashes() -> None:
    data = load_json(
        "stones/resume-master/resources/casey-barton.resume-master.v18.json"
    )
    assert data["facts_invariant"] is True
    assert data["identity"]["name"] == "Casey Del Carpio Barton"
    assert any(item["metrics"].get("tests_total") == 69 for item in data["proof"])
    assert all(len(item["sha256"]) == 64 for item in data["artifacts"])
    assert data["evidence_limits"]


def test_declared_resume_resources_exist() -> None:
    manifest = load_json("stones/resume-master/stone.json")
    resources = manifest["resources"]
    paths = [
        resources["personas"],
        resources["skills"],
        resources["canonical_data"],
        resources["resource_registry"],
        resources["tools"],
        resources["connectors"],
        resources["tests"],
        *resources["templates"],
    ]
    assert all((ROOT / path).is_file() for path in paths)


def test_declared_web_resources_exist() -> None:
    manifest = load_json("stones/web-design-pro/stone.json")
    resources = manifest["resources"]
    paths = [
        resources["personas"],
        resources["skills"],
        resources["design_system"],
        resources["tools"],
        resources["connectors"],
        resources["tests"],
        *resources["templates"],
    ]
    assert all((ROOT / path).is_file() for path in paths)


def test_web_template_is_script_free_semantic_and_responsive() -> None:
    html = (
        ROOT / "stones/web-design-pro/templates/index.html"
    ).read_text(encoding="utf-8")
    css = (
        ROOT / "stones/web-design-pro/templates/styles.css"
    ).read_text(encoding="utf-8")
    assert "<script" not in html.lower()
    assert all(tag in html.lower() for tag in ("<header", "<main", "<section", "<footer"))
    assert "Skip to content" in html
    assert ":focus-visible" in css
    assert "prefers-reduced-motion" in css
    assert "@media" in css


def test_resume_cases_refuse_fabrication_and_private_material() -> None:
    cases = load_json("stones/resume-master/tests/cases.json")["cases"]
    by_id = {case["id"]: case for case in cases}
    assert by_id["reject-fabricated-metric"]["expected"]["decision"] == "REJECT"
    assert by_id["private-material-exclusion"]["expected"]["decision"] == "BLOCK"
