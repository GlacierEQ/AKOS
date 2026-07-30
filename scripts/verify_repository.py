from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import sys
import tempfile
import time
import unittest
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

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


def _import_failure_test(relative: Path, error: Exception) -> unittest.FunctionTestCase:
    def raise_import_error(captured: Exception = error) -> None:
        raise captured

    return unittest.FunctionTestCase(
        raise_import_error,
        description=f"import {relative.as_posix()}",
    )


def load_suite(
    repository_root: Path,
    test_files: tuple[Path, ...],
) -> tuple[unittest.TestSuite, tuple[dict[str, str], ...]]:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    import_errors: list[dict[str, str]] = []

    for index, path in enumerate(test_files):
        relative = path.relative_to(repository_root)
        module_name = "akos_ci_" + "_".join(relative.with_suffix("").parts) + f"_{index}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec is None or spec.loader is None:
                raise RuntimeError(f"cannot create an import specification for {relative}")
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            suite.addTests(loader.loadTestsFromModule(module))
        except Exception as exc:
            import_errors.append(
                {
                    "module": relative.as_posix(),
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            )
            suite.addTest(_import_failure_test(relative, exc))

    return suite, tuple(import_errors)


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
        "repository_root": str(repository_root),
        "commit": os.getenv("GITHUB_SHA", "LOCAL"),
        "python": platform.python_version(),
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
    started_ns = time.time_ns()
    test_files = discover_test_files(repository_root)
    receipt = _base_receipt(repository_root, test_files, started_ns)

    if not test_files:
        receipt.update(
            {
                "completed_at_epoch_ns": time.time_ns(),
                "tests_run": 0,
                "failures": 0,
                "errors": 0,
                "skipped": 0,
                "import_errors": [],
                "conclusion": "FAILED",
                "reason": "no test modules were discovered",
            }
        )
        atomic_write_json(output, receipt)
        return receipt

    suite, import_errors = load_suite(repository_root, test_files)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    receipt.update(
        {
            "completed_at_epoch_ns": time.time_ns(),
            "tests_run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(result.skipped),
            "import_errors": list(import_errors),
        }
    )

    if result.testsRun <= 0:
        receipt["conclusion"] = "UNVERIFIED"
        receipt["reason"] = "test runner exited without a positive test count"
    elif not result.wasSuccessful():
        receipt["conclusion"] = "FAILED"
        receipt["reason"] = "one or more tests failed, errored, or could not import"
    else:
        receipt["conclusion"] = "VERIFIED"
        receipt["evidence_level"] = "TEST"

    atomic_write_json(output, receipt)
    return receipt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run every AKOS unittest module and emit a positive-count receipt."
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
