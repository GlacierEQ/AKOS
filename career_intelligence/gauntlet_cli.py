"""One-command interface for Career Intelligence Platform v2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import CareerGraphError
from .platform_builder import build_career_platform, verify_career_platform

_DEFAULT_SOURCE = Path("career_intelligence/resources/casey-barton.career-runtime.v1.json")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="build-career",
        description="Build the evidence-bound Career Intelligence Platform",
    )
    parser.add_argument("--source", type=Path, default=_DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target", default="Principal Engineer")
    parser.add_argument("--audience", default="principal-engineer")
    parser.add_argument("--job-file", type=Path)
    parser.add_argument("--company", default="")
    parser.add_argument("--resource", type=Path, action="append", default=[])
    parser.add_argument("--resource-catalog", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    return parser


def _load_catalog(path: Path | None) -> dict[str, object] | None:
    if path is None:
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise CareerGraphError("resource catalog root must be an object")
    return payload


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.verify_only:
            result = verify_career_platform(args.output)
        else:
            job_text = args.job_file.read_text(encoding="utf-8") if args.job_file else ""
            build_career_platform(
                args.source,
                args.output,
                target_role=args.target,
                audience=args.audience,
                job_text=job_text,
                company=args.company,
                local_resources=args.resource,
                resource_catalog=_load_catalog(args.resource_catalog),
            )
            result = verify_career_platform(args.output)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result.get("state") == "VERIFIED" else 1
    except (CareerGraphError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"state": "FAILED", "error": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
