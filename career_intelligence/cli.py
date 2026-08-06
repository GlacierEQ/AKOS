"""Command-line interface for the career intelligence runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .builder import build_package, verify_package
from .io import load_graph
from .models import CareerGraphError, TargetProfile
from .validation import validate_graph

_DEFAULT_SOURCE = Path("career_intelligence/resources/casey-barton.career-runtime.v1.json")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="akos-career", description="Build evidence-bound career artifacts"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--source", type=Path, default=_DEFAULT_SOURCE)

    build = subparsers.add_parser("build")
    build.add_argument("--source", type=Path, default=_DEFAULT_SOURCE)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--role", default="general")
    build.add_argument("--audience", default="technical recruiter")
    build.add_argument("--job-file", type=Path)
    build.add_argument("--max-keywords", type=int, default=24)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "validate":
            graph = load_graph(args.source)
            issues = validate_graph(graph)
            print(
                json.dumps(
                    {
                        "state": "VERIFIED" if not issues else "FAILED",
                        "issues": [item.__dict__ for item in issues],
                    },
                    indent=2,
                )
            )
            return 0 if not issues else 1

        if args.command == "build":
            job_text = args.job_file.read_text(encoding="utf-8") if args.job_file else ""
            target = TargetProfile(
                role=args.role,
                audience=args.audience,
                job_text=job_text,
                max_keywords=args.max_keywords,
            )
            result = build_package(args.source, args.output, target=target)
            verification = verify_package(result.output_dir)
            print(json.dumps(verification, indent=2, sort_keys=True))
            return 0 if verification["state"] == "VERIFIED" else 1

        verification = verify_package(args.output)
        print(json.dumps(verification, indent=2, sort_keys=True))
        return 0 if verification["state"] == "VERIFIED" else 1
    except (CareerGraphError, OSError, UnicodeDecodeError) as exc:
        print(json.dumps({"state": "FAILED", "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
