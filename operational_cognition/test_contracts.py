from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_machine_contracts_are_valid_json() -> None:
    for relative in (
        "schemas/operational_cognition.schema.json",
        "manifests/runtime/AKOS_OPERATIONAL_COGNITION.json",
    ):
        with (ROOT / relative).open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        assert isinstance(payload, dict)


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
