from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify_readme_contract import HEADINGS, REQUIRED_EVIDENCE, verify_readme
from scripts.verify_repository import (
    atomic_write_json,
    discover_test_files,
    verify_repository,
)


class RepositoryVerificationToolTests(unittest.TestCase):
    def test_discovery_includes_integrity_and_ignores_missing_roots(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            integrity = root / ".integrity"
            integrity.mkdir()
            expected = integrity / "test_watchdog.py"
            expected.write_text("import unittest\n", encoding="utf-8")

            discovered = discover_test_files(root)

            self.assertEqual(discovered, (expected.resolve(),))

    def test_no_test_modules_writes_failed_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "artifacts" / "receipt.json"

            receipt = verify_repository(root, output, stream=io.StringIO())

            self.assertEqual(receipt["conclusion"], "FAILED")
            self.assertEqual(receipt["tests_run"], 0)
            self.assertTrue(output.is_file())
            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8"))["conclusion"],
                "FAILED",
            )

    def test_import_failure_is_evidence_not_a_missing_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tests = root / "tests"
            tests.mkdir()
            (tests / "test_broken.py").write_text(
                "raise RuntimeError('import regression')\n",
                encoding="utf-8",
            )
            output = root / "receipt.json"

            receipt = verify_repository(root, output, stream=io.StringIO())

            self.assertEqual(receipt["conclusion"], "FAILED")
            self.assertEqual(receipt["errors"], 1)
            self.assertEqual(len(receipt["import_errors"]), 1)
            self.assertEqual(receipt["import_errors"][0]["type"], "RuntimeError")
            self.assertTrue(output.is_file())

    def test_atomic_write_replaces_content_without_shared_temp_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "receipt.json"
            atomic_write_json(output, {"conclusion": "RUNNING"})
            atomic_write_json(output, {"conclusion": "VERIFIED"})

            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8")),
                {"conclusion": "VERIFIED"},
            )
            self.assertEqual(list(root.glob(".receipt.json.*.tmp")), [])


class ReadmeContractToolTests(unittest.TestCase):
    @staticmethod
    def _valid_readme() -> str:
        return "\n".join((*HEADINGS, *REQUIRED_EVIDENCE)) + "\n"

    def test_valid_contract_is_independent_of_process_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text(self._valid_readme(), encoding="utf-8")

            self.assertEqual(verify_readme(readme), ())

    def test_standard_windows_user_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            windows_path = "C:" + "\\" + "Users" + "\\" + "casey" + "\\repo"
            readme.write_text(self._valid_readme() + windows_path + "\n", encoding="utf-8")

            errors = verify_readme(readme)

            self.assertIn("README exposes a machine-local path", errors)


if __name__ == "__main__":
    unittest.main()
