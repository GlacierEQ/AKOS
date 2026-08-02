from __future__ import annotations

import re
from pathlib import Path

HEADINGS = (
    "<!-- README-ACT:HUMAN -->",
    "<!-- README-ACT:MASTER -->",
    "<!-- README-ACT:MACHINE -->",
    "<!-- README-ACT:MESH -->",
)
FORBIDDEN_VISIBLE_HEADINGS = (
    "## For recruiters and non-technical reviewers",
    "## For senior engineers and domain experts",
    "## For AI systems and toolchains",
    "## Repository mesh",
    "## Portfolio mesh",
)
FILE_URL_PREFIX = "file:" + "/" * 3
MAC_USER_PREFIX = "/" + "Users" + "/"
LOCAL_PATH = re.compile(
    "|".join(
        (
            re.escape(FILE_URL_PREFIX),
            re.escape(MAC_USER_PREFIX),
            r"[A-Za-z]:\\Users\\",
        )
    )
)
REQUIRED_EVIDENCE = (
    ".github/workflows/ci.yml",
    "scripts/verify_repository.py",
    "glaciereq.akos.test-receipt.v1",
    "blocked_scope:",
    "unverified_scope:",
    "relationships:",
)


def verify_readme(readme: Path) -> tuple[str, ...]:
    text = readme.read_text(encoding="utf-8")
    errors: list[str] = []

    missing = [heading for heading in HEADINGS if heading not in text]
    if missing:
        errors.append(f"missing required four-act markers: {missing}")
    else:
        positions = [text.index(heading) for heading in HEADINGS]
        if positions != sorted(positions):
            errors.append("four-act README markers are out of order")

    bland = [heading for heading in FORBIDDEN_VISIBLE_HEADINGS if heading in text]
    if bland:
        errors.append(f"README uses forbidden generic visible headings: {bland}")

    if LOCAL_PATH.search(text):
        errors.append("README exposes a machine-local path")

    missing_evidence = [value for value in REQUIRED_EVIDENCE if value not in text]
    if missing_evidence:
        errors.append(f"machine contract is incomplete: {missing_evidence}")

    return tuple(errors)


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    readme = repository_root / "README.md"
    errors = verify_readme(readme)
    if errors:
        raise SystemExit("AKOS README contract failed: " + "; ".join(errors))

    print("AKOS README contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
