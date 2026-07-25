from __future__ import annotations

import importlib.util
import json
import os
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

BASELINE_STATUS_KEY = watchdog_module.BASELINE_STATUS_KEY
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
        self.assertFalse(self.watchdog.report().ok)
        self.assertEqual(self.watchdog.verify(), {BASELINE_STATUS_KEY: False})

    def test_clean_snapshot_passes(self) -> None:
        files = self.watchdog.update_baseline()
        self.assertIn("src/app.py", files)
        self.assertTrue(self.watchdog.report().ok)
        payload = json.loads(self.watchdog.hash_store.read_text(encoding="utf-8"))
        self.assertEqual(payload["algorithm"], "sha256")
        self.assertEqual(payload["schema_version"], 1)

    def test_custom_in_repo_baseline_excludes_itself(self) -> None:
        custom = self.root / "trust" / "anchor.json"
        watchdog = WatchdogDaemon(repo_root=self.root, hash_store=custom)
        watchdog.update_baseline()
        self.assertTrue(watchdog.report().ok)

    def test_invalid_manifest_metadata_fails_closed(self) -> None:
        self.watchdog.hash_store.parent.mkdir(parents=True)
        self.watchdog.hash_store.write_text(
            json.dumps({"schema_version": 99, "algorithm": "md5", "files": {}}),
            encoding="utf-8",
        )
        watchdog = WatchdogDaemon(repo_root=self.root)
        self.assertFalse(watchdog.report().ok)
        self.assertIn("unsupported integrity schema", watchdog.report().error or "")
        self.assertEqual(watchdog.verify(), {BASELINE_STATUS_KEY: False})

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

    def test_verify_marks_added_removed_and_modified_false(self) -> None:
        self.watchdog.update_baseline()
        (self.root / "README.md").unlink()
        (self.root / "src" / "app.py").write_text("VALUE = 3\n", encoding="utf-8")
        (self.root / "new.txt").write_text("new\n", encoding="utf-8")
        status = self.watchdog.verify()
        self.assertFalse(status["README.md"])
        self.assertFalse(status["src/app.py"])
        self.assertFalse(status["new.txt"])

    def test_symlink_hashes_link_text_without_reading_target(self) -> None:
        outside = self.root.parent / "outside-secret.txt"
        outside.write_text("secret-v1\n", encoding="utf-8")
        link = self.root / "external-link"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        first = self.watchdog.scan()["external-link"]
        outside.write_text("secret-v2\n", encoding="utf-8")
        second = self.watchdog.scan()["external-link"]
        self.assertEqual(first, second)

    def test_snapshot_refusal_precedes_malformed_baseline_load(self) -> None:
        malformed = self.root / "bad.json"
        malformed.write_text("{", encoding="utf-8")
        result = main(
            ["snapshot", "--root", str(self.root), "--baseline", str(malformed)]
        )
        self.assertEqual(result, 2)
        self.assertEqual(malformed.read_text(encoding="utf-8"), "{")


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

    def _commit_all(self, message: str) -> None:
        subprocess.run(["git", "-C", str(self.root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", message], check=True)

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

    def test_git_ignored_untracked_file_fails(self) -> None:
        (self.root / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
        self._commit_all("ignore policy")
        (self.root / "ignored.txt").write_text("unreviewed\n", encoding="utf-8")
        self.assertIn("ignored.txt", self.watchdog.verify_git().added)

    def test_git_assume_unchanged_cannot_hide_drift(self) -> None:
        subprocess.run(
            ["git", "-C", str(self.root), "update-index", "--assume-unchanged", "app.py"],
            check=True,
        )
        (self.root / "app.py").write_text("print('bypass')\n", encoding="utf-8")
        self.assertEqual(self.watchdog.verify_git().modified, ("app.py",))

    def test_git_tracked_file_under_excluded_directory_is_verified(self) -> None:
        (self.root / "build").mkdir()
        (self.root / "build" / "tracked.py").write_text("VALUE = 1\n", encoding="utf-8")
        self._commit_all("track build artifact")
        (self.root / "build" / "tracked.py").write_text("VALUE = 2\n", encoding="utf-8")
        self.assertIn("build/tracked.py", self.watchdog.verify_git().modified)

    def test_git_executable_mode_change_fails(self) -> None:
        os.chmod(self.root / "app.py", 0o755)
        self.assertEqual(self.watchdog.verify_git().modified, ("app.py",))

    def test_invalid_tree_anchor_returns_json_serializable_error(self) -> None:
        blob_sha = subprocess.run(
            ["git", "-C", str(self.root), "hash-object", "-w", "app.py"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        report = self.watchdog.verify_git(blob_sha)
        self.assertFalse(report.ok)
        json.dumps(report.to_dict())


if __name__ == "__main__":
    unittest.main()
