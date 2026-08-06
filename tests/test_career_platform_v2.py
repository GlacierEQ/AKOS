from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pytest

from career_intelligence.job_intelligence import analyze_job, job_analysis_to_dict
from career_intelligence.persona_council import run_persona_council
from career_intelligence.personas import load_reader_profiles, resolve_reader_profile
from career_intelligence.platform_builder import build_career_platform, verify_career_platform
from career_intelligence.resources_index import build_resource_index
from career_intelligence.skill_ontology import alias_index, extract_requested_skills, load_skill_ontology


@pytest.fixture()
def graph_data() -> dict[str, object]:
    return {
        "schema": "test.career.v1",
        "version": "1.0.0",
        "status": "TEST",
        "identity": {
            "name": "Casey Example",
            "display_name": "Casey Example",
            "location": "Honolulu, Hawaii",
            "phone": "+1-808-555-0100",
            "email": "casey@example.com",
            "portfolio": "https://example.com/",
            "github": "https://github.com/example",
        },
        "positioning": {
            "headline": "Evidence-bound systems.",
            "summary": "Builds deterministic Python and TypeScript agent infrastructure.",
            "method": ["observe", "bound authority", "build", "verify"],
        },
        "proof": [{
            "id": "proof-runtime",
            "label": "Agent Runtime",
            "evidence_state": "TEST_VERIFIED",
            "claim": "24 of 24 tests passed for a deterministic Python runtime with CI/CD receipts.",
            "metrics": {"tests_passed": 24, "tests_total": 24},
        }],
        "experience": [{
            "organization": "Example Systems",
            "role": "Applied AI Systems Builder",
            "location": "Honolulu, Hawaii",
            "start": "2025",
            "end": None,
            "highlights": ["Built Python, TypeScript, MCP, GitHub Actions, Docker, and Postgres systems."],
        }],
        "capabilities": {"primary_technology": ["Python", "TypeScript", "MCP", "GitHub Actions", "Docker", "Postgres"]},
        "selected_systems": [{"name": "Agent Runtime", "state": "TEST_VERIFIED", "evidence": "24/24 tests.", "boundary": "No production claim."}],
        "education": [{"institution": "University of Hawaii", "program": "Bachelor of Science"}],
        "artifacts": [],
        "evidence_limits": ["No production claim."],
    }


@pytest.fixture()
def source(tmp_path: Path, graph_data: dict[str, object]) -> Path:
    path = tmp_path / "career.json"
    path.write_text(json.dumps(graph_data), encoding="utf-8")
    return path


@dataclass
class FakeBuild:
    output_dir: Path


def fake_resume_builder(source: Path, output_dir: Path, *, target: object) -> FakeBuild:
    output_dir.mkdir(parents=True, exist_ok=True)
    text = "Casey Example\ncasey@example.com\n8085550100\n\nEXPERIENCE\nApplied AI Systems Builder\n\nSKILLS\nPython TypeScript MCP GitHub Actions Docker Postgres\n\nEDUCATION\nBachelor of Science\n" + "x" * 600
    payloads = {
        "resume.txt": text,
        "resume.md": "# Casey Example\n",
        "index.html": "<!doctype html><html><body>Casey Example</body></html>",
        "styles.css": "body{font-family:sans-serif}",
        "resume.schema.json": "{}\n",
        "canonical-source.json": source.read_text(encoding="utf-8"),
        "targeting.json": json.dumps({"target": str(target)}) + "\n",
        "resume.docx": "fake-docx",
        "resume.pdf": "%PDF-fake",
        "manifest.json": "{}\n",
        "receipt.json": "{}\n",
    }
    for name, value in payloads.items():
        path = output_dir / name
        if name.endswith((".docx", ".pdf")):
            path.write_bytes(value.encode())
        else:
            path.write_text(value, encoding="utf-8")
    return FakeBuild(output_dir)


def fake_resume_verifier(output_dir: Path) -> dict[str, object]:
    ok = (output_dir / "resume.txt").is_file() and (output_dir / "resume.pdf").is_file()
    return {"state": "VERIFIED" if ok else "FAILED"}


def test_resources_cover_reader_skill_and_connector_contracts(graph_data: dict[str, object], tmp_path: Path) -> None:
    profiles = load_reader_profiles()
    ontology = load_skill_ontology()
    aliases = alias_index(ontology)
    assert {"principal-engineer", "cto", "technical-recruiter", "government-reviewer", "startup-founder"} <= profiles.keys()
    assert resolve_reader_profile("Principal Engineer").id == "principal-engineer"
    assert aliases["py"] == "python" and aliases["postgresql"] == "postgres"
    assert {"python", "postgres", "cicd"} <= set(extract_requested_skills("Py PostgreSQL CI/CD", ontology))
    evidence = tmp_path / "evidence.txt"
    evidence.write_text("evidence", encoding="utf-8")
    index = build_resource_index(graph_data, local_paths=[evidence])
    assert index["local_resources"][0]["state"] == "INDEXED_LOCAL"
    assert index["execution"] == {"live_connector_queries": 0, "external_writes": 0, "authorization_required": True}


