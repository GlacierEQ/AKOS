"""Transactional build and verification of career artifacts."""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .documents import render_docx, render_pdf, verify_docx, verify_pdf
from .io import (
    atomic_write_bytes,
    atomic_write_json,
    atomic_write_text,
    digest_json,
    load_graph,
    sha256_file,
)
from .models import CareerGraphError, TargetProfile
from .renderers import render_ats, render_css, render_html, render_json_ld, render_markdown
from .targeting import target_graph, target_to_dict
from .validation import validate_graph

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_OUTPUTS = {
    "canonical-source.json",
    "index.html",
    "resume.docx",
    "resume.md",
    "resume.pdf",
    "resume.schema.json",
    "resume.txt",
    "styles.css",
    "targeting.json",
}


@dataclass(frozen=True)
class BuildResult:
    output_dir: Path
    manifest_path: Path
    receipt_path: Path
    files: tuple[Path, ...]
    manifest_sha256: str
    build_id: str


def _safe_relative_path(value: object) -> PurePosixPath | None:
    if not isinstance(value, str) or not value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        return None
    return path


def _target_payload(view: Any) -> dict[str, Any] | None:
    return target_to_dict(view) if view is not None else None


def build_package(
    source: Path,
    output_dir: Path,
    *,
    target: TargetProfile | None = None,
) -> BuildResult:
    graph = load_graph(source)
    issues = validate_graph(graph)
    if issues:
        summary = "; ".join(f"{item.path}:{item.code}" for item in issues)
        raise CareerGraphError(f"career graph validation failed: {summary}")

    view = target_graph(graph, target or TargetProfile())
    parent = output_dir.parent
    parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.building-", dir=parent))
    try:
        ats = render_ats(graph, view)
        generated_text = {
            "canonical-source.json": json.dumps(
                graph.data, indent=2, ensure_ascii=False, sort_keys=True
            )
            + "\n",
            "index.html": render_html(graph, view),
            "resume.md": render_markdown(graph, view),
            "resume.schema.json": render_json_ld(graph),
            "resume.txt": ats,
            "styles.css": render_css(),
        }
        files: list[Path] = []
        for relative, content in generated_text.items():
            path = temporary / relative
            atomic_write_text(path, content)
            files.append(path)

        document_payloads = {
            "resume.docx": render_docx(
                ats,
                title=f"{graph.identity['display_name']} Resume",
                creator=graph.identity["name"],
            ),
            "resume.pdf": render_pdf(
                ats,
                title=f"{graph.identity['display_name']} Resume",
            ),
        }
        for relative, payload in document_payloads.items():
            path = temporary / relative
            atomic_write_bytes(path, payload)
            files.append(path)

        targeting_path = temporary / "targeting.json"
        atomic_write_json(targeting_path, target_to_dict(view))
        files.append(targeting_path)

        manifest_entries = [
            {
                "path": path.relative_to(temporary).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in sorted(files)
        ]
        manifest = {
            "schema": "glaciereq.career-package.v2",
            "source": {
                "path": source.as_posix(),
                "sha256": graph.source_sha256,
                "version": graph.data.get("version"),
                "status": graph.data.get("status"),
            },
            "target": target_to_dict(view),
            "files": manifest_entries,
            "policies": {
                "facts_invariant": True,
                "network_queries": 0,
                "external_actions": 0,
                "external_trackers": 0,
                "script_policy": "one application/ld+json script; no executable JavaScript",
            },
        }
        manifest_path = temporary / "manifest.json"
        atomic_write_json(manifest_path, manifest)
        manifest_hash = sha256_file(manifest_path)
        build_id = digest_json(
            {
                "source_sha256": graph.source_sha256,
                "target": _target_payload(view),
                "files": manifest_entries,
                "manifest_sha256": manifest_hash,
            }
        )
        receipt = {
            "schema": "glaciereq.career-build-receipt.v2",
            "state": "BUILT",
            "build_id": build_id,
            "source_sha256": graph.source_sha256,
            "manifest_sha256": manifest_hash,
            "manifest_digest": digest_json(manifest),
            "file_count": len(manifest_entries),
            "targeted": True,
            "network_queries": 0,
            "external_actions": 0,
            "non_claims": [
                "production deployment",
                "ATS-vendor acceptance",
                "accessibility certification",
                "recruiter response",
                "hiring outcome",
            ],
        }
        receipt_path = temporary / "receipt.json"
        atomic_write_json(receipt_path, receipt)

        verification = verify_package(temporary)
        if verification["state"] != "VERIFIED":
            raise CareerGraphError(
                "generated package verification failed: " + "; ".join(verification["errors"])
            )

        if output_dir.exists():
            if output_dir.is_dir():
                shutil.rmtree(output_dir)
            else:
                output_dir.unlink()
        os.replace(temporary, output_dir)
        return BuildResult(
            output_dir=output_dir,
            manifest_path=output_dir / "manifest.json",
            receipt_path=output_dir / "receipt.json",
            files=tuple(output_dir / item["path"] for item in manifest_entries),
            manifest_sha256=manifest_hash,
            build_id=build_id,
        )
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def verify_package(output_dir: Path) -> dict[str, Any]:
    manifest_path = output_dir / "manifest.json"
    receipt_path = output_dir / "receipt.json"
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"state": "FAILED", "errors": [f"package metadata unreadable: {exc}"]}
    if not isinstance(manifest, dict) or not isinstance(receipt, dict):
        return {"state": "FAILED", "errors": ["package metadata roots must be objects"]}
    if manifest.get("schema") != "glaciereq.career-package.v2":
        errors.append("unsupported manifest schema")
    if receipt.get("schema") != "glaciereq.career-build-receipt.v2":
        errors.append("unsupported receipt schema")

    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        errors.append("manifest files must be a non-empty list")
        entries = []
    declared_paths: set[str] = set()
    for index, item in enumerate(entries):
        if not isinstance(item, dict):
            errors.append(f"manifest file entry {index} must be an object")
            continue
        relative = _safe_relative_path(item.get("path"))
        if relative is None:
            errors.append(f"unsafe manifest path: {item.get('path')}")
            continue
        relative_text = relative.as_posix()
        if relative_text in declared_paths:
            errors.append(f"duplicate manifest path: {relative_text}")
            continue
        declared_paths.add(relative_text)
        path = output_dir.joinpath(*relative.parts)
        try:
            resolved = path.resolve(strict=False)
            resolved.relative_to(output_dir.resolve())
        except (OSError, ValueError):
            errors.append(f"manifest path escapes package: {relative_text}")
            continue
        if not path.is_file() or path.is_symlink():
            errors.append(f"missing or non-regular file: {relative_text}")
            continue
        expected_size = item.get("bytes")
        expected_hash = item.get("sha256")
        if not isinstance(expected_size, int) or expected_size < 0:
            errors.append(f"invalid size declaration: {relative_text}")
        elif path.stat().st_size != expected_size:
            errors.append(f"size mismatch: {relative_text}")
        if not isinstance(expected_hash, str) or not _HEX64.fullmatch(expected_hash):
            errors.append(f"invalid hash declaration: {relative_text}")
        elif sha256_file(path) != expected_hash:
            errors.append(f"hash mismatch: {relative_text}")

    missing_required = sorted(_REQUIRED_OUTPUTS - declared_paths)
    errors.extend(f"required output missing from manifest: {item}" for item in missing_required)

    manifest_hash = sha256_file(manifest_path) if manifest_path.is_file() else ""
    if receipt.get("manifest_sha256") != manifest_hash:
        errors.append("manifest hash mismatch in receipt")
    source_hash = receipt.get("source_sha256")
    if not isinstance(source_hash, str) or not _HEX64.fullmatch(source_hash):
        errors.append("receipt source hash is invalid")
    if receipt.get("network_queries") != 0 or receipt.get("external_actions") != 0:
        errors.append("receipt violates zero-network or zero-external-action contract")

    html_path = output_dir / "index.html"
    css_path = output_dir / "styles.css"
    docx_path = output_dir / "resume.docx"
    pdf_path = output_dir / "resume.pdf"
    html_text = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
    css_text = css_path.read_text(encoding="utf-8") if css_path.is_file() else ""
    docx_ok, docx_error = verify_docx(docx_path.read_bytes()) if docx_path.is_file() else (False, "missing DOCX")
    pdf_ok, pdf_error = verify_pdf(pdf_path.read_bytes()) if pdf_path.is_file() else (False, "missing PDF")
    forbidden_tracker_tokens = (
        "google-analytics",
        "googletagmanager",
        "segment.com",
        "mixpanel",
        "hotjar",
    )
    checks = {
        "semantic_main": '<main id="main">' in html_text,
        "skip_link": 'class="skip-link"' in html_text,
        "json_ld_only_script": html_text.count("<script") == 1
        and "application/ld+json" in html_text,
        "artifact_links": all(
            value in html_text for value in ("resume.pdf", "resume.docx", "resume.txt")
        ),
        "responsive_css": "@media (max-width: 760px)" in css_text and "clamp(" in css_text,
        "print_css": "@media print" in css_text,
        "focus_css": ":focus-visible" in css_text,
        "zero_trackers": not any(token in html_text.casefold() for token in forbidden_tracker_tokens),
        "docx_structure": docx_ok,
        "pdf_structure": pdf_ok,
    }
    if not docx_ok:
        errors.append(docx_error)
    if not pdf_ok:
        errors.append(pdf_error)
    errors.extend(f"failed check: {name}" for name, passed in checks.items() if not passed)

    expected_build_id = digest_json(
        {
            "source_sha256": receipt.get("source_sha256"),
            "target": manifest.get("target"),
            "files": entries,
            "manifest_sha256": manifest_hash,
        }
    )
    if receipt.get("build_id") != expected_build_id:
        errors.append("build id mismatch")
    return {
        "state": "VERIFIED" if not errors else "FAILED",
        "errors": errors,
        "checks": checks,
        "file_count": len(entries),
        "manifest_sha256": manifest_hash,
        "build_id": receipt.get("build_id"),
    }
