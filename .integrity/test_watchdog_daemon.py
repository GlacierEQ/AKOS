from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("watchdog_daemon.py")
SPEC = importlib.util.spec_from_file_location("akos_watchdog", MODULE_PATH)
assert SPEC and SPEC.loader
watchdog_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = watchdog_module
SPEC.loader.exec_module(watchdog_module)

WatchdogDaemon = watchdog_module.WatchdogDaemon
main = watchdog_module.main


class WatchdogBaselineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "src").mkdir()
        (self.root / "src" / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
        (self.root / "README.md").write_text("anchor\n", encoding="utf-8")
        self.watchdog = WatchdogDaemon(repo_root=self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_missing_baseline_fails_closed(self) -> None:
        report = self.watchdog.report()
        self.assertFalse(report.ok)
        self.assertIn("missing", report.error or "")

    def test_clean_snapshot_passes(self) -> None:
        files = self.watchdog.update_baseline()
        self.assertIn("src/app.py", files)
        self.assertTrue(self.watchdog.report().ok)
        payload = json.loads(self.watchdog.hash_store.read_text(encoding="utf-8"))
        self.assertEqual(payload["algorithm"], "sha256")
        self.assertEqual(payload["schema_version"], 1)

    def test_modified_file_fails(self) -> None:
        self.watchdog.update_baseline()
        (self.root / "src" / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
        self.assertEqual(self.watchdog.report().modified, ("src/app.py",))

    def test_deleted_file_fails(self) -> None:
        self.watchdog.update_baseline()
        (self.root / "README.md").unlink()
        self.assertEqual(self.watchdog.report().removed, ("README.md",))

    def test_added_file_fails(self) -> None:
        self.watchdog.update_baseline()
        (self.root / "new.txt").write_text("drift\n", encoding="utf-8")
        self.assertEqual(self.watchdog.report().added, ("new.txt",))

    def test_verify_compatibility_marks_added_removed_and_modified_false(self) -> None:
        self.watchdog.update_baseline()
        (self.root / "README.md").unlink()
        (self.root / "src" / "app.py").write_text("VALUE = 3\n", encoding="utf-8")
        (self.root / "new.txt").write_text("new\n", encoding="utf-8")
        status = self.watchdog.verify()
        self.assertFalse(status["README.md"])
        self.assertFalse(status["src/app.py"])
        self.assertFalse(status["new.txt"])

    def test_snapshot_requires_explicit_confirmation(self) -> None:
        result = main(["snapshot", "--root", str(self.root)])
        self.assertEqual(result, 2)
        self.assertFalse(self.watchdog.hash_store.exists())


class WatchdogGitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            ["git", "-C", str(self.root), "config", "user.email", "test@example.invalid"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.root), "config", "user.name", "AKOS Test"],
            check=True,
        )
        (self.root / "app.py").write_text("print('ok')\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "app.py"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "anchor"], check=True)
        self.watchdog = WatchdogDaemon(repo_root=self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_git_clean_tree_passes(self) -> None:
        self.assertTrue(self.watchdog.verify_git().ok)

    def test_git_modified_file_fails(self) -> None:
        (self.root / "app.py").write_text("print('changed')\n", encoding="utf-8")
        self.assertEqual(self.watchdog.verify_git().modified, ("app.py",))

    def test_git_deleted_file_fails(self) -> None:
        (self.root / "app.py").unlink()
        self.assertEqual(self.watchdog.verify_git().removed, ("app.py",))

    def test_git_untracked_file_fails(self) -> None:
        (self.root / "rogue.py").write_text("pass\n", encoding="utf-8")
        self.assertEqual(self.watchdog.verify_git().added, ("rogue.py",))


if __name__ == "__main__":
    unittest.main()
