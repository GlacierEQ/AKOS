from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

from career_intelligence.builder import build_package, verify_package
from career_intelligence.documents import render_docx, render_pdf, verify_docx, verify_pdf
from career_intelligence.io import atomic_write_json, load_graph, sha256_bytes, sha256_file
from career_intelligence.models import TargetProfile
from career_intelligence.renderers import render_ats, render_css, render_html
from career_intelligence.targeting import extract_keywords, target_graph
from career_intelligence.validation import validate_graph

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "career_intelligence/resources/casey-barton.career-runtime.v1.json"


def test_canonical_graph_is_valid() -> None:
    graph = load_graph(SOURCE)
    assert validate_graph(graph) == ()


def test_targeting_is_deterministic_and_source_bound() -> None:
    graph = load_graph(SOURCE)
    target = TargetProfile(
        role="Principal AI Systems Engineer",
        job_text="Python agent infrastructure governance evidence CI/CD MCP",
    )
    first = target_graph(graph, target)
    second = target_graph(graph, target)
    assert first == second
    assert first.source_sha256 == graph.source_sha256
    assert "Python" in first.matched_capabilities


def test_keyword_extraction_has_stable_order() -> None:
    assert extract_keywords("Python Python Rust evidence evidence evidence", 3) == (
        "evidence",
        "Python",
        "Rust",
    )


def test_renderers_preserve_evidence_boundaries() -> None:
    graph = load_graph(SOURCE)
    ats = render_ats(graph)
    page = render_html(graph)
    assert "EVIDENCE BOUNDARY" in ats
    assert all(limit in ats for limit in graph.evidence_limits)
    assert "Evidence boundary" in page
    assert page.count("<script") == 1
    assert "application/ld+json" in page


def test_css_has_responsive_print_and_focus_contracts() -> None:
    css = render_css()
    assert "clamp(" in css
    assert "@media (max-width: 760px)" in css
    assert "@media print" in css
    assert ":focus-visible" in css


def test_documents_are_deterministic_and_structurally_valid() -> None:
    text = "CASEY BARTON\n\nPROFESSIONAL SUMMARY\nEvidence-bound systems.\n"
    first_docx = render_docx(text, title="Casey Barton Resume", creator="Casey Barton")
    second_docx = render_docx(text, title="Casey Barton Resume", creator="Casey Barton")
    first_pdf = render_pdf(text, title="Casey Barton Resume")
    second_pdf = render_pdf(text, title="Casey Barton Resume")
    assert first_docx == second_docx
    assert first_pdf == second_pdf
    assert verify_docx(first_docx) == (True, "")
    assert verify_pdf(first_pdf) == (True, "")
    with zipfile.ZipFile(io.BytesIO(first_docx)) as archive:
        assert "word/document.xml" in archive.namelist()


def test_full_build_is_verified_and_repeatable(tmp_path: Path) -> None:
    first = build_package(
        SOURCE,
        tmp_path / "first",
        target=TargetProfile(role="Staff AI Engineer"),
    )
    second = build_package(
        SOURCE,
        tmp_path / "second",
        target=TargetProfile(role="Staff AI Engineer"),
    )
    first_verification = verify_package(first.output_dir)
    second_verification = verify_package(second.output_dir)
    assert first_verification["state"] == "VERIFIED"
    assert second_verification["state"] == "VERIFIED"
    assert first.build_id == second.build_id
    assert first.manifest_sha256 == second.manifest_sha256
    for name in ("resume.pdf", "resume.docx", "resume.txt", "index.html"):
        assert sha256_file(first.output_dir / name) == sha256_file(second.output_dir / name)


def test_generated_documents_have_expected_signatures(tmp_path: Path) -> None:
    result = build_package(SOURCE, tmp_path / "package")
    docx = (result.output_dir / "resume.docx").read_bytes()
    pdf = (result.output_dir / "resume.pdf").read_bytes()
    assert docx.startswith(b"PK")
    assert pdf.startswith(b"%PDF-1.4")
    assert sha256_bytes(docx) == sha256_file(result.output_dir / "resume.docx")
    assert sha256_bytes(pdf) == sha256_file(result.output_dir / "resume.pdf")


def test_tampering_is_detected(tmp_path: Path) -> None:
    output = tmp_path / "package"
    build_package(SOURCE, output)
    (output / "resume.txt").write_text("tampered", encoding="utf-8")
    verification = verify_package(output)
    assert verification["state"] == "FAILED"
    assert any("resume.txt" in error for error in verification["errors"])


def test_malformed_manifest_fails_without_raising(tmp_path: Path) -> None:
    output = tmp_path / "package"
    build_package(SOURCE, output)
    (output / "manifest.json").write_text("[]", encoding="utf-8")
    verification = verify_package(output)
    assert verification["state"] == "FAILED"
    assert verification["errors"]


def test_path_traversal_is_rejected(tmp_path: Path) -> None:
    output = tmp_path / "package"
    build_package(SOURCE, output)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    manifest["files"][0]["path"] = "../escape"
    atomic_write_json(output / "manifest.json", manifest)
    verification = verify_package(output)
    assert verification["state"] == "FAILED"
    assert any("unsafe manifest path" in error for error in verification["errors"])


def test_invalid_graph_returns_specific_issues(tmp_path: Path) -> None:
    graph = json.loads(SOURCE.read_text(encoding="utf-8"))
    graph["identity"]["name"] = ""
    graph["artifacts"][0]["sha256"] = "not-a-hash"
    path = tmp_path / "invalid.json"
    atomic_write_json(path, graph)
    issues = validate_graph(load_graph(path))
    codes = {(item.path, item.code) for item in issues}
    assert ("identity.name", "REQUIRED") in codes
    assert ("artifacts[0].sha256", "HASH") in codes
