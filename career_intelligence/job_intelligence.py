"""Evidence-bound job analysis, gap mapping, and interview topic extraction."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from typing import Any

from .personas import resolve_reader_profile
from .platform_models import JobAnalysis, ReaderProfile
from .skill_ontology import (
    extract_requested_skills,
    load_skill_ontology,
    match_skills_to_evidence,
)


def analyze_job(
    graph_data: dict[str, Any],
    *,
    target_role: str,
    audience: str,
    job_text: str = "",
    reader_profile: ReaderProfile | None = None,
) -> JobAnalysis:
    """Analyze a role against the canonical career graph without inventing qualifications."""

    profile = reader_profile or resolve_reader_profile(audience or target_role)
    ontology = load_skill_ontology()
    requested = extract_requested_skills(f"{target_role}\n{job_text}", ontology)
    matches = match_skills_to_evidence(graph_data, requested, ontology)
    matched_ids = {item.skill_id for item in matches if item.score > 0}
    missing = tuple(sorted(set(requested) - matched_ids))
    proof_ids = tuple(
        sorted({evidence_id for item in matches for evidence_id in item.evidence_ids if not evidence_id.startswith("system:")})
    )
    topics = tuple(
        dict.fromkeys(
            topic
            for skill_id in requested
            for topic in ontology[skill_id].interview_topics
            if skill_id in ontology
        )
    )
    return JobAnalysis(
        target_role=target_role.strip(),
        audience_id=profile.id,
        job_text_sha256=sha256(job_text.encode("utf-8")).hexdigest(),
        requested_skill_ids=requested,
        matched_skills=matches,
        missing_skill_ids=missing,
        matched_proof_ids=proof_ids,
        interview_topics=topics,
        salary_market_state="UNAVAILABLE_WITHOUT_LIVE_MARKET_DATA",
    )


def job_analysis_to_dict(analysis: JobAnalysis) -> dict[str, Any]:
    """Serialize the analysis using stable, explicit fields."""

    payload = asdict(analysis)
    payload["matched_skills"] = [asdict(item) for item in analysis.matched_skills]
    payload["boundary"] = {
        "facts_invariant": True,
        "salary_estimate": "No salary number is emitted without current market evidence.",
        "missing_skills": "A missing match means no canonical evidence was found; it is not a claim that the person lacks the skill.",
    }
    return payload
