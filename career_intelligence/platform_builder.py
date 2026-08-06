"""Transactional Infinity Gauntlet v2 career-platform build."""

from __future__ import annotations

import json
import shutil
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Iterable

from .ats import score_ats_text
from .interview import build_interview_packet, render_interview_markdown
from .io import atomic_write_json, atomic_write_text, digest_json, load_graph, sha256_file
from .job_intelligence import analyze_job, job_analysis_to_dict
from .models import CareerGraphError, TargetProfile
from .persona_council import run_persona_council
from .personas import resolve_reader_profile
from .platform_artifacts import bios, cover_letter, markdown_resume, profiles
from .platform_common import VARIANTS, publish_directory, write_deterministic_zip
from .platform_models import PlatformBuildResult
from .platform_verify import verify_career_platform
from .portfolio import write_portfolio_site
from .resources_index import build_resource_index
from .skill_ontology import load_skill_ontology

ResumeBuilder = Callable[..., Any]
ResumeVerifier = Callable[[Path], dict[str, Any]]


def _default_builder() -> ResumeBuilder:
    from .builder import build_package

    return build_package


def _default_verifier() -> ResumeVerifier:
    from .builder import verify_package

    return verify_package


def _json(path: Path, payload: Any) -> Path:
    atomic_write_json(path, payload)
    return path


def _text(path: Path, payload: str) -> Path:
    atomic_write_text(path, payload)
    return path


