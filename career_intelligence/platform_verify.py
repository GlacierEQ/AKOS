"""Fail-closed verification for Career Intelligence Platform v2."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Any, Callable

from .io import sha256_file
from .platform_common import REQUIRED_PLATFORM_FILES, VARIANTS, safe_relative_path

ResumeVerifier = Callable[[Path], dict[str, Any]]


def _default_verifier() -> ResumeVerifier:
    from .builder import verify_package

    return verify_package


def verify_career_platform(
    output_dir: Path, *, resume_verifier: ResumeVerifier | None = None
) -> dict[str, Any]:
    errors: list[str] = []
    checks: dict[str, bool] = {}
    root = output_dir.resolve()
    verifier = resume_verifier or _default_verifier()
    manifest_path, receipt_path = root / "manifest.json", root / "receipt.json"
    bundle_path = root / "archives/deployment-bundle.zip"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"state": "FAILED", "checks": {"metadata_readable": False}, "errors": [f"metadata unreadable: {exc}"]}

    entries = manifest.get("files")
    checks["manifest_shape"] = manifest.get("schema") == "glaciereq.career-intelligence-platform.v2" and isinstance(entries, list) and bool(entries)
    if not checks["manifest_shape"]:
        errors.append("invalid platform manifest")
        entries = []

    declared: set[str] = set()
    paths_safe = hashes_valid = files_match = True
    for entry in entries:
        if not isinstance(entry, dict):
            hashes_valid = False
            continue
        relative = safe_relative_path(entry.get("path"))
        if relative is None or relative.as_posix() in declared:
            paths_safe = False
            continue
        name = relative.as_posix()
        declared.add(name)
        path = root / relative
        try:
            inside = path.resolve().is_relative_to(root)
        except (OSError, RuntimeError):
            inside = False
        if not inside or path.is_symlink():
            paths_safe = False
            continue
        expected = entry.get("sha256")
        if not isinstance(expected, str) or len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
            hashes_valid = False
            continue
        if not path.is_file() or path.stat().st_size != entry.get("bytes") or sha256_file(path) != expected:
            files_match = False
    checks.update(paths_safe=paths_safe, hash_contract=hashes_valid, declared_files_match=files_match)
    if not paths_safe:
        errors.append("unsafe or duplicate manifest path")
    if not hashes_valid:
        errors.append("invalid manifest hash contract")
    if not files_match:
        errors.append("missing or modified declared file")

    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink()
    }
    extras = {"manifest.json", "receipt.json", "archives/deployment-bundle.zip"}
    checks["no_undeclared_files"] = actual == declared | extras
    checks["required_platform_files"] = REQUIRED_PLATFORM_FILES <= declared
    if not checks["no_undeclared_files"]:
        errors.append("undeclared or missing package files")
    if not checks["required_platform_files"]:
        errors.append("required platform output is missing")

    resume_checks = {
        variant: verifier(root / "resumes" / variant).get("state") == "VERIFIED"
        for variant in VARIANTS
    }
    checks["resume_variants_verified"] = all(resume_checks.values())
    if not checks["resume_variants_verified"]:
        errors.append("one or more resume variants failed verification")

    try:
        html = (root / "portfolio/index.html").read_text(encoding="utf-8")
        app = (root / "portfolio/app.js").read_text(encoding="utf-8")
        combined = (html + app).casefold()
        checks["portfolio_no_trackers"] = not any(
            marker in combined
            for marker in ("google-analytics", "googletagmanager", "facebook.com/tr", "segment.io")
        )
        checks["portfolio_features"] = all(
            marker in html for marker in ("skill-filter", "theme-toggle", "Architecture", "resumes/")
        ) and "serviceWorker.register" in app
    except (OSError, UnicodeDecodeError) as exc:
        checks["portfolio_no_trackers"] = checks["portfolio_features"] = False
        errors.append(f"portfolio unreadable: {exc}")
    if not checks["portfolio_no_trackers"]:
        errors.append("portfolio tracker policy failed")
    if not checks["portfolio_features"]:
        errors.append("portfolio feature contract failed")

    checks["manifest_digest"] = sha256_file(manifest_path) == receipt.get("manifest_sha256")
    checks["bundle_digest"] = bundle_path.is_file() and sha256_file(bundle_path) == receipt.get("deployment_bundle_sha256")
    checks["receipt_policy"] = receipt.get("facts_invariant") is True and receipt.get("network_queries") == 0 and receipt.get("external_writes") == 0
    for name in ("manifest_digest", "bundle_digest", "receipt_policy"):
        if not checks[name]:
            errors.append(f"failed {name}")

    try:
        with zipfile.ZipFile(bundle_path) as archive:
            names = set(archive.namelist())
            checks["deployment_bundle_contents"] = not any(
                safe_relative_path(name) is None or name.endswith("/") for name in names
            ) and names == declared | {"manifest.json"}
    except (OSError, zipfile.BadZipFile):
        checks["deployment_bundle_contents"] = False
    if not checks["deployment_bundle_contents"]:
        errors.append("deployment bundle content mismatch")

    return {
        "schema": "glaciereq.career-platform-verification.v2",
        "state": "VERIFIED" if not errors and all(checks.values()) else "FAILED",
        "checks": checks,
        "resume_variants": resume_checks,
        "errors": errors,
        "manifest_sha256": sha256_file(manifest_path),
        "deployment_bundle_sha256": sha256_file(bundle_path) if bundle_path.is_file() else None,
        "build_id": receipt.get("build_id"),
    }
