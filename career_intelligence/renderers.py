"""Deterministic resume and portfolio renderers."""

from __future__ import annotations

import html
import json

from .models import CareerGraph
from .targeting import TargetedView


def _period(start: str, end: str | None) -> str:
    return f"{start} – {end or 'Present'}"


def _selected_proof(graph: CareerGraph, view: TargetedView | None) -> list[dict]:
    if view is None or not view.matched_proof_ids:
        return graph.proof
    selected = [item for item in graph.proof if item["id"] in view.matched_proof_ids]
    remaining = [item for item in graph.proof if item["id"] not in view.matched_proof_ids]
    return selected + remaining


def render_ats(graph: CareerGraph, view: TargetedView | None = None) -> str:
    identity = graph.identity
    lines = [
        identity["display_name"].upper(),
        " | ".join(identity["role_labels"]),
        f"{identity['location']} | {identity['email']} | {identity.get('phone', '')}",
        f"Portfolio: {identity['portfolio']} | GitHub: {identity['github']}",
        "",
        "PROFESSIONAL SUMMARY",
        graph.positioning["summary"],
        "",
        "VERIFIED PROOF",
    ]
    for item in _selected_proof(graph, view):
        lines.append(f"- {item['label']}: {item['claim']} [{item['evidence_state']}]")

    lines.extend(["", "EXPERIENCE"])
    for item in graph.experience:
        lines.extend(
            [
                f"{item['role']} | {item['organization']} | "
                f"{_period(item['start'], item.get('end'))}",
                *[f"- {highlight}" for highlight in item["highlights"]],
                "",
            ]
        )

    lines.append("CAPABILITIES")
    for group, values in graph.capabilities.items():
        label = group.replace("_", " ").title()
        lines.append(f"{label}: {', '.join(values)}")

    lines.extend(["", "EDUCATION"])
    for item in graph.education:
        period = (
            _period(item.get("start", ""), item.get("end"))
            if item.get("start")
            else str(item.get("end", ""))
        )
        lines.append(f"{item['program']} | {item['institution']} | {period}")

    lines.extend(["", "EVIDENCE BOUNDARY"])
    lines.extend(f"- {item}" for item in graph.evidence_limits)
    return "\n".join(line.rstrip() for line in lines).strip() + "\n"


def render_markdown(graph: CareerGraph, view: TargetedView | None = None) -> str:
    identity = graph.identity
    out = [
        f"# {identity['display_name']}",
        "",
        f"**{' · '.join(identity['role_labels'])}**",
        "",
        f"{identity['location']} · [{identity['email']}](mailto:{identity['email']}) · "
        f"[Portfolio]({identity['portfolio']}) · [GitHub]({identity['github']})",
        "",
        f"> {graph.positioning['headline']}",
        "",
        graph.positioning["summary"],
        "",
        "## Proof",
        "",
    ]
    out.extend(
        f"- **{item['label']}** — {item['claim']} `[{item['evidence_state']}]`"
        for item in _selected_proof(graph, view)
    )
    out.extend(["", "## Experience", ""])
    for item in graph.experience:
        out.extend(
            [
                f"### {item['role']} — {item['organization']}",
                f"*{item['location']} · {_period(item['start'], item.get('end'))}*",
                "",
                *[f"- {highlight}" for highlight in item["highlights"]],
                "",
            ]
        )
    out.extend(["## Capabilities", ""])
    for group, values in graph.capabilities.items():
        out.append(f"- **{group.replace('_', ' ').title()}:** {', '.join(values)}")
    out.extend(["", "## Evidence boundary", ""])
    out.extend(f"- {item}" for item in graph.evidence_limits)
    return "\n".join(out).strip() + "\n"


