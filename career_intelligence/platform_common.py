"""Shared deterministic packaging helpers for Career Intelligence Platform v2."""

from __future__ import annotations

import os
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Iterable

from .models import CareerGraphError

FIXED_ZIP_TIME = (2026, 8, 6, 0, 0, 0)
VARIANTS: dict[str, str] = {
    "executive": "cto",
    "ats": "technical-recruiter",
    "recruiter": "technical-recruiter",
    "government": "government-reviewer",
    "startup": "startup-founder",
}
REQUIRED_PLATFORM_FILES = {
    "canonical/career-graph.json",
    "analysis/job-analysis.json",
    "analysis/gap-analysis.json",
    "analysis/reader-profile.json",
    "analysis/persona-council.json",
    "analysis/skill-evidence-map.json",
    "reports/ats-report.json",
    "reports/platform-boundaries.json",
    "interview/interview-packet.json",
    "interview/interview-packet.md",
    "interview/star-library.json",
    "profiles/linkedin.md",
    "profiles/github-profile.md",
    "letters/cover-letter.md",
    "bios/executive-bio.md",
    "bios/speaker-bio.md",
    "resumes/one-page.md",
    "resumes/two-page.md",
    "resources/resource-index.json",
    "portfolio/index.html",
    "portfolio/architecture.html",
    "portfolio/accessibility-report.json",
    "portfolio/seo-report.json",
    "portfolio/performance-report.json",
    "portfolio/analytics-policy.json",
    "archives/portfolio.zip",
}


def safe_relative_path(value: object) -> PurePosixPath | None:
    if not isinstance(value, str) or not value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or "." in path.parts or ".." in path.parts:
        return None
    return path


def publish_directory(temporary: Path, output_dir: Path) -> None:
    if not output_dir.exists():
        os.replace(temporary, output_dir)
        return
    if output_dir.is_symlink():
        raise CareerGraphError("refusing to replace symlink output directory")
    backup = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.previous-", dir=output_dir.parent))
    backup.rmdir()
    os.replace(output_dir, backup)
    try:
        os.replace(temporary, output_dir)
    except Exception:
        os.replace(backup, output_dir)
        raise
    shutil.rmtree(backup, ignore_errors=True)


def write_deterministic_zip(destination: Path, root: Path, paths: Iterable[Path]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.building")
    temporary.unlink(missing_ok=True)
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(paths, key=lambda item: item.relative_to(root).as_posix()):
                if path.is_symlink() or not path.is_file():
                    raise CareerGraphError(f"unsafe archive input: {path}")
                info = zipfile.ZipInfo(path.relative_to(root).as_posix(), FIXED_ZIP_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes())
        os.replace(temporary, destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
