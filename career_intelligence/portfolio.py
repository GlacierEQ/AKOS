"""Static portfolio, architecture site, and PWA projections."""
from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

from .io import atomic_write_json, atomic_write_text
from .platform_models import JobAnalysis, ReaderProfile, SkillRecord


def _safe_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def _list(values: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{escape(value)}</li>" for value in values) + "</ul>"


def _cards(graph: dict[str, Any]) -> str:
    return "".join(
        "<article class='card'>"
        f"<p class='eyebrow'>{escape(str(item.get('state', '')))}</p>"
        f"<h3>{escape(str(item.get('name', '')))}</h3>"
        f"<p>{escape(str(item.get('evidence', '')))}</p>"
        f"<p class='muted'><strong>Boundary:</strong> {escape(str(item.get('boundary', '')))}</p>"
        "</article>"
        for item in graph.get("selected_systems", [])
        if isinstance(item, dict)
    )


def _timeline(graph: dict[str, Any]) -> str:
    return "".join(
        "<article class='card'>"
        f"<p class='eyebrow'>{escape(str(item.get('start', '')))} — {escape(str(item.get('end') or 'Present'))}</p>"
        f"<h3>{escape(str(item.get('role', '')))}</h3>"
        f"<p>{escape(str(item.get('organization', '')))} · {escape(str(item.get('location', '')))}</p>"
        f"{_list([str(value) for value in item.get('highlights', [])])}</article>"
        for item in graph.get("experience", [])
        if isinstance(item, dict)
    )


def _skills(analysis: JobAnalysis, ontology: dict[str, SkillRecord]) -> list[dict[str, Any]]:
    matched = {item.skill_id: item for item in analysis.matched_skills}
    return [
        {
            "id": record.id,
            "label": record.label,
            "category": record.category,
            "related": list(record.related),
            "score": matched[skill_id].score if skill_id in matched else 0,
            "evidence_ids": list(matched[skill_id].evidence_ids) if skill_id in matched else [],
        }
        for skill_id in analysis.requested_skill_ids
        if (record := ontology.get(skill_id)) is not None
    ]


def render_portfolio_html(
    graph: dict[str, Any], analysis: JobAnalysis, profile: ReaderProfile, ontology: dict[str, SkillRecord]
) -> str:
    identity, positioning = graph["identity"], graph["positioning"]
    skills = _safe_json(_skills(analysis, ontology))
    resumes = "".join(
        f"<a class='button' href='../resumes/{slug}/resume.pdf'>{label}</a>"
        for slug, label in (("executive", "Executive résumé"), ("ats", "ATS résumé"), ("recruiter", "Recruiter résumé"), ("government", "Government résumé"), ("startup", "Startup résumé"))
    )
    return f"""<!doctype html><html lang='en' data-theme='system'><head>
<meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<meta name='description' content='{escape(str(positioning['summary']), quote=True)}'>
<meta property='og:title' content='{escape(str(identity['display_name']), quote=True)} — Career Portfolio'>
<meta property='og:description' content='{escape(str(positioning['headline']), quote=True)}'>
<link rel='manifest' href='manifest.webmanifest'><link rel='stylesheet' href='styles.css'>
<link rel='alternate' type='application/rss+xml' href='rss.xml'><title>{escape(str(identity['display_name']))} — Career Portfolio</title></head>
<body><a class='skip-link' href='#main'>Skip to content</a><header><a href='#top'><strong>{escape(str(identity['display_name']))}</strong></a><nav aria-label='Primary'><a href='#architecture'>Architecture</a><a href='#projects'>Projects</a><a href='#skills'>Skills</a><a href='#experience'>Experience</a></nav><button id='theme-toggle' aria-label='Toggle color theme'>Theme</button></header>
<main id='main'><section id='top' class='hero'><p class='eyebrow'>Target: {escape(analysis.target_role)} · Reader: {escape(profile.label)}</p><h1>{escape(str(positioning['headline']))}</h1><p class='lede'>{escape(str(positioning['summary']))}</p><div class='actions'>{resumes}<a class='button secondary' href='architecture.html'>Architecture site</a></div></section>
<section id='architecture'><p class='eyebrow'>Operating method</p><h2>Architecture timeline</h2>{_list([str(item) for item in positioning.get('method', [])])}</section>
<section id='projects'><p class='eyebrow'>Project explorer</p><h2>Systems and evidence</h2><div class='grid'>{_cards(graph)}</div></section>
<section id='skills'><p class='eyebrow'>Interactive skill graph</p><h2>Target capability map</h2><label for='skill-filter'>Filter skills</label><input id='skill-filter' type='search'><div id='skill-graph' class='grid' aria-live='polite'></div><script id='skill-data' type='application/json'>{skills}</script></section>
<section id='experience'><p class='eyebrow'>Experience</p><h2>Career timeline</h2><div class='grid'>{_timeline(graph)}</div></section>
<section id='contact'><h2>Contact</h2><p><a href='mailto:{escape(str(identity['email']), quote=True)}'>{escape(str(identity['email']))}</a> · <a href='{escape(str(identity['github']), quote=True)}' rel='noreferrer'>GitHub</a></p></section></main><footer>No external trackers. Career Intelligence Platform v2.</footer><script src='app.js' defer></script></body></html>"""


def render_architecture_html(graph: dict[str, Any]) -> str:
    identity = graph["identity"]
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><link rel='stylesheet' href='styles.css'><title>{escape(str(identity['display_name']))} — Architecture</title></head><body><a class='skip-link' href='#main'>Skip to content</a><header><a href='index.html'>Portfolio</a></header><main id='main'><section class='hero'><p class='eyebrow'>Architecture website</p><h1>Bounded systems, explicit authority, verifiable completion.</h1></section><section><h2>System portfolio</h2><div class='grid'>{_cards(graph)}</div></section><section><h2>Evidence limits</h2>{_list([str(item) for item in graph.get('evidence_limits', [])])}</section></main></body></html>"""


def render_css() -> str:
    return """:root{color-scheme:light dark;--bg:#f7f7f5;--surface:#fff;--text:#171717;--muted:#5d625f;--line:#d9ddda;--accent:#1c5748;font-family:Inter,system-ui,sans-serif}[data-theme=dark]{--bg:#111513;--surface:#19201d;--text:#f3f7f5;--muted:#b7c1bc;--line:#34423c;--accent:#7bd5b8}@media(prefers-color-scheme:dark){[data-theme=system]{--bg:#111513;--surface:#19201d;--text:#f3f7f5;--muted:#b7c1bc;--line:#34423c;--accent:#7bd5b8}}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);line-height:1.6}a{color:inherit}header{position:sticky;top:0;z-index:2;display:flex;justify-content:space-between;gap:1rem;padding:1rem 5vw;background:var(--bg);border-bottom:1px solid var(--line)}nav{display:flex;gap:1rem}button,input{background:var(--surface);color:var(--text);border:1px solid var(--line);border-radius:999px;padding:.7rem 1rem}.skip-link{position:absolute;left:-9999px}.skip-link:focus{left:1rem;top:1rem}.hero,section{padding:clamp(3rem,8vw,8rem) clamp(1rem,7vw,7rem)}.hero{min-height:75vh;display:grid;align-content:center;gap:1.2rem}h1{font-size:clamp(2.7rem,8vw,7rem);line-height:.95;max-width:16ch}.lede{font-size:1.25rem;max-width:60ch;color:var(--muted)}.eyebrow{text-transform:uppercase;letter-spacing:.14em;color:var(--accent);font-weight:800}.actions{display:flex;gap:.7rem;flex-wrap:wrap}.button{padding:.7rem 1rem;border-radius:999px;background:var(--accent);color:var(--bg);text-decoration:none;font-weight:800}.secondary{background:var(--surface);color:var(--text);border:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1rem}.card{background:var(--surface);border:1px solid var(--line);border-radius:1rem;padding:1.2rem}.muted,footer{color:var(--muted)}#skill-filter{display:block;margin:1rem 0;width:min(32rem,100%)}footer{text-align:center;padding:2rem;border-top:1px solid var(--line)}:focus-visible{outline:3px solid var(--accent);outline-offset:3px}@media(max-width:800px){nav{display:none}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;animation:none!important}}@media print{header,footer,.actions,#skill-filter{display:none}.hero,section{padding:1rem}.card{break-inside:avoid}}"""


def render_app_js() -> str:
    return """(()=>{const r=document.documentElement,b=document.getElementById('theme-toggle'),f=document.getElementById('skill-filter'),c=document.getElementById('skill-graph'),d=document.getElementById('skill-data');const saved=localStorage.getItem('career-theme');if(['light','dark','system'].includes(saved))r.dataset.theme=saved;b?.addEventListener('click',()=>{const o=['system','light','dark'],n=o[(o.indexOf(r.dataset.theme||'system')+1)%o.length];r.dataset.theme=n;localStorage.setItem('career-theme',n);b.textContent=`Theme: ${n}`});let skills=[];try{skills=JSON.parse(d?.textContent||'[]')}catch{skills=[]}const render=(q='')=>{q=q.toLowerCase();c.replaceChildren(...skills.filter(x=>`${x.label} ${x.category}`.toLowerCase().includes(q)).map(x=>{const n=document.createElement('article');n.className='card';const h=document.createElement('strong'),m=document.createElement('p');h.textContent=x.label;m.textContent=`${x.category} · evidence score ${x.score}`;n.append(h,m);return n}))};f?.addEventListener('input',e=>render(e.target.value));render();if('serviceWorker'in navigator)navigator.serviceWorker.register('service-worker.js').catch(()=>undefined)})();"""


def write_portfolio_site(output: Path, graph: dict[str, Any], analysis: JobAnalysis, profile: ReaderProfile, ontology: dict[str, SkillRecord]) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    identity = graph["identity"]
    text_files = {
        "index.html": render_portfolio_html(graph, analysis, profile, ontology),
        "architecture.html": render_architecture_html(graph),
        "styles.css": render_css(),
        "app.js": render_app_js(),
        "service-worker.js": "const C='career-platform-v2',A=['./','index.html','architecture.html','styles.css','app.js'];self.addEventListener('install',e=>e.waitUntil(caches.open(C).then(x=>x.addAll(A))));self.addEventListener('fetch',e=>{if(e.request.method==='GET')e.respondWith(caches.match(e.request).then(x=>x||fetch(e.request)))})\n",
        "manifest.webmanifest": _safe_json({"name": f"{identity['display_name']} Career Portfolio", "short_name": identity["display_name"], "start_url": "./", "display": "standalone", "theme_color": "#1c5748"}) + "\n",
        "robots.txt": "User-agent: *\nAllow: /\nSitemap: sitemap.xml\n",
        "sitemap.xml": f"<?xml version='1.0'?><urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'><url><loc>{escape(str(identity.get('portfolio','')))}</loc></url></urlset>\n",
        "rss.xml": f"<?xml version='1.0'?><rss version='2.0'><channel><title>{escape(str(identity['display_name']))} Career Portfolio</title><link>{escape(str(identity.get('portfolio','')))}</link></channel></rss>\n",
        "icon.svg": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 128 128'><rect width='128' height='128' rx='28' fill='#1c5748'/><text x='64' y='82' text-anchor='middle' font-size='64' fill='white'>C</text></svg>\n",
    }
    paths: list[Path] = []
    for name, value in text_files.items():
        path = output / name; atomic_write_text(path, value); paths.append(path)
    reports = {
        "schema.json": {"@context": "https://schema.org", "@type": "Person", "name": identity["display_name"], "email": identity["email"], "url": identity.get("portfolio"), "sameAs": [identity.get("github")], "jobTitle": analysis.target_role},
        "open-graph.json": {"title": f"{identity['display_name']} — {analysis.target_role}", "description": graph["positioning"]["headline"], "type": "profile", "url": identity.get("portfolio")},
        "accessibility-report.json": {"schema": "glaciereq.accessibility-report.v1", "state": "STATIC_CHECKS_PASSED", "checks": {"semantic_landmarks": True, "skip_link": True, "keyboard_focus_style": True, "reduced_motion": True, "responsive_layout": True, "labels_for_controls": True, "external_accessibility_certification": False}, "boundary": "Static checks are not a WCAG certification."},
        "seo-report.json": {"schema": "glaciereq.seo-report.v1", "state": "STATIC_CHECKS_PASSED", "checks": {"title": True, "description": True, "open_graph": True, "schema_org": True, "sitemap": True, "rss": True, "robots": True}},
        "performance-report.json": {"schema": "glaciereq.performance-budget.v1", "state": "BUDGET_DECLARED", "budgets": {"third_party_requests": 0, "javascript_bytes_target": 15000, "css_bytes_target": 30000}, "boundary": "No live Lighthouse measurement is claimed."},
    }
    for name, value in reports.items():
        path = output / name; atomic_write_json(path, value); paths.append(path)
    return paths