def render_json_ld(graph: CareerGraph) -> str:
    identity = graph.identity
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": identity["name"],
        "alternateName": identity["display_name"],
        "email": identity["email"],
        "url": identity["portfolio"],
        "sameAs": [identity["github"]],
        "homeLocation": {"@type": "Place", "name": identity["location"]},
        "jobTitle": identity["role_labels"],
        "knowsAbout": sorted(
            {value for values in graph.capabilities.values() for value in values}
        ),
        "alumniOf": [
            {"@type": "EducationalOrganization", "name": item["institution"]}
            for item in graph.education
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def render_html(graph: CareerGraph, view: TargetedView | None = None) -> str:
    identity = graph.identity
    proof = _selected_proof(graph, view)

    def esc(value: object) -> str:
        return html.escape(str(value), quote=True)

    proof_cards = "".join(
        f'<article class="proof-card"><p class="eyebrow">{esc(item["evidence_state"])}</p>'
        f'<h3>{esc(item["label"])}</h3><p>{esc(item["claim"])}</p></article>'
        for item in proof
    )
    experience = "".join(
        f'<article class="experience"><header><div><h3>{esc(item["role"])}</h3>'
        f'<p>{esc(item["organization"])} · {esc(item["location"])}</p></div>'
        f'<time>{esc(_period(item["start"], item.get("end")))}</time></header><ul>'
        + "".join(f"<li>{esc(highlight)}</li>" for highlight in item["highlights"])
        + "</ul></article>"
        for item in graph.experience
    )
    capability_groups = "".join(
        f'<section class="capability"><h3>{esc(group.replace("_", " ").title())}</h3><p>'
        + " · ".join(esc(value) for value in values)
        + "</p></section>"
        for group, values in graph.capabilities.items()
    )
    limits = "".join(f"<li>{esc(item)}</li>" for item in graph.evidence_limits)
    json_ld = render_json_ld(graph).replace("</", "<\\/")
    target_note = ""
    if view is not None:
        target_note = (
            f'<p class="target-note">Target view: {esc(view.target.role)} · '
            f'{esc(view.target.audience)} · deterministic match score {view.score}/100</p>'
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(graph.positioning['summary'])}">
  <meta property="og:title" content="{esc(identity['display_name'])} — Applied AI Systems Architect">
  <meta property="og:description" content="{esc(graph.positioning['headline'])}">
  <meta property="og:type" content="profile">
  <title>{esc(identity['display_name'])} — Evidence-Bound Systems</title>
  <link rel="stylesheet" href="styles.css">
  <script type="application/ld+json">{json_ld}</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="hero">
    <nav aria-label="Primary">
      <a class="brand" href="#top">CB</a>
      <div><a href="#proof">Proof</a><a href="#experience">Experience</a><a href="#capabilities">Capabilities</a></div>
    </nav>
    <div id="top" class="hero-grid">
      <div>
        <p class="eyebrow">{' · '.join(esc(item) for item in identity['role_labels'])}</p>
        <h1>{esc(identity['display_name'])}</h1>
        <p class="lede">{esc(graph.positioning['headline'])}</p>
        <p class="summary">{esc(graph.positioning['summary'])}</p>
        {target_note}
        <div class="actions">
          <a class="button primary" href="resume.pdf">Download PDF</a>
          <a class="button" href="resume.docx">Download DOCX</a>
          <a class="button" href="resume.txt">ATS Text</a>
        </div>
      </div>
      <aside aria-label="Contact">
        <p>{esc(identity['location'])}</p>
        <a href="mailto:{esc(identity['email'])}">{esc(identity['email'])}</a>
        <a href="{esc(identity['github'])}">GitHub</a>
      </aside>
    </div>
  </header>
  <main id="main">
    <section id="proof" aria-labelledby="proof-heading"><div class="section-head"><p class="eyebrow">Receipts, not adjectives</p><h2 id="proof-heading">Verified proof</h2></div><div class="proof-grid">{proof_cards}</div></section>
    <section id="experience" aria-labelledby="experience-heading"><div class="section-head"><p class="eyebrow">Operating history</p><h2 id="experience-heading">Experience</h2></div>{experience}</section>
    <section id="capabilities" aria-labelledby="capabilities-heading"><div class="section-head"><p class="eyebrow">Technical surface</p><h2 id="capabilities-heading">Capabilities</h2></div><div class="capability-grid">{capability_groups}</div></section>
    <section class="boundary" aria-labelledby="boundary-heading"><h2 id="boundary-heading">Evidence boundary</h2><ul>{limits}</ul></section>
  </main>
  <footer><p>Canonical source SHA-256: <code>{graph.source_sha256}</code></p></footer>
</body>
</html>
"""


def render_css() -> str:
    return """:root {
  --ink: #111827;
  --muted: #596174;
  --paper: #f7f7f3;
  --panel: #ffffff;
  --line: #d8dadd;
  --accent: #0f766e;
  --accent-dark: #115e59;
  --max: 1180px;
  --space: clamp(1rem, 2vw, 2rem);
  color-scheme: light;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--paper); color: var(--ink); line-height: 1.6; }
