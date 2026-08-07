"""Typed contracts for the Career Intelligence Platform v2."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReaderProfile:
    """Explicit audience model used to prioritize presentation, never to manipulate."""

    id: str
    label: str
    attention_budget_words: int
    skepticism: str
    preferred_metrics: tuple[str, ...]
    preferred_language: tuple[str, ...]
    risk_tolerance: str
    decision_criteria: tuple[str, ...]
    artifact_priority: tuple[str, ...]


@dataclass(frozen=True)
class SkillRecord:
    """One normalized skill node with aliases and evidence expectations."""

    id: str
    label: str
    category: str
    aliases: tuple[str, ...]
    related: tuple[str, ...]
    seniority_signals: tuple[str, ...]
    interview_topics: tuple[str, ...]
    evidence_requirements: tuple[str, ...]


@dataclass(frozen=True)
class SkillMatch:
    """Deterministic mapping between a requested skill and canonical evidence."""

    skill_id: str
    label: str
    score: int
    source_terms: tuple[str, ...]
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class JobAnalysis:
    """Evidence-bound analysis of a target role or supplied job description."""

    target_role: str
    audience_id: str
    job_text_sha256: str
    requested_skill_ids: tuple[str, ...]
    matched_skills: tuple[SkillMatch, ...]
    missing_skill_ids: tuple[str, ...]
    matched_proof_ids: tuple[str, ...]
    interview_topics: tuple[str, ...]
    salary_market_state: str


@dataclass(frozen=True)
class PlatformBuildResult:
    """Completed Career Intelligence Platform build."""

    output_dir: Path
    manifest_path: Path
    receipt_path: Path
    deployment_bundle_path: Path
    build_id: str
    manifest_sha256: str
    bundle_sha256: str
    files: tuple[Path, ...]


JsonObject = dict[str, Any]
