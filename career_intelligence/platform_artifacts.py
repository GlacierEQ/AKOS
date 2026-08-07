"""Human-readable career projections derived from one canonical graph."""

from __future__ import annotations

from typing import Any

from .personas import prioritize_proof, resolve_reader_profile


def markdown_resume(
    graph: dict[str, Any], *, role: str, profile_id: str, proof_limit: int, experience_limit: int
) -> str:
    identity = graph["identity"]
    proof = prioritize_proof(graph.get("proof", []), resolve_reader_profile(profile_id))[:proof_limit]
    lines = [
        f"# {identity['display_name']}",
        f"**{role}** · {identity['location']} · {identity['email']} · {identity['phone']}",
        "",
        str(graph["positioning"]["summary"]),
        "",
        "## Evidence-Backed Results",
    ]
    lines.extend(
        f"- **{item['label']}** — {item['claim']} [{item['evidence_state']}]" for item in proof
    )
    lines.extend(["", "## Experience"])
    for item in graph.get("experience", [])[:experience_limit]:
        end = item.get("end") or "Present"
        lines.extend(
            [
                f"### {item['role']} — {item['organization']}",
                f"{item['start']}–{end} · {item.get('location', '')}",
                *[f"- {value}" for value in item.get("highlights", [])],
                "",
            ]
        )
    lines.append("## Capabilities")
    for label, values in graph.get("capabilities", {}).items():
        lines.append(f"- **{label.replace('_', ' ').title()}:** {', '.join(values)}")
    lines.extend(["", "## Education"])
    lines.extend(f"- {item['program']} — {item['institution']}" for item in graph.get("education", []))
    lines.extend(
        [
            "",
            "## Evidence Boundary",
            "All claims are projections of the canonical career graph; no unsupported employer, metric, credential, affiliation, production status, or outcome is inferred.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def cover_letter(graph: dict[str, Any], *, role: str, company: str, proof_ids: tuple[str, ...]) -> str:
    identity = graph["identity"]
    by_id = {str(item.get("id")): item for item in graph.get("proof", [])}
    selected = [by_id[item] for item in proof_ids if item in by_id] or graph.get("proof", [])[:2]
    evidence = "\n".join(f"- {item['claim']}" for item in selected[:3])
    return (
        f"# Application for {role}\n\nHiring Team — {company or 'Target Organization'}\n\n"
        f"I am applying for the {role} opportunity. My work centers on turning ambiguous, high-consequence requirements into bounded systems with explicit authority, deterministic verification, and reviewable completion evidence.\n\n"
        f"The strongest directly supported examples are:\n{evidence}\n\n"
        "I would bring the same operating method to the role: inspect the actual system, separate evidence from inference, isolate the governing failure, build the narrowest useful mechanism, and expose limits rather than hide them.\n\n"
        f"Sincerely,\n{identity['display_name']}\n{identity['email']}\n"
    )


def profiles(graph: dict[str, Any], role: str) -> dict[str, str]:
    identity, positioning = graph["identity"], graph["positioning"]
    evidence = "\n".join(
        f"- {item['label']}: {item['claim']}" for item in graph.get("proof", [])[:4]
    )
    return {
        "linkedin.md": (
            f"# LinkedIn Profile — {identity['display_name']}\n\n## Headline\n{role} | Applied AI Systems | Evidence-Bound Execution | Agent Infrastructure\n\n"
            f"## About\n{positioning['summary']}\n\n## Featured Evidence\n{evidence}\n\n"
            "Boundary: no company affiliation, production use, or outcome is claimed beyond the canonical graph.\n"
        ),
        "github-profile.md": (
            f"# {identity['display_name']}\n\n> {positioning['headline']}\n\n## Current Focus\n- {role}\n"
            "- Evidence-bound agent infrastructure\n- Deterministic verification and release receipts\n- Human-machine artifact systems\n\n"
            f"## Verified / Recorded Work\n{evidence}\n\n## Operating Standard\nFacts before inference. Authority before action. Verification before completion.\n"
        ),
    }


def bios(graph: dict[str, Any], role: str) -> dict[str, str]:
    name = graph["identity"]["display_name"]
    return {
        "executive-bio.md": (
            f"# Executive Bio\n\n{name} is an applied AI systems architect and {role} focused on the operating layer between model capability and dependable outcomes. The work emphasizes explicit authority, bounded tools, deterministic evidence, controlled failure, and completion receipts.\n"
        ),
        "speaker-bio.md": (
            f"# Speaker Bio\n\n{name} builds evidence-bound AI and agent infrastructure. Talks focus on turning ambiguous requirements into typed contracts, fail-closed systems, verifiable artifacts, and honest operational boundaries.\n"
        ),
    }
