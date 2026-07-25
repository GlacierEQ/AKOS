from __future__ import annotations

"""Deterministic repository-integrity watchdog.

The watchdog has two explicit trust modes:

* ``baseline`` compares the working tree with a reviewed SHA-256 manifest.
* ``git`` compares the working tree with a pinned Git commit (``HEAD`` by default).

Verification never rewrites its own trust anchor. Baseline creation is a separate,
explicit command.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

SCHEMA_VERSION = 1
HASH_ALGORITHM = "sha256"
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
        self.excluded_files = frozenset(Path(p).as_posix() for p in excluded_files)
        self.baseline = self._load_baseline()

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
        for path in sorted(self.repo_root.rglob("*"), key=lambda p: p.as_posix()):
            relative = path.relative_to(self.repo_root)
            if self._is_excluded(relative):
                continue
            if path.is_symlink() or path.is_file():
                yield relative.as_posix(), path

    def scan(self) -> dict[str, str]:
        current: dict[str, str] = {}
        for relative, path in self._iter_files():
            if path.is_symlink():
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

        # Backward compatibility with the original flat mapping.
        files = raw.get("files") if isinstance(raw, dict) and "files" in raw else raw
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
        return files

    def report(self) -> IntegrityReport:
        if not self.hash_store.exists() or not self.baseline:
            return IntegrityReport(
                anchor=f"baseline:{self.hash_store}",
                error="missing or empty SHA-256 baseline",
            )
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
            anchor=f"baseline:{self.hash_store}",
            added=added,
            removed=removed,
            modified=modified,
            unchanged=unchanged,
        )

    def verify(self) -> dict[str, bool]:
        """Compatibility API: return status for the union of baseline/current paths."""
        current = self.scan()
        all_paths = sorted(set(self.baseline) | set(current))
        return {path: self.baseline.get(path) == current.get(path) for path in all_paths}

    def verify_git(self, anchor: str = "HEAD") -> IntegrityReport:
        """Verify tracked content against a Git anchor and reject untracked files."""
        try:
            subprocess.run(
                ["git", "-C", str(self.repo_root), "rev-parse", "--verify", anchor],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
            changed = self._git_paths(
                ["diff", "--name-only", "--no-renames", "-z", anchor, "--"], nul=True
            )
            untracked = self._git_paths(
                ["ls-files", "--others", "--exclude-standard", "-z"], nul=True
            )
            tracked = set(
                self._git_paths(["ls-tree", "-r", "--name-only", "-z", anchor], nul=True)
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            detail = getattr(exc, "stderr", None) or str(exc)
            return IntegrityReport(anchor=f"git:{anchor}", error=detail.strip())

        changed = {path for path in changed if not self._is_excluded(Path(path))}
        untracked = {path for path in untracked if not self._is_excluded(Path(path))}
        tracked = {path for path in tracked if not self._is_excluded(Path(path))}
        removed = tuple(sorted(path for path in changed if not (self.repo_root / path).exists()))
        modified = tuple(sorted(set(changed) - set(removed)))
        added = tuple(sorted(untracked))
        unchanged = max(0, len(tracked - set(changed)))
        return IntegrityReport(
            anchor=f"git:{anchor}",
            added=added,
            removed=removed,
            modified=modified,
            unchanged=unchanged,
        )

    def _git_paths(self, arguments: Sequence[str], *, nul: bool = False) -> set[str]:
        completed = subprocess.run(
            ["git", "-C", str(self.repo_root), *arguments],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        separator = b"\0" if nul else b"\n"
        return {
            item.decode("utf-8", errors="surrogateescape")
            for item in completed.stdout.split(separator)
            if item
        }


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
    watchdog = WatchdogDaemon(repo_root=args.root, hash_store=args.baseline)
    if args.command == "snapshot":
        if args.confirm != "YES":
            print("Refusing to rewrite trust anchor: pass --confirm YES", file=sys.stderr)
            return 2
        files = watchdog.update_baseline()
        print(f"Wrote SHA-256 baseline for {len(files)} files: {watchdog.hash_store}")
        return 0
    report = watchdog.verify_git(args.anchor) if args.command == "verify-git" else watchdog.report()
    _print_report(report, json_output=args.json_output)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
