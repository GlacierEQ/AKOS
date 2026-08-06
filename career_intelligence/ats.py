"""Transparent ATS-oriented parsing heuristics and failure explanations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .platform_models import JobAnalysis

_RESOURCE_DIR = Path(__file__).with_name("resources")
_DEFAULT_SYSTEMS = _RESOURCE_DIR / "ats-systems.v1.json"


def _section_present(text: str, title: str) -> bool:
    return title.casefold() in text.casefold()


def score_ats_text(
    text: str,
    analysis: JobAnalysis,
    *,
    systems_path: Path = _DEFAULT_SYSTEMS,
) -> dict[str, Any]:
    """Score plain-text resume structure with explicit, non-vendor-certified rules."""

    systems = json.loads(systems_path.read_text(encoding="utf-8")).get("systems", [])
    common_checks = {
        "has_name": bool(text.splitlines() and text.splitlines()[0].strip()),
        "has_email": "@" in text,
        "has_phone": any(char.isdigit() for char in text[:500]),
        "has_experience": _section_present(text, "experience"),
        "has_skills": _section_present(text, "skills") or _section_present(text, "capabilities"),
        "has_education": _section_present(text, "education"),
        "plain_text": "<table" not in text.casefold() and "\x00" not in text,
        "reasonable_length": 500 <= len(text) <= 20000,
    }
    requested = set(analysis.requested_skill_ids)
    matched = {item.skill_id for item in analysis.matched_skills if item.score > 0}
    keyword_coverage = 1.0 if not requested else len(requested & matched) / len(requested)
    base_score = round(70 * sum(common_checks.values()) / len(common_checks) + 30 * keyword_coverage)

    reports: list[dict[str, Any]] = []
    for system in systems:
        warnings: list[str] = []
        if not common_checks["has_email"]:
            warnings.append("email was not detected")
        if not common_checks["has_phone"]:
            warnings.append("phone number was not detected")
        if not common_checks["has_experience"]:
            warnings.append("standard experience heading was not detected")
        if keyword_coverage < 0.5 and requested:
            warnings.append("less than half of requested ontology skills have canonical evidence matches")
        reports.append(
            {
                "id": system["id"],
                "label": system["label"],
                "score": base_score,
                "emphasis": system.get("emphasis", []),
                "warnings": warnings,
                "basis": "transparent structural heuristic; not vendor-certified parsing",
            }
        )
    return {
        "schema": "glaciereq.ats-report.v1",
        "state": "ANALYZED",
        "common_checks": common_checks,
        "keyword_coverage": round(keyword_coverage, 4),
        "systems": reports,
        "boundary": "Scores predict structural compatibility only and do not guarantee vendor parsing, ranking, or acceptance.",
    }
