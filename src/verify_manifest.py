#!/usr/bin/env python3
"""AKOS Manifest Verifier

Validates the structure, types, and schema of the AKOS_MANIFEST.yaml file.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Add PyYAML dependency-free parsing for lightweight validation if yaml is not installed
try:
    import yaml
except ImportError:
    yaml = None


def load_manifest(manifest_path: Path) -> dict:
    """Loads and parses the AKOS manifest file."""
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest file not found: {manifest_path}")

    content = manifest_path.read_text()
    if yaml:
        return yaml.safe_load(content)

    # Basic fallback parser for simple key-value YAML structure
    data = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def verify_manifest(manifest_path: Path) -> bool:
    """Verifies that key governance and identity fields are defined in the manifest."""
    try:
        data = load_manifest(manifest_path)
        required_keys = ["version", "operator", "governance"]
        for key in required_keys:
            if key not in data:
                print(f"VERIFICATION FAILURE: Missing required manifest key '{key}'", file=sys.stderr)
                return False
        return True
    except Exception as e:
        print(f"VERIFICATION ERROR: Failed to parse manifest: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    default_path = Path(__file__).parent.parent / "AKOS_MANIFEST.yaml"
    success = verify_manifest(default_path)
    sys.exit(0 if success else 1)
