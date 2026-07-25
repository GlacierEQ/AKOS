from __future__ import annotations

"""Deterministic repository-integrity watchdog.

Trust modes:

* ``baseline`` compares the working tree with a reviewed SHA-256 manifest.
* ``git`` compares actual working-tree bytes with a pinned Git tree.

Verification never rewrites its own trust anchor. Baseline creation is a separate,
explicit command.
"""

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

SCHEMA_VERSION = 1
HASH_ALGORITHM = "sha256"
GIT_TIMEOUT_SECONDS = 30
BASELINE_STATUS_KEY = "__akos_baseline__"
DEFAULT_EXCLUDED_DIRS = frozenset(
    {
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "venv",
        "node_modules",
        "dist",
        "build",
        "out",
    }
)
DEFAULT_EXCLUDED_FILES = frozenset({".integrity/file_hashes.json"})


@dataclass(frozen=True)
class IntegrityReport:
    anchor: str
    added: tuple[str, ...] = ()
    removed: tuple[str, ...] = ()
    modified: tuple[str, ...] = ()
    unchanged: int = 0
    error: str | None = None

    @property
    def ok(self) -> bool:
        return not self.error and not (self.added or self.removed or self.modified)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["ok"] = self.ok
        return payload


@dataclass(frozen=True)
class GitTreeEntry:
    mode: str
    object_type: str
    object_sha: str