def test_job_analysis_is_evidence_bound(graph_data: dict[str, object]) -> None:
    result = job_analysis_to_dict(analyze_job(graph_data, target_role="Principal AI Engineer", audience="principal-engineer", job_text="Python TypeScript MCP Kubernetes"))
    assert "python" in result["requested_skill_ids"]
    assert "kubernetes" in result["missing_skill_ids"]
    assert result["salary_market_state"] == "UNAVAILABLE_WITHOUT_LIVE_MARKET_DATA"


def test_persona_council_runs_all_experts(graph_data: dict[str, object]) -> None:
    report = run_persona_council(
        graph_data,
        target_role="Principal Engineer",
        job_analysis={"missing_skill_ids": []},
        ats_report={"common_checks": {"structure": True}},
        portfolio_reports={"accessibility": {"checks": {"semantic_landmarks": True}}, "seo": {"checks": {"open_graph": True}}},
    )
    assert report["state"] == "PASSED" and len(report["passes"]) == 15


def build(source: Path, output: Path):
    return build_career_platform(
        source,
        output,
        target_role="Principal AI Systems Engineer",
        audience="principal-engineer",
        job_text="Python TypeScript MCP Kubernetes",
        company="Example Corp",
        resume_builder=fake_resume_builder,
        resume_verifier=fake_resume_verifier,
    )


def test_platform_build_is_complete_verified_and_deterministic(source: Path, tmp_path: Path) -> None:
    first = build(source, tmp_path / "one")
    second = build(source, tmp_path / "two")
    verification = verify_career_platform(first.output_dir, resume_verifier=fake_resume_verifier)
    assert verification["state"] == "VERIFIED"
    assert first.manifest_sha256 == second.manifest_sha256
    assert first.bundle_sha256 == second.bundle_sha256
    assert first.build_id == second.build_id
    assert (first.output_dir / "portfolio/manifest.webmanifest").is_file()
    assert all(verification["resume_variants"].values())


def test_platform_verifier_detects_tampering_and_undeclared_files(source: Path, tmp_path: Path) -> None:
    output = tmp_path / "platform"
    build(source, output)
    (output / "profiles/linkedin.md").write_text("tampered", encoding="utf-8")
    assert verify_career_platform(output, resume_verifier=fake_resume_verifier)["state"] == "FAILED"
    output.unlink(missing_ok=True) if output.is_file() else None

    clean = tmp_path / "clean"
    build(source, clean)
    (clean / "extra.txt").write_text("unexpected", encoding="utf-8")
    result = verify_career_platform(clean, resume_verifier=fake_resume_verifier)
    assert result["state"] == "FAILED" and result["checks"]["no_undeclared_files"] is False


def test_output_symlink_is_rejected(source: Path, tmp_path: Path) -> None:
    real = tmp_path / "real"
    real.mkdir()
    output = tmp_path / "platform"
    output.symlink_to(real, target_is_directory=True)
    with pytest.raises(Exception, match="symlink"):
        build(source, output)


def test_resource_index_marks_mid_read_failure_unavailable(
    graph_data: dict[str, object], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import career_intelligence.resources_index as resource_module

    evidence = tmp_path / "evidence.txt"
    evidence.write_text("evidence", encoding="utf-8")
    monkeypatch.setattr(resource_module, "sha256_file", lambda _: (_ for _ in ()).throw(OSError("gone")))
    record = build_resource_index(graph_data, local_paths=[evidence])["local_resources"][0]
    assert record["state"] == "UNAVAILABLE"
    assert record["reason"] == "file became inaccessible during indexing"


def test_missing_ats_projection_returns_clear_build_error(source: Path, tmp_path: Path) -> None:
    def missing_ats_builder(source: Path, output_dir: Path, *, target: object) -> FakeBuild:
        result = fake_resume_builder(source, output_dir, target=target)
        (output_dir / "resume.txt").unlink()
        return result

    with pytest.raises(Exception, match="failed to read ATS resume for scoring"):
        build_career_platform(
            source,
            tmp_path / "platform",
            target_role="Principal Engineer",
            resume_builder=missing_ats_builder,
            resume_verifier=lambda _: {"state": "VERIFIED"},
        )
