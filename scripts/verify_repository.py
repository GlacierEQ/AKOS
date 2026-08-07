from __future__ import annotations

import argparse
import contextlib
import json
import os
import platform
import sys
import tempfile
import time
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

import pytest

TEST_ROOTS = (".integrity", "operational_cognition", "finisher", "tests")
RECEIPT_SCHEMA = "glaciereq.akos.test-receipt.v1"


def discover_test_files(repository_root: Path) -> tuple[Path, ...]:
    files: set[Path] = set()
    for root_name in TEST_ROOTS:
        test_root = repository_root / root_name
        if not test_root.is_dir():
            continue
        files.update(path.resolve() for path in test_root.rglob("test_*.py") if path.is_file())
    return tuple(sorted(files))


class ReceiptPlugin:
    def __init__(self) -> None:
        self.collected = 0
        self.outcomes: dict[str, str] = {}
        self.collection_errors: list[dict[str, str]] = []
        self.internal_errors: list[str] = []

    def pytest_collection_modifyitems(
        self,
        session: pytest.Session,
        config: pytest.Config,
        items: list[pytest.Item],
    ) -> None:
        del session, config
        self.collected = len(items)

    def pytest_collectreport(self, report: pytest.CollectReport) -> None:
        if report.failed:
            self.collection_errors.append(
                {
                    "nodeid": report.nodeid,
                    "message": str(report.longrepr),
                }
            )

    def pytest_internalerror(
        self,
        excrepr: pytest.ExceptionInfo[BaseException],
        excinfo: pytest.ExceptionInfo[BaseException],
    ) -> None:
        del excinfo
        self.internal_errors.append(str(excrepr))

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        current = self.outcomes.get(report.nodeid)
        if report.when == "setup":
            if report.failed:
                self.outcomes[report.nodeid] = "error"
            elif report.skipped:
                self.outcomes[report.nodeid] = "skipped"
            return

        if report.when == "call":
            if report.passed:
                self.outcomes[report.nodeid] = "passed"
            elif report.failed:
                self.outcomes[report.nodeid] = "failed"
            elif report.skipped:
                self.outcomes[report.nodeid] = "skipped"
            return

        if report.when == "teardown" and report.failed and current != "failed":
            self.outcomes[report.nodeid] = "error"

    def summary(self) -> dict[str, int]:
        return {
            outcome: sum(value == outcome for value in self.outcomes.values())
            for outcome in ("passed", "failed", "error", "skipped")
        }

    def nodeids(self, outcome: str) -> list[str]:
        return sorted(
            nodeid for nodeid, observed in self.outcomes.items() if observed == outcome
        )


def atomic_write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _base_receipt(
    repository_root: Path,
    test_files: tuple[Path, ...],
    started_ns: int,
) -> dict[str, object]:
    return {
        "schema": RECEIPT_SCHEMA,
        "repository": "GlacierEQ/AKOS",
        "commit": os.getenv("GITHUB_SHA", "LOCAL"),
        "python": platform.python_version(),
        "pytest": pytest.__version__,
        "started_at_epoch_ns": started_ns,
        "test_modules": [str(path.relative_to(repository_root)) for path in test_files],
    }


def verify_repository(
    repository_root: Path,
    output: Path,
    *,
    stream: TextIO | None = None,
) -> dict[str, object]:
    repository_root = repository_root.resolve()
    output = output.resolve()
    started_ns = time.time_ns()
    test_files = discover_test_files(repository_root)
    receipt = _base_receipt(repository_root, test_files, started_ns)

    if not test_files:
        receipt.update(
            {
                "completed_at_epoch_ns": time.time_ns(),
                "collected": 0,
                "tests_run": 0,
                "passed": 0,
                "failures": 0,
                "errors": 0,
                "skipped": 0,
                "failed_tests": [],
                "error_tests": [],
                "collection_errors": [],
                "internal_errors": [],
                "conclusion": "FAILED",
                "reason": "no test modules were discovered",
            }
        )
        atomic_write_json(output, receipt)
        return receipt

    plugin = ReceiptPlugin()
    arguments = [
        "-q",
        "--disable-warnings",
        "--rootdir",
        str(repository_root),
        *[str(path) for path in test_files],
    ]

    capture = stream if stream is not None else sys.stdout
    try:
        with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
            exit_code = pytest.main(arguments, plugins=[plugin])
    except BaseException as exc:
        plugin.internal_errors.append(f"{type(exc).__name__}: {exc}")
        exit_code = pytest.ExitCode.INTERNAL_ERROR

    summary = plugin.summary()
    tests_run = sum(summary.values())
    receipt.update(
        {
            "completed_at_epoch_ns": time.time_ns(),
            "pytest_exit_code": int(exit_code),
            "collected": plugin.collected,
            "tests_run": tests_run,
            "passed": summary["passed"],
            "failures": summary["failed"],
            "errors": summary["error"],
            "skipped": summary["skipped"],
            "failed_tests": plugin.nodeids("failed"),
            "error_tests": plugin.nodeids("error"),
            "collection_errors": plugin.collection_errors,
            "internal_errors": plugin.internal_errors,
        }
    )

    infrastructure_failure = (
        bool(plugin.collection_errors)
        or bool(plugin.internal_errors)
        or exit_code
        in {
            pytest.ExitCode.INTERRUPTED,
            pytest.ExitCode.INTERNAL_ERROR,
            pytest.ExitCode.USAGE_ERROR,
        }
    )
    if infrastructure_failure:
        receipt["conclusion"] = "FAILED"
        receipt["reason"] = "pytest reported a collection, usage, or internal error"
    elif plugin.collected <= 0:
        receipt["conclusion"] = "UNVERIFIED"
        receipt["reason"] = "pytest collected no tests"
    elif tests_run <= 0:
        receipt["conclusion"] = "UNVERIFIED"
        receipt["reason"] = "pytest executed no tests"
    elif (
        exit_code != pytest.ExitCode.OK
        or summary["failed"]
        or summary["error"]
    ):
        receipt["conclusion"] = "FAILED"
        receipt["reason"] = "pytest reported one or more failed or errored tests"
    else:
        receipt["conclusion"] = "VERIFIED"
        receipt["evidence_level"] = "TEST"

    atomic_write_json(output, receipt)
    return receipt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the exhaustive AKOS pytest surface and emit an atomic receipt."
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/ci/test-receipt.json"),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repository_root = args.repository_root.resolve()
    sys.path.insert(0, str(repository_root))
    receipt = verify_repository(repository_root, args.output)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["conclusion"] == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
