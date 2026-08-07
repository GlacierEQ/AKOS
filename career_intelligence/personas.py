"""Reader and expert-persona models for deterministic career presentation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .platform_models import ReaderProfile

_RESOURCE_DIR = Path(__file__).with_name("resources")
_READER_PROFILES = _RESOURCE_DIR / "reader-profiles.v1.json"


def _tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(str(item) for item in value if isinstance(item, str) and item.strip())


def load_reader_profiles(path: Path = _READER_PROFILES) -> dict[str, ReaderProfile]:
    """Load explicit reader profiles from a versioned resource file."""

    data = json.loads(path.read_text(encoding="utf-8"))
    profiles: dict[str, ReaderProfile] = {}
    for item in data.get("profiles", []):
        profile = ReaderProfile(
            id=str(item["id"]),
            label=str(item["label"]),
            attention_budget_words=int(item["attention_budget_words"]),
            skepticism=str(item["skepticism"]),
            preferred_metrics=_tuple(item.get("preferred_metrics")),
            preferred_language=_tuple(item.get("preferred_language")),
            risk_tolerance=str(item["risk_tolerance"]),
            decision_criteria=_tuple(item.get("decision_criteria")),
            artifact_priority=_tuple(item.get("artifact_priority")),
        )
        profiles[profile.id] = profile
    return profiles


def resolve_reader_profile(value: str, *, profiles: dict[str, ReaderProfile] | None = None) -> ReaderProfile:
    """Resolve an audience by exact id, label, or a conservative role mapping."""

    available = profiles or load_reader_profiles()
    normalized = value.strip().casefold().replace("_", "-").replace(" ", "-")
    if normalized in available:
        return available[normalized]
    for profile in available.values():
        if profile.label.casefold() == value.strip().casefold():
            return profile

    mappings = (
        (("principal",), "principal-engineer"),
        (("staff",), "staff-engineer"),
        (("cto", "chief-technology"), "cto"),
        (("vp", "vice-president"), "vp-engineering"),
        (("government", "public-sector"), "government-reviewer"),
        (("defense", "mission"), "defense-reviewer"),
        (("startup", "founder"), "startup-founder"),
        (("faang", "big-tech"), "faang-panel"),
        (("open-source", "maintainer"), "open-source-maintainer"),
        (("recruiter", "talent"), "technical-recruiter"),
    )
    for terms, profile_id in mappings:
        if any(term in normalized for term in terms):
            return available[profile_id]
    return available["engineering-manager"]


def claim_weight(
    claim: dict[str, Any],
    profile: ReaderProfile,
    *,
    keyword_hits: int = 0,
) -> int:
    """Score a canonical claim for one reader without altering its factual content."""

    state = str(claim.get("evidence_state", "")).casefold()
    evidence_weight = 35 if "verified" in state else 24 if "recorded" in state else 12
    metrics = claim.get("metrics", {})
    metric_weight = min(30, 6 * len(metrics)) if isinstance(metrics, dict) else 0
    language = " ".join(str(claim.get(key, "")) for key in ("label", "claim")).casefold()
    language_weight = sum(4 for term in profile.preferred_language if term.casefold() in language)
    return evidence_weight + metric_weight + min(24, keyword_hits * 4) + language_weight


def prioritize_proof(
    proof: list[dict[str, Any]],
    profile: ReaderProfile,
    *,
    keyword_terms: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
    """Return proof records ordered for the reader while preserving records exactly."""

    def score(item: dict[str, Any]) -> tuple[int, str]:
        haystack = " ".join(str(item.get(key, "")) for key in ("label", "claim")).casefold()
        hits = sum(1 for term in keyword_terms if term.casefold() in haystack)
        return claim_weight(item, profile, keyword_hits=hits), str(item.get("id", ""))

    return sorted(proof, key=score, reverse=True)
