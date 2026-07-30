from __future__ import annotations

import re
from pathlib import Path

HEADINGS = (
    "## For recruiters and non-technical reviewers",
    "## For senior engineers and domain experts",
    "## For AI systems and toolchains",
)
FILE_URL_PREFIX = "file:" + "/" * 3
MAC_USER_PREFIX = "/" + "Users" + "/"
LOCAL_PATH = re.compile(
    "|".join(
        (
            re.escape(FILE_URL_PREFIX),
            re.escape(MAC_USER_PREFIX),
            r"[A-Za-z]:\\\\Users\\\\",
        )
    )
)


def main() -> int:
    readme = Path("README.md")
    text = readme.read_text(encoding="utf-8")
    missing = [heading for heading in HEADINGS if heading not in text]
    if missing:
        raise SystemExit(f"README is missing required audience headings: {missing}")

    positions = [text.index(heading) for heading in HEADINGS]
    if positions != sorted(positions):
        raise SystemExit("README audience headings are out of order")
    if LOCAL_PATH.search(text):
        raise SystemExit("README exposes a machine-local path")

    required_evidence = (
        ".github/workflows/ci.yml",
        "scripts/verify_repository.py",
        "glaciereq.akos.test-receipt.v1",
        "blocked_scope:",
        "unverified_scope:",
        "relationships:",
    )
    missing_evidence = [value for value in required_evidence if value not in text]
    if missing_evidence:
        raise SystemExit(f"README machine contract is incomplete: {missing_evidence}")

    print("AKOS README contract verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
