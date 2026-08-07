"""Interview, STAR-story, and architecture-talk projections."""

from __future__ import annotations

from typing import Any

from .platform_models import JobAnalysis, ReaderProfile


def build_star_library(graph_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Create evidence-bound STAR records from canonical proof entries."""

    method = graph_data.get("positioning", {}).get("method", [])
    action = "; ".join(str(item) for item in method[:4])
    stories: list[dict[str, Any]] = []
    for item in graph_data.get("proof", []):
        if not isinstance(item, dict):
            continue
        stories.append(
            {
                "id": f"star:{item.get('id', '')}",
                "title": str(item.get("label", "Evidence-backed result")),
                "situation": f"A consequential system required a verifiable outcome: {item.get('label', '')}.",
                "task": "Convert ambiguous requirements into a bounded, testable, reviewable artifact.",
                "action": action or "Observed the system, bounded authority, implemented the narrowest useful mechanism, and verified the result.",
                "result": str(item.get("claim", "")),
                "evidence_state": str(item.get("evidence_state", "UNSPECIFIED")),
                "source_id": str(item.get("id", "")),
                "boundary": "Narrative structure is generated; result language remains source-bound.",
            }
        )
    return stories


def build_interview_packet(
    graph_data: dict[str, Any],
    analysis: JobAnalysis,
    profile: ReaderProfile,
) -> dict[str, Any]:
    """Build a complete, role-targeted interview packet."""

    systems = [item for item in graph_data.get("selected_systems", []) if isinstance(item, dict)]
    architecture_talks = [
        {
            "system": str(item.get("name", "")),
            "opening": f"Frame {item.get('name', '')} by problem, constraints, authority boundary, implementation, verification, and unresolved limits.",
            "evidence": str(item.get("evidence", "")),
            "boundary": str(item.get("boundary", "")),
            "questions": [
                "What was the governing failure mode?",
                "Which tradeoffs were rejected and why?",
                "How was success verified?",
                "What remains unverified or intentionally out of scope?",
            ],
        }
        for item in systems
    ]
    behavioral = [
        {
            "prompt": "Tell me about a time you inherited ambiguity.",
            "answer_strategy": "Use the strongest source-bound STAR record; emphasize observation, scope, and proof.",
        },
        {
            "prompt": "Describe a conflict over technical direction.",
            "answer_strategy": "Separate facts, constraints, and decision criteria; avoid claiming people-management history not in the graph.",
        },
        {
            "prompt": "How do you handle failure?",
            "answer_strategy": "Explain fail-closed behavior, degraded modes, receipts, and explicit limits.",
        },
        {
            "prompt": "How do you influence without authority?",
            "answer_strategy": "Use interface contracts, evidence, shared decision criteria, and reversible implementation slices.",
        },
    ]
    return {
        "schema": "glaciereq.interview-packet.v1",
        "target_role": analysis.target_role,
        "reader_profile": profile.id,
        "decision_criteria": list(profile.decision_criteria),
        "star_stories": build_star_library(graph_data),
        "architecture_talks": architecture_talks,
        "system_design_topics": list(analysis.interview_topics),
        "behavioral_prompts": behavioral,
        "promotion_packet_outline": [
            "scope and operating context",
            "technical decisions and tradeoffs",
            "evidence of leverage",
            "risk reduced",
            "repeatable mechanisms created",
            "limits and next-level responsibilities",
        ],
        "boundary": "Generated prompts and structures do not add facts beyond the canonical graph.",
    }


def render_interview_markdown(packet: dict[str, Any]) -> str:
    """Render a readable interview packet."""

    lines = [f"# Interview Packet — {packet['target_role']}", ""]
    lines.extend(["## Decision Criteria", *[f"- {item}" for item in packet["decision_criteria"]], ""])
    lines.append("## STAR Story Library")
    for story in packet["star_stories"]:
        lines.extend(
            [
                "",
                f"### {story['title']}",
                f"- **Situation:** {story['situation']}",
                f"- **Task:** {story['task']}",
                f"- **Action:** {story['action']}",
                f"- **Result:** {story['result']}",
                f"- **Evidence state:** {story['evidence_state']}",
            ]
        )
    lines.extend(["", "## Architecture Talks"])
    for talk in packet["architecture_talks"]:
        lines.extend(["", f"### {talk['system']}", talk["opening"], f"Evidence: {talk['evidence']}"])
        lines.extend(f"- {question}" for question in talk["questions"])
    lines.extend(["", "## System Design Topics", *[f"- {item}" for item in packet["system_design_topics"]]])
    lines.extend(["", "## Behavioral Prompts"])
    for item in packet["behavioral_prompts"]:
        lines.extend([f"- **{item['prompt']}** {item['answer_strategy']}"])
    return "\n".join(lines).rstrip() + "\n"
