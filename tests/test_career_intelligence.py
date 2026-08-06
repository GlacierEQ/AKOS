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
    first_pdf = render_pdf(text, title="Casey Barton Resume", author="Casey Barton")
    second_pdf = render_pdf(text, title="Casey Barton Resume", author="Casey Barton")
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


def test_validator_requires_renderer_fields_and_education_shape(tmp_path: Path) -> None:
    graph = json.loads(SOURCE.read_text(encoding="utf-8"))
    graph["proof"][0].pop("label")
    graph["experience"][0].pop("location")
    graph["education"][0].pop("institution")
    path = tmp_path / "invalid-renderer-fields.json"
    atomic_write_json(path, graph)
    issues = validate_graph(load_graph(path))
    codes = {(item.path, item.code) for item in issues}
    assert ("proof[0].label", "REQUIRED") in codes
    assert ("experience[0].location", "REQUIRED") in codes
    assert ("education[0].institution", "REQUIRED") in codes


def test_validator_rejects_unsafe_identity_urls(tmp_path: Path) -> None:
    graph = json.loads(SOURCE.read_text(encoding="utf-8"))
    graph["identity"]["github"] = "javascript:alert(1)"
    graph["identity"]["portfolio"] = "https://user:secret@example.com/"
    path = tmp_path / "unsafe-urls.json"
    atomic_write_json(path, graph)
    issues = validate_graph(load_graph(path))
    codes = {(item.path, item.code) for item in issues}
    assert ("identity.github", "URL") in codes
    assert ("identity.portfolio", "URL") in codes


def test_markdown_includes_canonical_education() -> None:
    from career_intelligence.renderers import render_markdown

    graph = load_graph(SOURCE)
    markdown = render_markdown(graph)
    assert "## Education" in markdown
    assert all(item["institution"] in markdown for item in graph.education)


def test_json_ld_script_escapes_case_insensitive_terminators(tmp_path: Path) -> None:
    graph_data = json.loads(SOURCE.read_text(encoding="utf-8"))
    graph_data["identity"]["display_name"] = "payload </SCRIPT><script>alert(1)</script>"
    path = tmp_path / "script-payload.json"
    atomic_write_json(path, graph_data)
    graph = load_graph(path)
    page = render_html(graph)
    assert "</SCRIPT>" not in page
    assert "<script>alert(1)</script>" not in page
    assert "\\u003c/SCRIPT\\u003e" in page
    assert page.count("<script") == 1


def test_target_contract_binds_job_text_digest() -> None:
    from career_intelligence.targeting import target_to_dict

    graph = load_graph(SOURCE)
    first = target_to_dict(target_graph(graph, TargetProfile(job_text="Python MCP")))
    second = target_to_dict(target_graph(graph, TargetProfile(job_text="Python MCP.")))
    assert first["target"]["job_text_sha256"] != second["target"]["job_text_sha256"]
    assert first["target"]["job_text_bytes"] == len("Python MCP".encode("utf-8"))


def test_proof_matching_uses_normalized_token_boundaries() -> None:
    graph = load_graph(SOURCE)
    punctuation = target_graph(graph, TargetProfile(job_text="CI/CD."))
    plain = target_graph(graph, TargetProfile(job_text="CI/CD"))
    assert punctuation.matched_proof_ids == plain.matched_proof_ids
    false_positive = target_graph(graph, TargetProfile(job_text="ai"))
    assert "proof-agent-coordinator" not in false_positive.matched_proof_ids


def test_pdf_metadata_uses_source_author() -> None:
    payload = render_pdf("ADA LOVELACE\n", title="Resume", author="Ada Lovelace")
    assert b"/Author (Ada Lovelace)" in payload
    assert b"/Author (Casey Barton)" not in payload


def test_verifier_rejects_executable_or_remote_scripts() -> None:
    from career_intelligence.builder import _has_only_json_ld_script

    assert _has_only_json_ld_script(
        '<script type="application/ld+json">{"name":"Casey"}</script>'
    )
    assert not _has_only_json_ld_script(
        '<script>alert(1)</script><p>application/ld+json</p>'
    )
    assert not _has_only_json_ld_script(
        '<script type="application/ld+json" src="https://example.com/data.js"></script>'
    )


def test_invalid_utf8_artifacts_return_failed(tmp_path: Path) -> None:
    output = tmp_path / "package"
    build_package(SOURCE, output)
    (output / "index.html").write_bytes(b"\xff\xfe")
    verification = verify_package(output)
    assert verification["state"] == "FAILED"
    assert any("HTML artifact unreadable" in error for error in verification["errors"])


def test_undeclared_files_are_rejected(tmp_path: Path) -> None:
    output = tmp_path / "package"
    build_package(SOURCE, output)
    (output / "untracked.js").write_text("alert(1)", encoding="utf-8")
    verification = verify_package(output)
    assert verification["state"] == "FAILED"
    assert "undeclared package file: untracked.js" in verification["errors"]


def test_failed_publication_restores_previous_package(tmp_path: Path, monkeypatch) -> None:
    import career_intelligence.builder as builder_module

    output = tmp_path / "package"
    original = build_package(SOURCE, output)
    previous_manifest = original.manifest_sha256
    real_replace = builder_module.os.replace
    calls = 0

    def fail_install(source, destination):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated install failure")
        return real_replace(source, destination)

    monkeypatch.setattr(builder_module.os, "replace", fail_install)
    try:
        build_package(SOURCE, output, target=TargetProfile(role="Different role"))
    except OSError as exc:
        assert "simulated install failure" in str(exc)
    else:
        raise AssertionError("publication failure was not raised")

    assert output.is_dir()
    assert sha256_file(output / "manifest.json") == previous_manifest
    assert verify_package(output)["state"] == "VERIFIED"


def test_validator_checks_selected_systems_and_cross_domain_foundation(tmp_path: Path) -> None:
    graph = json.loads(SOURCE.read_text(encoding="utf-8"))
    graph["selected_systems"][0].pop("boundary")
    graph["cross_domain_foundation"][0].pop("record")
    path = tmp_path / "invalid-secondary-records.json"
    atomic_write_json(path, graph)
    issues = validate_graph(load_graph(path))
    codes = {(item.path, item.code) for item in issues}
    assert ("selected_systems[0].boundary", "REQUIRED") in codes
    assert ("cross_domain_foundation[0].record", "REQUIRED") in codes