def build_career_platform(
    source: Path,
    output_dir: Path,
    *,
    target_role: str,
    audience: str = "principal-engineer",
    job_text: str = "",
    company: str = "",
    local_resources: Iterable[Path] = (),
    resource_catalog: dict[str, Any] | None = None,
    resume_builder: ResumeBuilder | None = None,
    resume_verifier: ResumeVerifier | None = None,
) -> PlatformBuildResult:
    """Build every career projection from one evidence-bound graph."""

    if not target_role.strip():
        raise CareerGraphError("target role must be non-empty")
    if output_dir.is_symlink():
        raise CareerGraphError("refusing to replace symlink output directory")

    graph = load_graph(source)
    profile = resolve_reader_profile(audience or target_role)
    analysis = analyze_job(
        graph.data,
        target_role=target_role,
        audience=profile.id,
        job_text=job_text,
        reader_profile=profile,
    )
    analysis_payload = job_analysis_to_dict(analysis)
    ontology = load_skill_ontology()
    builder, verifier = resume_builder or _default_builder(), resume_verifier or _default_verifier()

    output_dir = output_dir.resolve()
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.building-", dir=output_dir.parent))
    try:
        files: list[Path] = [
            _json(temporary / "canonical/career-graph.json", graph.data),
            _json(temporary / "analysis/job-analysis.json", analysis_payload),
            _json(
                temporary / "analysis/gap-analysis.json",
                {
                    "schema": "glaciereq.career-gap-analysis.v1",
                    "target_role": target_role,
                    "matched_skills": [asdict(item) for item in analysis.matched_skills],
                    "missing_skill_ids": list(analysis.missing_skill_ids),
                    "boundary": "Missing means no matching canonical evidence was found; it is not a claim of absence.",
                },
            ),
            _json(temporary / "analysis/reader-profile.json", asdict(profile)),
            _json(
                temporary / "analysis/skill-evidence-map.json",
                {
                    "requested": [asdict(ontology[item]) for item in analysis.requested_skill_ids],
                    "matches": [asdict(item) for item in analysis.matched_skills],
                },
            ),
        ]

        for variant, variant_audience in VARIANTS.items():
            variant_dir = temporary / "resumes" / variant
            result = builder(
                source,
                variant_dir,
                target=TargetProfile(
                    role=target_role,
                    audience=variant_audience,
                    job_text=job_text,
                    max_keywords=36,
                ),
            )
            if verifier(result.output_dir).get("state") != "VERIFIED":
                raise CareerGraphError(f"resume variant failed verification: {variant}")
            files.extend(path for path in variant_dir.rglob("*") if path.is_file())

        files.extend(
            [
                _text(
                    temporary / "resumes/one-page.md",
                    markdown_resume(
                        graph.data,
                        role=target_role,
                        profile_id=profile.id,
                        proof_limit=3,
                        experience_limit=2,
                    ),
                ),
                _text(
                    temporary / "resumes/two-page.md",
                    markdown_resume(
                        graph.data,
                        role=target_role,
                        profile_id=profile.id,
                        proof_limit=6,
                        experience_limit=6,
                    ),
                ),
            ]
        )
        for name, content in profiles(graph.data, target_role).items():
            files.append(_text(temporary / "profiles" / name, content))
        for name, content in bios(graph.data, target_role).items():
            files.append(_text(temporary / "bios" / name, content))
        files.append(
            _text(
                temporary / "letters/cover-letter.md",
                cover_letter(
                    graph.data,
                    role=target_role,
                    company=company,
                    proof_ids=analysis.matched_proof_ids,
                ),
            )
        )

        packet = build_interview_packet(graph.data, analysis, profile)
        files.extend(
            [
                _json(temporary / "interview/interview-packet.json", packet),
                _text(
                    temporary / "interview/interview-packet.md",
                    render_interview_markdown(packet),
                ),
                _json(temporary / "interview/star-library.json", packet["star_stories"]),
            ]
        )

        try:
            ats_text = (temporary / "resumes/ats/resume.txt").read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise CareerGraphError(f"failed to read ATS resume for scoring: {exc}") from exc
        ats_report = score_ats_text(ats_text, analysis)
        boundaries = {
            "schema": "glaciereq.career-platform-boundaries.v1",
            "facts_invariant": True,
            "network_queries": 0,
            "external_writes": 0,
            "non_claims": [
                "production deployment",
                "ATS-vendor acceptance",
                "accessibility certification",
                "current salary estimate without live market data",
                "recruiter response",
                "hiring outcome",
            ],
        }
        files.extend(
            [
                _json(temporary / "reports/ats-report.json", ats_report),
                _json(temporary / "reports/platform-boundaries.json", boundaries),
                _json(
                    temporary / "resources/resource-index.json",
                    build_resource_index(
                        graph.data,
                        local_paths=local_resources,
                        catalog=resource_catalog,
                    ),
                ),
            ]
        )

        portfolio_paths = write_portfolio_site(
            temporary / "portfolio", graph.data, analysis, profile, ontology
        )
        analytics = _json(
            temporary / "portfolio/analytics-policy.json",
            {
                "schema": "glaciereq.portfolio-analytics-policy.v1",
                "state": "DISABLED_BY_DEFAULT",
                "external_trackers": 0,
                "permitted_future_mode": "explicitly enabled, privacy-preserving, first-party aggregate analytics",
                "boundary": "This build performs no analytics collection or external telemetry.",
            },
        )
        portfolio_paths.append(analytics)
        files.extend(portfolio_paths)

        council = run_persona_council(
            graph.data,
            target_role=target_role,
            job_analysis=analysis_payload,
            ats_report=ats_report,
            portfolio_reports={
                "accessibility": json.loads(
                    (temporary / "portfolio/accessibility-report.json").read_text(encoding="utf-8")
                ),
                "seo": json.loads(
                    (temporary / "portfolio/seo-report.json").read_text(encoding="utf-8")
                ),
            },
        )
        if council["state"] != "PASSED":
            raise CareerGraphError("persona council reported blocking findings")
        files.append(_json(temporary / "analysis/persona-council.json", council))

        portfolio_zip = temporary / "archives/portfolio.zip"
        write_deterministic_zip(portfolio_zip, temporary / "portfolio", portfolio_paths)
        files.append(portfolio_zip)

        unique = sorted(
            {path.resolve() for path in files},
            key=lambda path: path.relative_to(temporary).as_posix(),
        )
        entries = [
            {
                "path": path.relative_to(temporary).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in unique
        ]
        manifest = {
            "schema": "glaciereq.career-intelligence-platform.v2",
            "version": "2.0.0",
            "source": {
                "path": source.as_posix(),
                "sha256": graph.source_sha256,
                "version": graph.data.get("version"),
                "status": graph.data.get("status"),
            },
            "target": {
                "role": target_role,
                "audience": profile.id,
                "company": company,
                "job_text_sha256": analysis.job_text_sha256,
            },
            "variants": dict(VARIANTS),
            "files": entries,
            "policies": boundaries,
        }
        manifest_path = temporary / "manifest.json"
        atomic_write_json(manifest_path, manifest)
        manifest_sha = sha256_file(manifest_path)

        bundle = temporary / "archives/deployment-bundle.zip"
        write_deterministic_zip(bundle, temporary, [*unique, manifest_path])
        bundle_sha = sha256_file(bundle)
        build_id = digest_json(
            {
                "source_sha256": graph.source_sha256,
                "target": manifest["target"],
                "manifest_sha256": manifest_sha,
                "bundle_sha256": bundle_sha,
            }
        )
        receipt_path = temporary / "receipt.json"
        atomic_write_json(
            receipt_path,
            {
                "schema": "glaciereq.career-platform-receipt.v2",
                "state": "BUILT",
                "build_id": build_id,
                "source_sha256": graph.source_sha256,
                "manifest_sha256": manifest_sha,
                "deployment_bundle_sha256": bundle_sha,
                "declared_file_count": len(entries),
                "network_queries": 0,
                "external_writes": 0,
                "facts_invariant": True,
                "non_claims": boundaries["non_claims"],
            },
        )
        verification = verify_career_platform(temporary, resume_verifier=verifier)
        if verification["state"] != "VERIFIED":
            raise CareerGraphError(
                "career platform verification failed: "
                + ("; ".join(verification["errors"]) or json.dumps(verification["checks"], sort_keys=True))
            )
        publish_directory(temporary, output_dir)
        return PlatformBuildResult(
            output_dir=output_dir,
            manifest_path=output_dir / "manifest.json",
            receipt_path=output_dir / "receipt.json",
            deployment_bundle_path=output_dir / "archives/deployment-bundle.zip",
            build_id=build_id,
            manifest_sha256=manifest_sha,
            bundle_sha256=bundle_sha,
            files=tuple(output_dir / entry["path"] for entry in entries),
        )
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


__all__ = ["build_career_platform", "verify_career_platform"]
