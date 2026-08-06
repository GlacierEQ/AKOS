"""Deterministic, evidence-preserving role targeting."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import dataclass
from typing import Any

from .models import CareerGraph, TargetProfile

_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9+#./-]{1,40}")
_STOP = {
    "about", "after", "also", "and", "are", "but", "can", "for", "from", "have", "into",
    "its", "more", "our", "that", "the", "their", "this", "through", "using", "with", "will",
    "you", "your", "years", "team", "work", "role", "job", "skills", "experience", "required",
    "preferred", "responsibilities", "qualifications",
}


@dataclass(frozen=True)
class TargetedView:
    target: TargetProfile
    keywords: tuple[str, ...]
    matched_capabilities: tuple[str, ...]
    matched_proof_ids: tuple[str, ...]
    score: int
    source_sha256: str


def _normalize(text: str) -> str:
    return text.casefold().strip(".,:;()[]{}")


def extract_keywords(text: str, limit: int) -> tuple[str, ...]:
    counter: Counter[str] = Counter()
    display: dict[str, str] = {}
    for token in _TOKEN.findall(text):
        normalized = _normalize(token)
        if len(normalized) < 2 or normalized in _STOP:
            continue
        counter[normalized] += 1
        display.setdefault(normalized, token)
    ranked = sorted(counter, key=lambda item: (-counter[item], item))[:limit]
    return tuple(display[item] for item in ranked)


def target_graph(graph: CareerGraph, target: TargetProfile) -> TargetedView:
    query = " ".join((target.role, target.audience, target.job_text)).strip()
    keywords = extract_keywords(query, target.max_keywords)
    keyword_set = {_normalize(item) for item in keywords}

    matched_capabilities: list[str] = []
    for values in graph.capabilities.values():
        for capability in values:
            terms = {_normalize(item) for item in _TOKEN.findall(capability)}
            if terms & keyword_set:
                matched_capabilities.append(capability)

    matched_proof_ids: list[str] = []
    for item in graph.proof:
        haystack = " ".join((str(item.get("label", "")), str(item.get("claim", ""))))
        terms = {_normalize(token) for token in _TOKEN.findall(haystack)}
        if terms & keyword_set:
            matched_proof_ids.append(str(item["id"]))

    score = min(100, len(set(matched_capabilities)) * 5 + len(set(matched_proof_ids)) * 10)
    return TargetedView(
        target=target,
        keywords=keywords,
        matched_capabilities=tuple(dict.fromkeys(matched_capabilities)),
        matched_proof_ids=tuple(dict.fromkeys(matched_proof_ids)),
        score=score,
        source_sha256=graph.source_sha256,
    )


def target_to_dict(view: TargetedView) -> dict[str, Any]:
    job_bytes = view.target.job_text.encode("utf-8")
    return {
        "target": {
            "role": view.target.role,
            "audience": view.target.audience,
            "max_keywords": view.target.max_keywords,
            "job_text_bytes": len(job_bytes),
            "job_text_sha256": hashlib.sha256(job_bytes).hexdigest(),
        },
        "keywords": list(view.keywords),
        "matched_capabilities": list(view.matched_capabilities),
        "matched_proof_ids": list(view.matched_proof_ids),
        "score": view.score,
        "source_sha256": view.source_sha256,
    }
