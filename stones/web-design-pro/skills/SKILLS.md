# Web Design Pro Skills

## Operating Principle

The website is not a decorated résumé. It is a reversible set of human and machine projections over one canonical fact, evidence, repository, and capability graph.

Every design decision must improve at least one of these outcomes without degrading the others:

- comprehension;
- orientation;
- decision quality;
- proof accessibility;
- accessibility;
- performance;
- privacy;
- reconstructability.

## 1. Recruiter Information Architecture

Answer role, value, strongest proof, differentiation, and next-action questions in the first review screen. Place deeper evidence behind progressive disclosure rather than forcing every reader through the complete technical ledger.

The first screen must distinguish:

- what Casey does;
- why it matters;
- which systems prove it;
- what is verified versus bounded;
- where to inspect next.

## 2. Multidimensional Experience Architecture

Model the site as a navigable experience graph rather than a sequence of disconnected pages.

Supported projections include:

- hierarchical trees;
- repository constellations;
- capability graphs;
- company bottleneck maps;
- system architecture diagrams;
- timelines and evolution paths;
- evidence and provenance chains;
- comparison matrices;
- guided narratives;
- machine-readable records.

Each projection must identify its source nodes, filters, policy overlays, freshness, and fallback representation.

## 3. Hierarchical Routing and Clever Interlinking

Every node should lead naturally upward, downward, and sideways:

```text
company ↔ bottleneck ↔ capability ↔ flagship ↔ repository ↔ proof
   ↕           ↕             ↕            ↕           ↕
 role      domain model   reusable skill  donor map  receipt
```

Use stable identifiers and typed relationships rather than hand-authored link sprawl. Breadcrumbs, related-node panels, backlinks, search, and deep links must derive from the graph.

## 4. Graph and Mind-Map Design

Use graph visualization when relationships are the subject, not as decoration.

Requirements:

- progressive loading for large graphs;
- semantic node labels and edge types;
- deterministic filtering and layout inputs;
- focus-plus-context interaction;
- keyboard traversal;
- textual adjacency list or table fallback;
- shareable filtered state;
- visible scope and freshness;
- no implication that visual proximity proves causation or runtime integration.

## 5. Data Visualization and Chart Selection

Select visual forms by question:

- trend → line or area;
- composition → stacked bars or treemap when area comparison is valid;
- comparison → bars, dot plots, or matrices;
- flow → Sankey only when quantity is real and supportable;
- dependency → directed graph;
- hierarchy → tree, sunburst, or indented table;
- state transition → state machine;
- chronology → timeline;
- uncertainty → ranges, confidence bands, or explicit labels.

Never invent quantitative precision. If values are ordinal, use ordinal representation. If evidence is categorical, do not fabricate a numeric score merely to enable a chart.

## 6. Animation and Motion Grammar

Motion must explain one of four things:

1. state change;
2. causal sequence;
3. spatial relationship;
4. focus transition.

Define reusable motion tokens for duration, easing, distance, staging, and interruption. All motion must:

- honor `prefers-reduced-motion`;
- remain understandable when disabled;
- avoid blocking input;
- preserve focus;
- avoid vestibular-risk patterns;
- operate within a performance budget.

## 7. Interactive Explanation Design

Interactive explainers should let the user manipulate a real model rather than watch a prewritten spectacle.

Good examples:

- reveal how one canonical fact generates several audience projections;
- filter repository nodes by domain, evidence, ownership, or company relevance;
- step through a release receipt from source to deployment;
- compare alternative system boundaries and their tradeoffs;
- trace a capability from bottleneck to donor repo to implemented flagship.

Every explainer requires an equivalent static narrative and downloadable machine representation.

## 8. Design Token Engineering

Define typography, spacing, radii, surfaces, borders, accents, states, layers, motion, data colors, chart semantics, and responsive breakpoints as machine-readable tokens. Do not scatter unexplained values across components.

Tokens must separate:

- brand identity;
- semantic state;
- evidence state;
- visualization category;
- interaction feedback.

Color must never be the sole carrier of state or evidence.

## 9. Responsive Systems, Not Responsive Screenshots

Use mobile-first flow, readable line lengths, flexible grids, container-aware components, and content-order invariants.

Complex graphs and diagrams need responsive transformation rules:

- wide graph → filtered focus view;
- matrix → scrollable table with anchored labels;
- constellation → searchable node list;
- dense timeline → segmented eras;
- multi-column comparison → stacked comparison with preserved headings.