class WatchdogDaemon:
    def __init__(
        self,
        repo_root: str | os.PathLike[str] | None = None,
        hash_store: str | os.PathLike[str] | None = None,
        *,
        excluded_dirs: Iterable[str] = DEFAULT_EXCLUDED_DIRS,
        excluded_files: Iterable[str] = DEFAULT_EXCLUDED_FILES,
    ) -> None:
        module_root = Path(__file__).resolve().parents[1]
        self.repo_root = Path(repo_root).resolve() if repo_root else module_root
        self.integrity_dir = self.repo_root / ".integrity"
        self.hash_store = (
            Path(hash_store).resolve()
            if hash_store
            else self.integrity_dir / "file_hashes.json"
        )
        self.excluded_dirs = frozenset(excluded_dirs)
        dynamic_exclusions = {Path(path).as_posix() for path in excluded_files}
        try:
            dynamic_exclusions.add(self.hash_store.relative_to(self.repo_root).as_posix())
        except ValueError:
            pass
        self.excluded_files = frozenset(dynamic_exclusions)
        self.baseline: dict[str, str] = {}
        self.baseline_error: str | None = None
        try:
            self.baseline = self._load_baseline()
        except (OSError, ValueError) as exc:
            self.baseline_error = str(exc)

    @staticmethod
    def _sha256_file(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()

    @staticmethod
    def _sha256_bytes(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _is_excluded(self, relative: Path) -> bool:
        posix = relative.as_posix()
        return posix in self.excluded_files or any(
            part in self.excluded_dirs for part in relative.parts
        )

    def _iter_files(self) -> Iterable[tuple[str, Path]]:
        if not self.repo_root.is_dir():
            raise FileNotFoundError(f"repository root does not exist: {self.repo_root}")

        for current_root, dirnames, filenames in os.walk(
            self.repo_root, topdown=True, followlinks=False
        ):
            root = Path(current_root)
            kept_dirs: list[str] = []
            for dirname in sorted(dirnames):
                path = root / dirname
                relative = path.relative_to(self.repo_root)
                if self._is_excluded(relative):
                    continue
                if path.is_symlink():
                    yield relative.as_posix(), path
                else:
                    kept_dirs.append(dirname)
            dirnames[:] = kept_dirs

            for filename in sorted(filenames):
                path = root / filename
                relative = path.relative_to(self.repo_root)
                if self._is_excluded(relative):
                    continue
                if path.is_symlink() or path.is_file():
                    yield relative.as_posix(), path

    def scan(self) -> dict[str, str]:
        current: dict[str, str] = {}
        for relative, path in self._iter_files():
            if path.is_symlink():
                # Hash link text only. Never resolve or read the target.
                target = os.readlink(path).encode("utf-8", errors="surrogateescape")
                current[relative] = self._sha256_bytes(b"symlink\0" + target)
            else:
                current[relative] = self._sha256_file(path)
        return current

    def _load_baseline(self) -> dict[str, str]:
        if not self.hash_store.exists():
            return {}
        try:
            raw = json.loads(self.hash_store.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid integrity baseline: {self.hash_store}: {exc}") from exc
        if not isinstance(raw, dict):
            raise ValueError("integrity baseline must be a JSON object")

        if "files" in raw:
            if raw.get("schema_version") != SCHEMA_VERSION:
                raise ValueError(
                    f"unsupported integrity schema: {raw.get('schema_version')!r}"
                )
            if raw.get("algorithm") != HASH_ALGORITHM:
                raise ValueError(
                    f"unsupported integrity algorithm: {raw.get('algorithm')!r}"
                )
            files = raw["files"]
        else:
            # Backward compatibility with the original flat mapping.
            files = raw

        if not isinstance(files, dict):
            raise ValueError("integrity baseline must contain a 'files' object")

        validated: dict[str, str] = {}
        for path, digest in files.items():
            if not isinstance(path, str) or not isinstance(digest, str):
                raise ValueError("integrity baseline entries must be string-to-string")
            if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
                raise ValueError(f"invalid SHA-256 digest for {path!r}")
            validated[Path(path).as_posix()] = digest
        return validated

    def update_baseline(self) -> dict[str, str]:
        """Create a reviewed SHA-256 anchor without weakening verification."""
        files = self.scan()
        payload = {
            "schema_version": SCHEMA_VERSION,
            "algorithm": HASH_ALGORITHM,
            "files": files,
        }
        self.hash_store.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary_name = tempfile.mkstemp(
            prefix=f".{self.hash_store.name}.", dir=str(self.hash_store.parent)
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, self.hash_store)
        except BaseException:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
            raise
        self.baseline = files
        self.baseline_error = None
        return files

    def report(self) -> IntegrityReport:
        anchor = f"baseline:{self.hash_store}"
        if self.baseline_error:
            return IntegrityReport(anchor=anchor, error=self.baseline_error)
        if not self.hash_store.exists() or not self.baseline:
            return IntegrityReport(anchor=anchor, error="missing or empty SHA-256 baseline")
        current = self.scan()
        baseline_paths = set(self.baseline)
        current_paths = set(current)
        added = tuple(sorted(current_paths - baseline_paths))
        removed = tuple(sorted(baseline_paths - current_paths))
        modified = tuple(
            sorted(
                path
                for path in baseline_paths & current_paths
                if self.baseline[path] != current[path]
            )
        )
        unchanged = len((baseline_paths & current_paths) - set(modified))
        return IntegrityReport(
            anchor=anchor,
            added=added,
            removed=removed,
            modified=modified,
            unchanged=unchanged,
        )

    def verify(self) -> dict[str, bool]:
        """Compatibility API returning per-path status and a fail-closed anchor flag."""
        if self.baseline_error or not self.hash_store.exists() or not self.baseline:
            return {BASELINE_STATUS_KEY: False}
        current = self.scan()
        all_paths = sorted(set(self.baseline) | set(current))
        missing = object()
        return {
            path: self.baseline.get(path, missing) == current.get(path, missing)
            for path in all_paths
        }

    def verify_git(self, anchor: str = "HEAD") -> IntegrityReport:
        """Compare actual tracked bytes with a Git tree and reject non-excluded extras."""
        try:
            tree_sha = self._git_text(
                ["rev-parse", "--verify", f"{anchor}^{{tree}}"]
            ).strip()
            entries = self._git_tree(tree_sha)
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            return IntegrityReport(anchor=f"git:{anchor}", error=self._error_text(exc))

        modified: set[str] = set()
        removed: set[str] = set()
        submodules: set[str] = set()

        for relative, entry in sorted(entries.items()):
            path = self.repo_root / relative
            present = path.exists() or path.is_symlink()
            if not present:
                removed.add(relative)
                continue
            try:
                if entry.mode == "120000":
                    if not path.is_symlink():
                        modified.add(relative)
                        continue
                    actual = os.readlink(path).encode("utf-8", errors="surrogateescape")
                    expected = self._git_bytes(["cat-file", "blob", entry.object_sha])
                    if actual != expected:
                        modified.add(relative)
                elif entry.object_type == "blob":
                    if path.is_symlink() or not path.is_file():
                        modified.add(relative)
                        continue
                    actual = path.read_bytes()
                    expected = self._git_bytes(["cat-file", "blob", entry.object_sha])
                    expected_executable = entry.mode == "100755"
                    actual_executable = bool(path.stat().st_mode & stat.S_IXUSR)
                    if actual != expected or actual_executable != expected_executable:
                        modified.add(relative)
                elif entry.object_type == "commit":
                    submodules.add(relative)
                    if not path.is_dir():
                        modified.add(relative)
                        continue
                    current_sha = self._git_text(
                        ["-C", str(path), "rev-parse", "--verify", "HEAD"]
                    ).strip()
                    if current_sha != entry.object_sha:
                        modified.add(relative)
                else:
                    modified.add(relative)
            except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                modified.add(relative)

        tracked_paths = set(entries)
        current_paths = set(self.scan())
        added = {
            path
            for path in current_paths - tracked_paths
            if not any(path == root or path.startswith(f"{root}/") for root in submodules)
        }
        unchanged = max(0, len(tracked_paths - modified - removed))
        return IntegrityReport(
            anchor=f"git:{anchor}",
            added=tuple(sorted(added)),
            removed=tuple(sorted(removed)),
            modified=tuple(sorted(modified)),
            unchanged=unchanged,
        )

    def _git_tree(self, tree_sha: str) -> dict[str, GitTreeEntry]:
        output = self._git_bytes(
            ["ls-tree", "-r", "-z", "--full-tree", tree_sha]
        )
        entries: dict[str, GitTreeEntry] = {}
        for record in output.split(b"\0"):
            if not record:
                continue
            header, raw_path = record.split(b"\t", 1)
            mode, object_type, object_sha = header.split(b" ", 2)
            relative = raw_path.decode("utf-8", errors="surrogateescape")
            entries[relative] = GitTreeEntry(
                mode=mode.decode("ascii"),
                object_type=object_type.decode("ascii"),
                object_sha=object_sha.decode("ascii"),
            )
        return entries

    def _run_git(
        self, arguments: Sequence[str], *, text: bool = False
    ) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self.repo_root), *arguments],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=text,
            timeout=GIT_TIMEOUT_SECONDS,
        )

    def _git_bytes(self, arguments: Sequence[str]) -> bytes:
        output = self._run_git(arguments).stdout
        assert isinstance(output, bytes)
        return output

    def _git_text(self, arguments: Sequence[str]) -> str:
        output = self._run_git(arguments, text=True).stdout
        assert isinstance(output, str)
        return output

    @staticmethod
    def _error_text(exc: BaseException) -> str:
        detail = getattr(exc, "stderr", None)
        if isinstance(detail, bytes):
            return detail.decode("utf-8", errors="replace").strip()
        if isinstance(detail, str) and detail.strip():
            return detail.strip()
        return str(exc)


