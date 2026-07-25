from __future__ import annotations

import unittest

from operational_cognition.master_strand import (
    BranchAssessment,
    BranchDisposition,
    BranchExtinctionGate,
    ExtinctionReceipt,
    MasterStrandEngine,
)


class MasterStrandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = MasterStrandEngine()
        self.gate = BranchExtinctionGate()

    def assessment(self, **overrides) -> BranchAssessment:
        base = dict(
            repository="GlacierEQ/AKOS",
            branch="feature/power",
            canonical_branch="main",
            head_sha="a" * 40,
            ahead_by=2,
            behind_by=0,
            changed_files=("runtime.py", "test_runtime.py"),
        )
        base.update(overrides)
        return BranchAssessment(**base)

    def test_canonical_mainline_is_alive(self) -> None:
        decision = self.engine.decide(
            self.assessment(branch="main", canonical_branch="main")
        )
        self.assertEqual(decision.disposition, BranchDisposition.ALIVE)
        self.assertFalse(decision.deletion_allowed)

    def test_zero_unique_progress_is_discardable(self) -> None:
        decision = self.engine.decide(
            self.assessment(ahead_by=0, changed_files=())
        )
        self.assertEqual(decision.disposition, BranchDisposition.DISCARD)
        self.assertTrue(decision.deletion_allowed)

    def test_wrong_repo_function_is_transplanted(self) -> None:
        decision = self.engine.decide(
            self.assessment(
                belongs_here=False,
                destination_repository="GlacierEQ/FILEBOSS",
            )
        )
        self.assertEqual(decision.disposition, BranchDisposition.TRANSPLANT)
        self.assertEqual(
            decision.destination_repository,
            "GlacierEQ/FILEBOSS",
        )
        self.assertFalse(decision.deletion_allowed)

    def test_unresolved_destination_blocks(self) -> None:
        decision = self.engine.decide(
            self.assessment(belongs_here=False, destination_repository=None)
        )
        self.assertEqual(decision.disposition, BranchDisposition.BLOCKED)
        self.assertIn("no destination repository", decision.exact_blocker)

    def test_conflict_reconstructs_function_on_main(self) -> None:
        decision = self.engine.decide(
            self.assessment(merge_conflict=True)
        )
        self.assertEqual(decision.disposition, BranchDisposition.ABSORB)
        self.assertIn("manual", decision.reason)
        self.assertFalse(decision.deletion_allowed)

    def test_secret_risk_quarantines(self) -> None:
        decision = self.engine.decide(
            self.assessment(security_or_secret_risk=True)
        )
        self.assertEqual(decision.disposition, BranchDisposition.QUARANTINE)
        self.assertFalse(decision.deletion_allowed)

    def test_delete_gate_requires_destination_and_receipts(self) -> None:
        result = self.gate.evaluate(
            ExtinctionReceipt(
                repository="GlacierEQ/AKOS",
                branch="feature/power",
                source_sha="a" * 40,
                disposition=BranchDisposition.ABSORB,
                destination_repository="GlacierEQ/AKOS",
                destination_sha=None,
                verification_receipt=None,
                lineage_receipt=None,
                pr_closed=False,
                ref_aligned=False,
                provider_deleted=False,
            )
        )
        self.assertFalse(result.safe_to_delete)
        self.assertIn("destination commit SHA", result.missing_requirements)
        self.assertIn("destination verification receipt", result.missing_requirements)

    def test_delete_gate_opens_after_verified_absorption(self) -> None:
        result = self.gate.evaluate(
            ExtinctionReceipt(
                repository="GlacierEQ/AKOS",
                branch="feature/power",
                source_sha="a" * 40,
                disposition=BranchDisposition.ABSORB,
                destination_repository="GlacierEQ/AKOS",
                destination_sha="b" * 40,
                verification_receipt="runner:job-1",
                lineage_receipt="ledger:branch-1",
                pr_closed=True,
                ref_aligned=True,
                provider_deleted=False,
            )
        )
        self.assertTrue(result.safe_to_delete)
        self.assertIsNone(result.exact_blocker)

    def test_canonical_branch_cannot_be_deleted(self) -> None:
        result = self.gate.evaluate(
            ExtinctionReceipt(
                repository="GlacierEQ/AKOS",
                branch="main",
                source_sha="a" * 40,
                disposition=BranchDisposition.ALIVE,
                destination_repository="GlacierEQ/AKOS",
                destination_sha="a" * 40,
                verification_receipt="runner:job-1",
                lineage_receipt="ledger:main",
                pr_closed=True,
                ref_aligned=True,
                provider_deleted=False,
            )
        )
        self.assertFalse(result.safe_to_delete)
        self.assertIn(
            "canonical working face cannot be deleted",
            result.missing_requirements,
        )


if __name__ == "__main__":
    unittest.main()
