from __future__ import annotations

import unittest

from finisher.finisher import Policy, Snapshot, Target, evaluate


def snapshot(**overrides):
    base = dict(
        repo="GlacierEQ/example",
        pr=1,
        title="Finish the thing",
        url="https://github.com/GlacierEQ/example/pull/1",
        state="open",
        draft=False,
        merged=False,
        mergeable=True,
        mergeable_state="clean",
        head_sha="abc123",
        base_ref="main",
        created_at="2026-07-01T00:00:00Z",
        updated_at="2026-07-01T00:00:00Z",
        commits=4,
        changed_files=6,
        additions=100,
        deletions=10,
        statuses=(),
        reviews=(),
        node_id="PR_kwDOexample",
    )
    base.update(overrides)
    return Snapshot(**base)


class FinisherDecisionTests(unittest.TestCase):
    def setUp(self):
        self.policy = Policy(allow_no_checks=True, stale_days=1)
        self.target = Target(repo="GlacierEQ/example", pr=1)

    def test_ready_pr_is_finishable_for_merge(self):
        decision = evaluate(self.target, snapshot(), self.policy)
        self.assertEqual(decision.disposition, "FINISHABLE")
        self.assertEqual(decision.next_action, "MERGE")
        self.assertTrue(decision.finishable)
        self.assertFalse(decision.hard_blockers)

    def test_draft_pr_promotes_before_merge(self):
        decision = evaluate(self.target, snapshot(draft=True), self.policy)
        self.assertEqual(decision.next_action, "MARK_READY")
        self.assertTrue(decision.finishable)
        self.assertIn("draft_ready_to_promote", decision.soft_blockers)

    def test_failed_status_is_hard_blocker(self):
        decision = evaluate(
            self.target,
            snapshot(statuses=({"context": "tests", "state": "failure"},)),
            self.policy,
        )
        self.assertEqual(decision.disposition, "BLOCKED")
        self.assertFalse(decision.finishable)
        self.assertTrue(any(v.startswith("failed_checks:") for v in decision.hard_blockers))

    def test_changes_requested_is_hard_blocker(self):
        reviews = (
            {
                "user": {"login": "reviewer"},
                "state": "CHANGES_REQUESTED",
                "submitted_at": "2026-07-16T00:00:00Z",
            },
        )
        decision = evaluate(self.target, snapshot(reviews=reviews), self.policy)
        self.assertIn("changes_requested", decision.hard_blockers)

    def test_required_approval_must_exist(self):
        target = Target(repo="GlacierEQ/example", pr=1, required_approvals=1)
        decision = evaluate(target, snapshot(), self.policy)
        self.assertIn("approvals_0_of_1", decision.hard_blockers)

    def test_merge_conflict_blocks(self):
        decision = evaluate(
            self.target,
            snapshot(mergeable=False, mergeable_state="dirty"),
            self.policy,
        )
        self.assertIn("merge_conflict", decision.hard_blockers)


if __name__ == "__main__":
    unittest.main()