def _print_report(report: IntegrityReport, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
        return
    state = "PASS" if report.ok else "FAIL"
    print(f"Integrity check: {state} ({report.anchor})")
    if report.error:
        print(f"error: {report.error}")
    for label, paths in (
        ("added", report.added),
        ("removed", report.removed),
        ("modified", report.modified),
    ):
        for path in paths:
            print(f"{label}: {path}")
    print(f"unchanged: {report.unchanged}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        nargs="?",
        default="verify",
        choices=("verify", "verify-git", "snapshot"),
    )
    parser.add_argument("--root", default=None, help="repository root (defaults to module parent)")
    parser.add_argument("--baseline", default=None, help="baseline file path")
    parser.add_argument("--anchor", default="HEAD", help="Git anchor for verify-git")
    parser.add_argument("--confirm", default="NO", help="must be YES for snapshot")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "snapshot" and args.confirm != "YES":
        print("Refusing to rewrite trust anchor: pass --confirm YES", file=sys.stderr)
        return 2

    watchdog = WatchdogDaemon(repo_root=args.root, hash_store=args.baseline)
    if args.command == "snapshot":
        files = watchdog.update_baseline()
        print(f"Wrote SHA-256 baseline for {len(files)} files: {watchdog.hash_store}")
        return 0
    report = watchdog.verify_git(args.anchor) if args.command == "verify-git" else watchdog.report()
    _print_report(report, json_output=args.json_output)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
