"""Deterministic expert-council review for generated career artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_RESOURCE_DIR = Path(__file__).with_name("resources")
_DEFAULT_COUNCIL = _RESOURCE_DIR / "persona-council.v1.json"


def load_persona_council(path: Path = _DEFAULT_COUNCIL) -> dict[str, Any]:
    """Load the versioned expert council contract."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("personas"), list):
        raise ValueError("persona council resource is malformed")
    return payload


def run_persona_council(
    graph_data: dict[str, Any],
    *,
    target_role: str,
    job_analysis: dict[str, Any],
    ats_report: dict[str, Any],
    portfolio_reports: dict[str, Any],
) -> dict[str, Any]:
    """Run transparent rule-based review passes and cross-check their findings."""

    council = load_persona_council()
    proof_count = len(graph_data.get("proof", []))
    systems_count = len(graph_data.get("selected_systems", []))
    missing_count = len(job_analysis.get("missing_skill_ids", []))
    ats_checks = ats_report.get("common_checks", {})
    passes: list[dict[str, Any]] = []
    for persona in council["personas"]:
        findings: list[dict[str, str]] = []
        checks = set(persona.get("checks", []))
        if "technical depth" in checks and systems_count < 2:
            findings.append(
                {
                    "severity": "ADVISORY",
                    "finding": "Fewer than two selected systems are available for technical-depth review.",
                }
            )
        if "traceability" in checks and proof_count == 0:
            findings.append(
                {
                    "severity": "BLOCKING",
                    "finding": "No canonical proof records are available.",
                }
            )
        if "keyword coverage" in checks and missing_count:
            findings.append(
                {
                    "severity": "ADVISORY",
                    "finding": f"{missing_count} requested ontology skills have no canonical evidence match.",
                }
            )
        if "scanability" in checks and not all(ats_checks.values()):
            findings.append(
                {
                    "severity": "BLOCKING",
                    "finding": "One or more transparent ATS structure checks failed.",
                }
            )
        if "semantic structure" in checks and not portfolio_reports.get(
            "accessibility", {}
        ).get("checks", {}).get("semantic_landmarks", False):
            findings.append(
                {"severity": "BLOCKING", "finding": "Semantic landmarks check failed."}
            )
        if "metadata" in checks and not portfolio_reports.get("seo", {}).get(
            "checks", {}
        ).get("open_graph", False):
            findings.append(
                {"severity": "BLOCKING", "finding": "OpenGraph metadata check failed."}
            )
        passes.append(
            {
                "persona_id": persona["id"],
                "role": persona["role"],
                "checks": persona.get("checks", []),
                "findings": findings,
                "state": "PASSED" if not any(item["severity"] == "BLOCKING" for item in findings) else "FAILED",
            }
        )
    blocking = [
        {"persona_id": item["persona_id"], **finding}
        for item in passes
        for finding in item["findings"]
        if finding["severity"] == "BLOCKING"
    ]
    return {
        "schema": "glaciereq.persona-council-review.v1",
        "target_role": target_role,
        "state": "PASSED" if not blocking else "FAILED",
        "passes": passes,
        "blocking_findings": blocking,
        "cross_review": {
            "method": "Every pass receives the same canonical graph and generated reports; no persona may add facts.",
            "council_rule": council.get("council_rule"),
        },
    }
