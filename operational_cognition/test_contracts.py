from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


MACHINE_CONTRACTS = (
    "schemas/operational_cognition.schema.json",
    "schemas/akos_system_topology.schema.json",
    "schemas/operational_maturity.schema.json",
    "manifests/runtime/AKOS_OPERATIONAL_COGNITION.json",
    "manifests/runtime/AKOS_SYSTEM_TOPOLOGY.json",
    "manifests/runtime/AKOS_OPERATIONAL_MATURITY.json",
)


def test_machine_contracts_are_valid_json() -> None:
    for relative in MACHINE_CONTRACTS:
        with (ROOT / relative).open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        assert isinstance(payload, dict)


def test_operational_maturity_rejects_subjective_score_contract() -> None:
    path = ROOT / "manifests/runtime/AKOS_OPERATIONAL_MATURITY.json"
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    assert payload["score_contract"]["unsupported_numeric_self_rating"] == "forbidden"
    assert payload["score_contract"]["unmeasured_state"] == "unassessed"


def test_artifact_lifecycle_is_complete_and_ordered() -> None:
    expected = [
        "located",
        "acquired",
        "hashed",
        "preserved",
        "parsed",
        "classified",
        "correlated",
        "drafted",
        "verified",
        "packaged",
        "stored",
        "logged",
        "ready_for_use",
    ]
    path = ROOT / "manifests/runtime/AKOS_OPERATIONAL_MATURITY.json"
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    assert payload["artifact_lifecycle"] == expected


def test_private_repository_owns_no_actions_workflows() -> None:
    workflow_root = ROOT / ".github" / "workflows"
    if not workflow_root.exists():
        return
    forbidden = sorted(
        path.relative_to(ROOT).as_posix()
        for path in workflow_root.iterdir()
        if path.suffix.lower() in {".yml", ".yaml"}
    )
    assert forbidden == [], (
        "AKOS is a private workload and policy repository; execution must route "
        f"through GlacierEQ/public-actions-runner-host, found: {forbidden}"
    )
