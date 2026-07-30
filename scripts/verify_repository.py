from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import sys
import time
import unittest
from collections.abc import Sequence
from pathlib import Path

TEST_ROOTS = ("operational_cognition", "finisher", "tests")


def discover_test_files(repository_root: Path) -> tuple[Path, ...]:
    files = {
        path.resolve()
        for root_name in TEST_ROOTS
        for path in (repository_root / root_name).rglob("test_*.py")
        if path.is_file()
    }
    return tuple(sorted(files))


def load_suite(repository_root: Path, test_files: tuple[Path, ...]) -> unittest.TestSuite:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()

    for index, path in enumerate(test_files):
        relative = path.relative_to(repository_root)
        module_name = "akos_ci_" + "_".join(relative.with_suffix("").parts) + f"_{index}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot create an import specification for {relative}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        suite.addTests(loader.loadTestsFromModule(module))

    return suite


def atomic_write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run every AKOS unittest module and emit a positive-count receipt."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/ci/test-receipt.json"),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repository_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repository_root))

    started_ns = time.time_ns()
    test_files = discover_test_files(repository_root)
    suite = load_suite(repository_root, test_files)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    receipt: dict[str, object] = {
        "schema": "glaciereq.akos.test-receipt.v1",
        "repository": "GlacierEQ/AKOS",
        "commit": os.getenv("GITHUB_SHA", "LOCAL"),
        "python": platform.python_version(),
        "started_at_epoch_ns": started_ns,
        "completed_at_epoch_ns": time.time_ns(),
        "test_modules": [str(path.relative_to(repository_root)) for path in test_files],
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
    }

    if not test_files:
        receipt["conclusion"] = "FAILED"
        receipt["reason"] = "no test modules were discovered"
    elif result.testsRun <= 0:
        receipt["conclusion"] = "UNVERIFIED"
        receipt["reason"] = "test runner exited without a positive test count"
    elif not result.wasSuccessful():
        receipt["conclusion"] = "FAILED"
        receipt["reason"] = "one or more tests failed or errored"
    else:
        receipt["conclusion"] = "VERIFIED"
        receipt["evidence_level"] = "TEST"

    atomic_write_json(args.output, receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["conclusion"] == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
