from __future__ import annotations

import json
from pathlib import Path

import yaml

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


def test_repository_workflows_are_read_only_verification_only() -> None:
    workflow_root = ROOT / ".github" / "workflows"
    workflows = sorted(
        path
        for path in workflow_root.iterdir()
        if path.suffix.lower() in {".yml", ".yaml"}
    )
    assert workflows, "AKOS should own repository-local verification workflows"

    for path in workflows:
        text = path.read_text(encoding="utf-8")
        payload = yaml.safe_load(text)
        assert isinstance(payload, dict), f"workflow is not a mapping: {path}"
        assert payload.get("permissions") == {"contents": "read"}, (
            f"repository workflow permissions must be exactly contents: read: {path}"
        )

        lowered = text.lower()
        for forbidden in (
            "pull_request_target",
            "secrets.",
            "apex_private_read_token",
            "apex_control_token",
        ):
            assert forbidden not in lowered, f"forbidden workflow capability {forbidden}: {path}"

        jobs = payload.get("jobs")
        assert isinstance(jobs, dict) and jobs, f"workflow has no jobs: {path}"
        checkout_steps = []
        for job in jobs.values():
            assert isinstance(job, dict), f"workflow job is not a mapping: {path}"
            steps = job.get("steps")
            assert isinstance(steps, list) and steps, f"workflow job has no steps: {path}"
            for step in steps:
                if not isinstance(step, dict):
                    continue
                if str(step.get("uses", "")).startswith("actions/checkout@"):
                    checkout_steps.append(step)
                    options = step.get("with") or {}
                    assert options.get("persist-credentials") is False, (
                        f"checkout credentials must not persist: {path}"
                    )
                    assert "repository" not in options, (
                        "verification workflows must not checkout "
                        f"another repository: {path}"
                    )
        assert checkout_steps, f"workflow does not establish a checked-out source: {path}"


def test_verified_reversible_improvements_execute_without_redundant_permission() -> None:
    path = ROOT / "manifests/runtime/AKOS_OPERATIONAL_COGNITION.json"
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    authority = payload["execution_authority"]
    assert authority["default_mode"] == "execute_verify_persist_report"
    assert authority["redundant_confirmation"] == "forbidden"
    assert authority["pr_is_completion_when_safe_release_remains"] is False
    assert authority["auto_execute_requires"] == [
        "clearly_beneficial",
        "objective_preserving",
        "within_standing_authority",
        "non_destructive_or_recoverable",
        "verified_or_immediately_verifiable",
    ]

    assert payload["mutation_gates"]["mutate_reversible"].startswith("auto_execute_if_")
    assert payload["mutation_gates"]["merge_verified_change"] == (
        "auto_execute_if_authorized_green_and_recoverable"
    )
    assert "no_redundant_confirmation_after_green_gates" in payload["anti_loop_rules"]
    assert "no_pr_as_completion_when_safe_merge_is_authorized" in payload["anti_loop_rules"]
    assert payload["promotion_gate"]["human_review"] == (
        "required_only_when_confirmation_triggered"
    )
