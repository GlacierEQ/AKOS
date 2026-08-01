from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

API_ROOT = "https://api.github.com"
DEFAULT_MANIFEST = Path("governance/glaciereq.aspen-grove-constellation.v1.json")
DEFAULT_CHECK = "Aspen Grove Contract / validate"


@dataclass(frozen=True)
class Result:
    repository: str
    status: str
    detail: str


def request_json(url: str, token: str, method: str, body: dict[str, Any] | None = None) -> tuple[int, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "GlacierEQ-Aspen-Grove-Protection/1.0",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
            return response.status, json.loads(payload) if payload else None
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        try:
            parsed: Any = json.loads(payload) if payload else None
        except json.JSONDecodeError:
            parsed = payload
        return exc.code, parsed


def protection_payload(required_check: str) -> dict[str, Any]:
    return {
        "required_status_checks": {
            "strict": True,
            "contexts": [required_check],
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 0,
            "require_last_push_approval": False,
        },
        "restrictions": None,
        "required_linear_history": False,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": True,
        "lock_branch": False,
        "allow_fork_syncing": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply required Aspen Grove Contract protection to every active Grove.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--branch", default="main")
    parser.add_argument("--required-check", default=os.getenv("ASPEN_GROVE_REQUIRED_CHECK", DEFAULT_CHECK))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--receipt", type=Path, default=Path("artifacts/aspen-grove-branch-protection-receipt.json"))
    args = parser.parse_args()

    token = os.getenv("GROVE_ADMIN_TOKEN", "").strip()
    if not args.dry_run and not token:
        print("GROVE_ADMIN_TOKEN is required for live branch-protection writes.", file=sys.stderr)
        return 2

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    repositories = [node["repository"] for node in manifest["nodes"]]
    results: list[Result] = []

    for repository in repositories:
        if args.dry_run:
            results.append(Result(repository, "DRY_RUN", f"would require {args.required_check!r} on {args.branch}"))
            continue

        url = f"{API_ROOT}/repos/{repository}/branches/{args.branch}/protection"
        status, payload = request_json(url, token, "PUT", protection_payload(args.required_check))
        if 200 <= status < 300:
            verification_status, verification = request_json(url, token, "GET")
            contexts = (((verification or {}).get("required_status_checks") or {}).get("contexts") or [])
            if verification_status == 200 and args.required_check in contexts:
                results.append(Result(repository, "APPLIED", f"required check verified: {args.required_check}"))
            else:
                results.append(Result(repository, "VERIFY_FAILED", f"HTTP {verification_status}: {verification}"))
        else:
            results.append(Result(repository, "FAILED", f"HTTP {status}: {payload}"))

    receipt = {
        "schema_id": "glaciereq.aspen-grove-branch-protection-receipt.v1",
        "branch": args.branch,
        "required_check": args.required_check,
        "dry_run": args.dry_run,
        "results": [result.__dict__ for result in results],
        "status": "PASS" if all(result.status in {"APPLIED", "DRY_RUN"} for result in results) else "FAIL",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
