"""Normalized skill ontology and deterministic evidence matching."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

from .platform_models import SkillMatch, SkillRecord

_RESOURCE_DIR = Path(__file__).with_name("resources")
_DEFAULT_ONTOLOGY = _RESOURCE_DIR / "skill-ontology.v1.json"
_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9+#./-]*")


def normalize_term(value: str) -> str:
    """Normalize a skill term for alias matching."""

    return " ".join(value.casefold().replace("_", " ").replace("-", " ").split()).strip(" .,/+")


def load_skill_ontology(path: Path = _DEFAULT_ONTOLOGY) -> dict[str, SkillRecord]:
    """Load a versioned ontology. New nodes require no code changes."""

    data = json.loads(path.read_text(encoding="utf-8"))
    records: dict[str, SkillRecord] = {}
    defaults = data.get("defaults", {})
    default_seniority = tuple(str(value) for value in defaults.get("seniority_signals", []))
    default_evidence = tuple(str(value) for value in defaults.get("evidence_requirements", []))
    for item in data.get("skills", []):
        label = str(item["label"])
        record = SkillRecord(
            id=str(item["id"]),
            label=label,
            category=str(item["category"]),
            aliases=tuple(str(value) for value in item.get("aliases", [])),
            related=tuple(str(value) for value in item.get("related", [])),
            seniority_signals=tuple(str(value) for value in item.get("seniority_signals", default_seniority)),
            interview_topics=tuple(
                str(value)
                for value in item.get(
                    "interview_topics",
                    [
                        f"Explain a consequential {label} design decision",
                        f"Describe failure modes and verification for {label}",
                    ],
                )
            ),
            evidence_requirements=tuple(str(value) for value in item.get("evidence_requirements", default_evidence)),
        )
        records[record.id] = record
    return records


def alias_index(records: dict[str, SkillRecord]) -> dict[str, str]:
    """Map normalized aliases to canonical skill ids."""

    index: dict[str, str] = {}
    for record in records.values():
        for value in (record.id, record.label, *record.aliases):
            normalized = normalize_term(value)
            if normalized:
                index.setdefault(normalized, record.id)
    return index


def extract_requested_skills(
    text: str,
    records: dict[str, SkillRecord],
) -> tuple[str, ...]:
    """Extract only ontology-backed skill requests from arbitrary job text."""

    normalized_text = f" {normalize_term(text)} "
    tokens = {normalize_term(token) for token in _TOKEN.findall(text)}
    aliases = alias_index(records)
    found: set[str] = set()
    for alias, skill_id in aliases.items():
        if not alias:
            continue
        if " " in alias:
            if f" {alias} " in normalized_text:
                found.add(skill_id)
        elif alias in tokens:
            found.add(skill_id)
    return tuple(sorted(found))


def _flatten_graph_text(graph_data: dict[str, Any]) -> tuple[str, dict[str, str]]:
    fragments: list[str] = []
    evidence_text: dict[str, str] = {}

    capabilities = graph_data.get("capabilities", {})
    if isinstance(capabilities, dict):
        for values in capabilities.values():
            if isinstance(values, list):
                fragments.extend(str(value) for value in values)

    for item in graph_data.get("proof", []):
        if not isinstance(item, dict):
            continue
        evidence_id = str(item.get("id", ""))
        text = " ".join(str(item.get(key, "")) for key in ("label", "claim", "evidence_state"))
        evidence_text[evidence_id] = text
        fragments.append(text)

    for item in graph_data.get("selected_systems", []):
        if not isinstance(item, dict):
            continue
        evidence_id = f"system:{item.get('name', '')}"
        text = " ".join(str(item.get(key, "")) for key in ("name", "evidence", "boundary", "state"))
        evidence_text[evidence_id] = text
        fragments.append(text)

    for item in graph_data.get("experience", []):
        if not isinstance(item, dict):
            continue
        fragments.extend(str(value) for value in item.get("highlights", []) if isinstance(value, str))

    return " ".join(fragments), evidence_text


def match_skills_to_evidence(
    graph_data: dict[str, Any],
    skill_ids: Iterable[str],
    records: dict[str, SkillRecord],
) -> tuple[SkillMatch, ...]:
    """Bind requested skills to canonical proof and system records."""

    all_text, evidence_text = _flatten_graph_text(graph_data)
    normalized_all = f" {normalize_term(all_text)} "
    matches: list[SkillMatch] = []
    for skill_id in sorted(set(skill_ids)):
        record = records.get(skill_id)
        if record is None:
            continue
        aliases = tuple(sorted({normalize_term(value) for value in (record.id, record.label, *record.aliases)}))
        aliases = tuple(value for value in aliases if value)
        source_terms = tuple(alias for alias in aliases if f" {alias} " in normalized_all)
        evidence_ids = tuple(
            sorted(
                evidence_id
                for evidence_id, text in evidence_text.items()
                if any(f" {alias} " in f" {normalize_term(text)} " for alias in aliases)
            )
        )
        score = min(100, 20 * len(source_terms) + 15 * len(evidence_ids))
        matches.append(
            SkillMatch(
                skill_id=record.id,
                label=record.label,
                score=score,
                source_terms=source_terms,
                evidence_ids=evidence_ids,
            )
        )
    return tuple(sorted(matches, key=lambda item: (-item.score, item.label.casefold())))
