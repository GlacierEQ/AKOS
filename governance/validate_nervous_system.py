#!/usr/bin/env python3
"""Validate a GlacierEQ nervous-system node against the canonical manifest."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.request import urlopen

CANONICAL_URL = (
    "https://raw.githubusercontent.com/GlacierEQ/AKOS/main/"
    "governance/glaciereq.nervous-system.v1.json"
)
LOCAL_MANIFEST = Path("governance/glaciereq.nervous-system.v1.json")
LOCAL_CONTRACT = Path(".glaciereq/nervous-system.node.json")
README = Path("README.md")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_manifest() -> dict:
    if LOCAL_MANIFEST.exists():
        return load_json(LOCAL_MANIFEST)
    with urlopen(CANONICAL_URL, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"::error::{error}")
    print(json.dumps({"schema": "glaciereq.nervous-system.validation.v1", "status": "failed", "errors": errors}, indent=2))
    return 1


def main() -> int:
    errors: list[str] = []
    manifest = load_manifest()
    repository = os.getenv("GITHUB_REPOSITORY")
    if not repository:
        repository = load_json(LOCAL_CONTRACT).get("repository") if LOCAL_CONTRACT.exists() else None
    if not repository:
        return fail(["Repository identity unavailable: set GITHUB_REPOSITORY or add local node contract."])

    nodes = manifest.get("nodes", {})
    expected = nodes.get(repository)
    if expected is None:
        return fail([f"Repository {repository} is not registered in {manifest.get('schema_id')}."])

    if not LOCAL_CONTRACT.exists():
        errors.append(f"Missing local contract: {LOCAL_CONTRACT}")
        contract = {}
    else:
        contract = load_json(LOCAL_CONTRACT)

    if contract.get("schema_id") != manifest.get("schema_id"):
        errors.append("Local schema_id does not match canonical schema_id.")
    if contract.get("repository") != repository:
        errors.append("Local repository identity does not match execution repository.")
    if contract.get("role") != expected.get("role"):
        errors.append(f"Role drift: expected {expected.get('role')!r}, got {contract.get('role')!r}.")
    if contract.get("canonical_manifest") != f"{manifest.get('canonical_repository')}/{manifest.get('canonical_path')}":
        errors.append("Local canonical_manifest pointer is missing or incorrect.")

    if not README.exists():
        errors.append("README.md is missing.")
        readme = ""
    else:
        readme = README.read_text(encoding="utf-8").lower()

    for term in expected.get("required_terms", []):
        if term.lower() not in readme:
            errors.append(f"README missing required role term: {term}")
    for link in expected.get("required_links", []):
        if link.lower() not in readme:
            errors.append(f"README missing nervous-system link: {link}")

    sequence = manifest.get("operating_sequence", [])
    normalized = " → ".join(word.upper() for word in sequence).lower()
    ascii_normalized = " -> ".join(word.upper() for word in sequence).lower()
    if normalized not in readme and ascii_normalized not in readme:
        errors.append("README missing canonical MEMORY → TOOL → CURE → INNOVATE → RESPOND sequence.")

    if errors:
        return fail(errors)

    receipt = {
        "schema": "glaciereq.nervous-system.validation.v1",
        "status": "verified",
        "repository": repository,
        "role": expected["role"],
        "manifest_version": manifest["version"],
        "checks": ["identity", "role", "canonical_pointer", "required_terms", "required_links", "operating_sequence"],
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