a { color: inherit; text-underline-offset: .2em; }
a:focus-visible { outline: 3px solid var(--accent); outline-offset: 4px; }
.skip-link { position: fixed; left: 1rem; top: -5rem; z-index: 100; padding: .75rem 1rem; background: var(--ink); color: white; }
.skip-link:focus { top: 1rem; }
.hero { padding: 1rem var(--space) clamp(3rem, 8vw, 7rem); background: var(--ink); color: white; }
nav { max-width: var(--max); margin: 0 auto clamp(3rem, 8vw, 7rem); display: flex; justify-content: space-between; align-items: center; }
nav div { display: flex; gap: 1rem; flex-wrap: wrap; }
.brand { display: grid; place-items: center; width: 2.75rem; height: 2.75rem; border: 1px solid #ffffff55; border-radius: 50%; text-decoration: none; font-weight: 800; }
.hero-grid { max-width: var(--max); margin: 0 auto; display: grid; grid-template-columns: minmax(0, 1fr) minmax(14rem, 22rem); gap: clamp(2rem, 7vw, 7rem); align-items: end; }
h1 { margin: .2rem 0 1rem; font-size: clamp(3rem, 10vw, 7.5rem); letter-spacing: -.065em; line-height: .9; max-width: 10ch; }
h2 { margin: 0; font-size: clamp(2rem, 5vw, 4rem); letter-spacing: -.04em; line-height: 1; }
h3 { margin: 0; line-height: 1.2; }
.eyebrow { margin: 0 0 .75rem; text-transform: uppercase; letter-spacing: .13em; font-size: .76rem; font-weight: 800; color: #73d8ce; }
.lede { max-width: 24ch; font-size: clamp(1.25rem, 2.4vw, 2rem); line-height: 1.25; }
.summary { max-width: 68ch; color: #d7dce5; }
.hero aside { padding: 1.25rem; border: 1px solid #ffffff2d; display: grid; gap: .5rem; }
.hero aside p { margin: 0; }
.actions { display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 2rem; }
.button { display: inline-flex; padding: .78rem 1rem; border: 1px solid #ffffff55; text-decoration: none; font-weight: 750; }
.button.primary { background: #fff; color: var(--ink); }
.target-note { border-left: 3px solid #73d8ce; padding-left: 1rem; color: #d7dce5; }
main { max-width: var(--max); margin: 0 auto; padding: clamp(3rem, 8vw, 7rem) var(--space); }
main > section { margin-bottom: clamp(4rem, 9vw, 8rem); }
.section-head { display: grid; grid-template-columns: minmax(10rem, .45fr) 1fr; gap: 2rem; align-items: end; margin-bottom: 2rem; }
.section-head .eyebrow, .proof-card .eyebrow { color: var(--accent-dark); }
.proof-grid, .capability-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
.proof-card, .capability { background: var(--panel); border: 1px solid var(--line); padding: clamp(1.25rem, 3vw, 2rem); }
.experience { padding: 2rem 0; border-top: 1px solid var(--line); }
.experience header { display: flex; justify-content: space-between; gap: 2rem; }
.experience header p { margin: .4rem 0 0; color: var(--muted); }
.experience time { white-space: nowrap; font-weight: 700; }
.experience li { margin-block: .6rem; }
.boundary { background: #e7ebe9; padding: clamp(1.5rem, 4vw, 3rem); }
footer { padding: 2rem var(--space); border-top: 1px solid var(--line); color: var(--muted); overflow-wrap: anywhere; }
footer p { max-width: var(--max); margin: 0 auto; }
@media (max-width: 760px) {
  .hero-grid, .section-head, .proof-grid, .capability-grid { grid-template-columns: 1fr; }
  .experience header { display: grid; gap: .5rem; }
  nav div { display: none; }
}
@media print {
  nav, .actions, .skip-link { display: none !important; }
  body, .hero { background: white; color: black; }
  .hero { padding-bottom: 2rem; }
  .summary, .eyebrow { color: black; }
  main { padding-top: 2rem; }
  a { text-decoration: none; }
}
"""
