#!/usr/bin/env python3
"""AKOS Manifest Verifier Unit Tests"""
from __future__ import annotations

import unittest
from pathlib import Path
from src.verify_manifest import verify_manifest


class TestAKOSManifestVerifier(unittest.TestCase):
    """Unit tests validating the manifest verification functions."""

    def setUp(self):
        self.repo_root = Path(__file__).parent.parent
        self.manifest_path = self.repo_root / "AKOS_MANIFEST.yaml"

    def test_manifest_exists(self):
        """Validates that the target manifest exists in the repository."""
        self.assertTrue(self.manifest_path.is_file(), "AKOS_MANIFEST.yaml is missing from the repository root")

    def test_verify_manifest_structure(self):
        """Validates that the existing manifest passes structure verification rules."""
        self.assertTrue(verify_manifest(self.manifest_path), "AKOS_MANIFEST.yaml failed structural verification")


if __name__ == "__main__":
    unittest.main()
