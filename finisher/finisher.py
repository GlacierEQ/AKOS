#!/usr/bin/env python3
"""AKOS Finisher: convert near-complete GitHub work into explicit closure actions.

The Finisher is intentionally narrow. It scans an allowlisted set of pull
requests, applies a deterministic readiness policy, writes a finish queue and
receipt, and can execute at most a bounded number of approved actions.

It never creates new repositories, force-pushes, edits evidence, contacts third
parties, or treats a queued action as completed without a GitHub response.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request
from typing import Any, Iterable

UTC = dt.timezone.utc


class FinisherError(RuntimeError):
    """Raised for configuration, network, or policy failures."""


@dataclasses.dataclass(frozen=True)
class Target:
    repo: str
    pr: int
    desired_action: str = "merge"
    merge_method: str = "squash"
    allow_mark_ready: bool = True
    required_approvals: int = 0
    required_checks: tuple[str, ...] = ()
    notes: str = ""


@dataclasses.dataclass(frozen=True)
class Policy:
    allow_apply: bool = False
    max_actions_per_run: int = 1
    allow_no_checks: bool = True
    freeze_new_work_when_ready: bool = True
    stale_days: int = 14
    output_dir: str = "finisher/out"


@dataclasses.dataclass(frozen=True)
class Snapshot:
    repo: str
    pr: int
    title: str
    url: str
    state: str
    draft: bool
    merged: bool
    mergeable: bool | None
    mergeable_state: str
    head_sha: str
    base_ref: str
    created_at: str
    updated_at: str
    commits: int
    changed_files: int
    additions: int
    deletions: int
    statuses: tuple[dict[str, Any], ...]
    reviews: tuple[dict[str, Any], ...]
    node_id: str


@dataclasses.dataclass(frozen=True)
class Decision:
    target: Target
    snapshot: Snapshot
    score: int
    disposition: str
    next_action: str
    hard_blockers: tuple[str, ...]
    soft_blockers: tuple[str, ...]
    reasons: tuple[str, ...]

    @property
    def finishable(self) -> bool:
        return not self.hard_blockers and self.next_action in {
            "MARK_READY",
            "MERGE",
            "CLOSE",
        }


class GitHubClient:
    def __init__(self, token: str, api_url: str = "https://api.github.com") -> None:
        if not token:
            raise FinisherError("GITHUB_TOKEN is required")
        self.token = token
        self.api_url = api_url.rstrip("/")

    def request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        body = None
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.api_url}{path}",
            data=body,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "akos-finisher/1.0",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read()
                return json.loads(raw.decode("utf-8")) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise FinisherError(
                f"GitHub API {method} {path} failed: HTTP {exc.code}: {detail}"
            ) from exc
        except urllib.error.URLError as exc:
            raise FinisherError(f"GitHub API unavailable: {exc}") from exc

    def get_pr_snapshot(self, target: Target) -> Snapshot:
        repo, pr = target.repo, target.pr
        data = self.request("GET", f"/repos/{repo}/pulls/{pr}")
        head_sha = data["head"]["sha"]
        status_data = self.request("GET", f"/repos/{repo}/commits/{head_sha}/status")
        reviews = self.request("GET", f"/repos/{repo}/pulls/{pr}/reviews?per_page=100")
        return Snapshot(
            repo=repo,
            pr=pr,
            title=data.get("title", ""),
            url=data.get("html_url", ""),
            state=data.get("state", "unknown"),
            draft=bool(data.get("draft", False)),
            merged=bool(data.get("merged", False)),
            mergeable=data.get("mergeable"),
            mergeable_state=data.get("mergeable_state", "unknown"),
            head_sha=head_sha,
            base_ref=data["base"]["ref"],
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            commits=int(data.get("commits", 0)),
            changed_files=int(data.get("changed_files", 0)),
            additions=int(data.get("additions", 0)),
            deletions=int(data.get("deletions", 0)),
            statuses=tuple(status_data.get("statuses", [])),
            reviews=tuple(reviews),
            node_id=data.get("node_id", ""),
        )

    def mark_ready(self, snapshot: Snapshot) -> dict[str, Any]:
        if not snapshot.node_id:
            raise FinisherError(f"Missing PR node_id for {snapshot.repo}#{snapshot.pr}")
        query = """
        mutation($id: ID!) {
          markPullRequestReadyForReview(input: {pullRequestId: $id}) {
            pullRequest { number isDraft url }
          }
        }
        """
        result = self.request(
            "POST",
            "/graphql",
            {"query": query, "variables": {"id": snapshot.node_id}},
        )
        if result.get("errors"):
            raise FinisherError(f"mark-ready failed: {result['errors']}")
        return result

    def merge(self, decision: Decision) -> dict[str, Any]:
        snap, target = decision.snapshot, decision.target
        result = self.request(
            "PUT",
            f"/repos/{snap.repo}/pulls/{snap.pr}/merge",
            {
                "merge_method": target.merge_method,
                "sha": snap.head_sha,
                "commit_title": f"Finish {snap.repo}#{snap.pr}: {snap.title}",
                "commit_message": "Closed by AKOS Finisher after deterministic readiness scan.",
            },
        )
        if not result.get("merged"):
            raise FinisherError(
                f"GitHub did not merge {snap.repo}#{snap.pr}: {result.get('message', result)}"
            )
        return result

    def close(self, decision: Decision) -> dict[str, Any]:
        snap = decision.snapshot
        return self.request(
            "PATCH",
            f"/repos/{snap.repo}/pulls/{snap.pr}",
            {"state": "closed"},
        )


def parse_timestamp(value: str) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def latest_review_states(reviews: Iterable[dict[str, Any]]) -> dict[str, str]:
    latest: dict[str, tuple[str, str]] = {}
    for review in reviews:
        user = (review.get("user") or {}).get("login")
        state = str(review.get("state", "")).upper()
        submitted = str(review.get("submitted_at") or "")
        if not user or state in {"COMMENTED", "PENDING", "DISMISSED"}:
            continue
        previous = latest.get(user)
        if previous is None or submitted >= previous[0]:
            latest[user] = (submitted, state)
    return {user: state for user, (_, state) in latest.items()}


def evaluate(target: Target, snapshot: Snapshot, policy: Policy) -> Decision:
    hard: list[str] = []
    soft: list[str] = []
    reasons: list[str] = []
    score = 0

    if snapshot.merged:
        hard.append("already_merged")
    elif snapshot.state != "open":
        hard.append(f"pr_state_{snapshot.state}")

    if snapshot.mergeable is False or snapshot.mergeable_state == "dirty":
        hard.append("merge_conflict")
    elif snapshot.mergeable is True:
        score += 25
        reasons.append("GitHub reports the PR mergeable")
    else:
        soft.append("mergeability_pending")

    statuses = {str(s.get("context")): str(s.get("state")) for s in snapshot.statuses}
    failed = sorted(k for k, v in statuses.items() if v in {"failure", "error"})
    pending = sorted(k for k, v in statuses.items() if v == "pending")
    if failed:
        hard.append("failed_checks:" + ",".join(failed))
    if pending:
        hard.append("pending_checks:" + ",".join(pending))

    missing_required = sorted(set(target.required_checks) - set(statuses))
    if missing_required:
        hard.append("missing_required_checks:" + ",".join(missing_required))
    elif statuses:
        if all(v == "success" for v in statuses.values()):
            score += 20
            reasons.append("reported commit statuses are successful")
    elif policy.allow_no_checks:
        score += 10
        soft.append("no_checks_reported")
    else:
        hard.append("no_checks_reported")

    review_states = latest_review_states(snapshot.reviews)
    if "CHANGES_REQUESTED" in review_states.values():
        hard.append("changes_requested")
    else:
        score += 15
        reasons.append("no active changes-requested review")

    approvals = sum(1 for state in review_states.values() if state == "APPROVED")
    if approvals < target.required_approvals:
        hard.append(f"approvals_{approvals}_of_{target.required_approvals}")
    else:
        score += 15
        if target.required_approvals:
            reasons.append(f"required approvals satisfied ({approvals})")

    if snapshot.draft:
        if target.allow_mark_ready:
            soft.append("draft_ready_to_promote")
        else:
            hard.append("draft_not_authorized_for_promotion")
    else:
        score += 15
        reasons.append("PR is already marked ready for review")

    updated = parse_timestamp(snapshot.updated_at)
    if updated:
        age = max(0, (dt.datetime.now(UTC) - updated).days)
        if age >= policy.stale_days:
            score += 10
            reasons.append(f"closure debt is stale ({age} days since update)")

    if snapshot.changed_files > 0:
        score += 5
    if snapshot.commits > 0:
        score += 5

    score = min(score, 100)

    if hard:
        disposition = "BLOCKED"
        next_action = "FIX_BLOCKERS"
    elif snapshot.draft:
        disposition = "FINISHABLE"
        next_action = "MARK_READY"
    elif target.desired_action == "merge":
        disposition = "FINISHABLE"
        next_action = "MERGE"
    elif target.desired_action == "close":
        disposition = "FINISHABLE"
        next_action = "CLOSE"
    else:
        disposition = "REVIEW"
        next_action = "HUMAN_REVIEW"

    return Decision(
        target=target,
        snapshot=snapshot,
        score=score,
        disposition=disposition,
        next_action=next_action,
        hard_blockers=tuple(hard),
        soft_blockers=tuple(soft),
        reasons=tuple(reasons),
    )


def load_config(path: pathlib.Path) -> tuple[Policy, list[Target]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FinisherError(f"Cannot load config {path}: {exc}") from exc

    policy_raw = raw.get("policy", {})
    policy = Policy(
        allow_apply=bool(policy_raw.get("allow_apply", False)),
        max_actions_per_run=max(1, int(policy_raw.get("max_actions_per_run", 1))),
        allow_no_checks=bool(policy_raw.get("allow_no_checks", True)),
        freeze_new_work_when_ready=bool(
            policy_raw.get("freeze_new_work_when_ready", True)
        ),
        stale_days=max(1, int(policy_raw.get("stale_days", 14))),
        output_dir=str(policy_raw.get("output_dir", "finisher/out")),
    )

    targets: list[Target] = []
    seen: set[tuple[str, int]] = set()
    for item in raw.get("targets", []):
        target = Target(
            repo=str(item["repo"]),
            pr=int(item["pr"]),
            desired_action=str(item.get("desired_action", "merge")),
            merge_method=str(item.get("merge_method", "squash")),
            allow_mark_ready=bool(item.get("allow_mark_ready", True)),
            required_approvals=max(0, int(item.get("required_approvals", 0))),
            required_checks=tuple(str(v) for v in item.get("required_checks", [])),
            notes=str(item.get("notes", "")),
        )
        key = (target.repo, target.pr)
        if key in seen:
            raise FinisherError(f"Duplicate target: {target.repo}#{target.pr}")
        if target.desired_action not in {"merge", "close", "review"}:
            raise FinisherError(f"Invalid desired_action for {target.repo}#{target.pr}")
        if target.merge_method not in {"merge", "squash", "rebase"}:
            raise FinisherError(f"Invalid merge_method for {target.repo}#{target.pr}")
        seen.add(key)
        targets.append(target)

    if not targets:
        raise FinisherError("Config contains no targets")
    return policy, targets


def decision_dict(decision: Decision) -> dict[str, Any]:
    return {
        "repo": decision.snapshot.repo,
        "pr": decision.snapshot.pr,
        "title": decision.snapshot.title,
        "url": decision.snapshot.url,
        "head_sha": decision.snapshot.head_sha,
        "score": decision.score,
        "disposition": decision.disposition,
        "next_action": decision.next_action,
        "hard_blockers": list(decision.hard_blockers),
        "soft_blockers": list(decision.soft_blockers),
        "reasons": list(decision.reasons),
        "metrics": {
            "commits": decision.snapshot.commits,
            "changed_files": decision.snapshot.changed_files,
            "additions": decision.snapshot.additions,
            "deletions": decision.snapshot.deletions,
        },
        "target_notes": decision.target.notes,
    }


def write_outputs(policy: Policy, decisions: list[Decision], actions: list[dict[str, Any]]) -> None:
    out = pathlib.Path(policy.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    generated = dt.datetime.now(UTC).isoformat()
    payload = {
        "schema": "akos.finisher.receipt.v1",
        "generated_at": generated,
        "decisions": [decision_dict(d) for d in decisions],
        "actions": actions,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["receipt_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    (out / "FINISH_RECEIPT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    lines = [
        "# AKOS Finish Queue",
        "",
        f"Generated: `{generated}`",
        "",
        "| Rank | Score | State | Next action | Pull request | Blockers |",
        "|---:|---:|---|---|---|---|",
    ]
    ranked = sorted(decisions, key=lambda d: (d.finishable, d.score), reverse=True)
    for rank, decision in enumerate(ranked, 1):
        blockers = "; ".join(decision.hard_blockers) or "none"
        lines.append(
            f"| {rank} | {decision.score} | {decision.disposition} | "
            f"{decision.next_action} | [{decision.snapshot.repo}#{decision.snapshot.pr}]"
            f"({decision.snapshot.url}) | {blockers} |"
        )
    lines.extend(["", "## Rule", "", "Finish before expansion. Completion requires a GitHub receipt."])
    (out / "FINISH_QUEUE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def apply_actions(
    client: GitHubClient,
    policy: Policy,
    decisions: list[Decision],
) -> list[dict[str, Any]]:
    if not policy.allow_apply:
        raise FinisherError("Apply is disabled by config policy.allow_apply=false")
    if os.environ.get("FINISHER_APPLY") != "YES":
        raise FinisherError("Set FINISHER_APPLY=YES to execute closure actions")

    candidates = sorted(
        (d for d in decisions if d.finishable),
        key=lambda d: d.score,
        reverse=True,
    )[: policy.max_actions_per_run]
    actions: list[dict[str, Any]] = []
    for decision in candidates:
        snap = decision.snapshot
        if decision.next_action == "MARK_READY":
            result = client.mark_ready(snap)
        elif decision.next_action == "MERGE":
            result = client.merge(decision)
        elif decision.next_action == "CLOSE":
            result = client.close(decision)
        else:
            continue
        actions.append(
            {
                "repo": snap.repo,
                "pr": snap.pr,
                "action": decision.next_action,
                "expected_head_sha": snap.head_sha,
                "github_result": result,
                "completed_at": dt.datetime.now(UTC).isoformat(),
            }
        )
    return actions


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AKOS deterministic closure engine")
    parser.add_argument(
        "command",
        choices=("scan", "gate", "apply"),
        help="scan queue, enforce expansion gate, or execute bounded actions",
    )
    parser.add_argument(
        "--config",
        default="finisher/config.json",
        help="path to Finisher JSON configuration",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        policy, targets = load_config(pathlib.Path(args.config))
        client = GitHubClient(os.environ.get("GITHUB_TOKEN", ""))
        decisions = [evaluate(target, client.get_pr_snapshot(target), policy) for target in targets]
        actions: list[dict[str, Any]] = []
        if args.command == "apply":
            actions = apply_actions(client, policy, decisions)
        write_outputs(policy, decisions, actions)

        finishable = [d for d in decisions if d.finishable]
        blocked = [d for d in decisions if d.hard_blockers]
        print(
            json.dumps(
                {
                    "targets": len(decisions),
                    "finishable": len(finishable),
                    "blocked": len(blocked),
                    "actions_executed": len(actions),
                    "output_dir": policy.output_dir,
                },
                sort_keys=True,
            )
        )
        if (
            args.command == "gate"
            and policy.freeze_new_work_when_ready
            and finishable
        ):
            print(
                "FINISHER_GATE: finishable work exists; expansion is blocked until closure.",
                file=sys.stderr,
            )
            return 3
        return 0
    except FinisherError as exc:
        print(f"FINISHER_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
