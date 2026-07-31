from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LAW_SPEC = ROOT / "specs" / "AKOS-LAW-001_FOUNDATIONAL_LAWS.md"
MANIFEST = ROOT / "AKOS_MANIFEST.yaml"
ECHO_ADR = ROOT / "adr" / "ADR-0012_ECHO_STANDALONE_GOVERNED_PRODUCT.md"
ECHO_CONTRACT = ROOT / "contracts" / "AKOS-ECHO-001_INTEGRATION_CONTRACT.md"


def test_law_017_is_canonical_and_machine_declared() -> None:
    text = LAW_SPEC.read_text(encoding="utf-8")

    assert "## LAW-017 — Best-of-All-Worlds Integration" in text
    assert "DISCOVER -> COMPARE -> PRESERVE -> COMBINE -> TEST -> PROMOTE -> RETIRE" in text
    assert "best_of_all_worlds_integration" in text
    assert "preserve every verified strength while removing every verified weakness" in text


def test_manifest_enforces_best_of_all_worlds_policy() -> None:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    governance = manifest["governance"]
    principles = set(manifest["required_principles"])
    gates = set(manifest["quality_gates"])

    assert governance["integration_doctrine"] == "best_of_all_worlds"
    assert "best_of_all_worlds_integration" in principles
    assert "no_novelty_only_refactor" in principles
    assert "regression_requires_explicit_evidence_backed_tradeoff" in principles
    assert "best_of_all_worlds_comparison" in gates
    assert "regression_preservation" in gates
    assert "retirement_proof" in gates


def test_echo_is_standalone_but_governed_by_akos() -> None:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    governed = manifest["relationships"]["governs"]
    echo = next(item for item in governed if item["canonical_id"] == "SYS-ECHO-001")

    assert echo["intended_repository"] == "GlacierEQ/ECHO"
    assert echo["state"] == "repository_not_yet_observed"
    assert echo["relation"] == "GOVERNS"
    assert ECHO_ADR.is_file()
    assert ECHO_CONTRACT.is_file()

    adr = ECHO_ADR.read_text(encoding="utf-8")
    contract = ECHO_CONTRACT.read_text(encoding="utf-8")

    assert "standalone product repository governed by AKOS" in adr
    assert "AKOS owns" in contract
    assert "ECHO owns" in contract
    assert "repository_observed: false" in contract
    assert "product_runtime_verified: false" in contract