Reflow must not hide evidence states or separate labels from their claims.

## 10. Semantic HTML Architecture

Use landmarks, headings, lists, links, buttons, dialogs, tables, details/summary, figures, captions, and form controls according to meaning.

The page must remain understandable without CSS and without JavaScript. Custom widgets require explicit keyboard, focus, label, state, and fallback contracts.

## 11. Accessibility-First Design

Check:

- keyboard navigation;
- focus visibility and order;
- semantic names, roles, and states;
- contrast;
- zoom and text spacing;
- responsive reflow;
- reduced motion;
- descriptive links;
- meaning independent of color;
- chart descriptions;
- graph alternatives;
- error recovery;
- touch targets;
- print and export behavior.

A limited audit is evidence of the audit scope, not accessibility certification.

## 12. PSYSOC-X Presentation Calibration

PSYSOC-X may adapt order, density, disclosure depth, terminology, skepticism response, and memory anchors using explicit audience and decision context.

It may not:

- alter facts;
- promote evidence;
- infer hidden traits;
- exploit vulnerability;
- conceal material limitations;
- replace user-controlled navigation with coercive sequencing.

## 13. Dynamic Resource and Standards Discovery

Do not freeze moving browsers, frameworks, connector inventories, company targets, repositories, or role families into permanent arrays.

At activation:

1. discover current official standards and platform capabilities;
2. record source, version/date, retrieval time, and hash where possible;
3. select only resources relevant to the current implementation;
4. cache them as an observation snapshot;
5. apply explicit policy overlays;
6. refresh when the snapshot exceeds its freshness rule or a source changes.

Hard-code only stable schemas, safety rules, authority boundaries, and validation invariants.

## 14. SEO, Social, and Machine Discovery

Publish canonical URL, concise descriptions, structured titles, Open Graph metadata, robots policy, sitemap, JSON-LD where truthful, and machine routes without inventing authority or affiliation.

The machine surface should expose stable identifiers and relationships for:

- people;
- roles;
- companies;
- bottlenecks;
- capabilities;
- systems;
- repositories;
- evidence;
- artifacts;
- releases.

## 15. Progressive Enhancement and Bounded Client Runtime

Static HTML and CSS remain the semantic baseline. Client behavior is allowed when it creates a bounded benefit that cannot be delivered as clearly through native semantics alone.

Every script-bearing feature must declare:

- user benefit;
- data dependencies;
- privacy impact;
- performance budget;
- accessibility behavior;
- offline/failure behavior;
- no-script fallback;
- test plan;
- removal path.

## 16. Performance and Perceptual Latency

Budget the experience by route and interaction, not only by total bundle size.

Track:

- initial HTML and CSS;
- critical fonts and images;
- JavaScript by capability;
- graph/data payloads;
- hydration or initialization cost;
- interaction latency;
- layout shift;
- memory use on mobile;
- cache behavior.

Load depth on demand. The first useful answer should not wait for the complete repository universe.

## 17. Privacy and Public-Surface Safety

Every public projection must pass an allowlist-based privacy policy. Graph traversal, search, generated backlinks, previews, and machine APIs can expose sensitive paths even when the primary page does not.

Validate the unauthenticated public surface, not merely the intended navigation.

## 18. Static and Dynamic Release Verification

Verify source, preview, and production separately.

Required checks include:

- canonical routes;
- deep links and filtered states;
- artifact downloads and hashes;
- content types;
- source commit and build identity;
- redirects;
- error routes;
- security headers;
- scripts and trackers;
- accessibility gates;
- responsive behavior;
- graph/table equivalence;
- reduced-motion behavior;
- freshness markers;
- production reconstruction from the release source.

## 19. Website-as-Library Architecture

Each domain Stone may publish a web-facing knowledge package containing:

- operating mentality;
- core laws;
- skills;
- tools;
- connectors;
- authoritative resource discovery rules;
- examples;
- tests;
- failure modes;
- reusable prompts;
- visualizations;
- proof references.

The website renders these packages as a connected academy. The Stone remains the source contract; the site is its explorable projection.

## 20. Final Quality Gate

A multidimensional feature is admitted only when:

- it answers a real user question;
- its source data is identified;
- its state is reproducible;
- its fallback preserves meaning;
- it passes accessibility and reduced-motion gates;
- it respects privacy and authority;
- it remains within performance budget;
- it cannot overstate evidence;
- it materially improves the experience over a simpler representation.
