from __future__ import annotations

import unittest

from operational_cognition.engine import ArtifactStage
from operational_cognition.maturity import (
    ArtifactClosureGate,
    CapabilityLedger,
    CapabilityReceipt,
    CapabilityState,
    ControlEvidence,
    EvidenceLevel,
    MaturityBand,
    MaturityDimension,
    ReceiptGroundedScorecard,
    standard_maturity_controls,
)


class OperationalMaturityTests(unittest.TestCase):
    def test_capability_requires_provider_receipt_at_return(self):
        ledger = CapabilityLedger("GitHub")
        ledger.record(
            CapabilityReceipt(
                "GitHub",
                CapabilityState.DISCOVERED,
                "repo:GlacierEQ/AKOS",
            )
        )
        with self.assertRaises(ValueError):
            ledger.record(
                CapabilityReceipt(
                    "GitHub",
                    CapabilityState.RETURNED,
                    "repo:GlacierEQ/AKOS",
                )
            )

    def test_capability_persisted_is_operational(self):
        ledger = CapabilityLedger("GitHub")
        ledger.record(
            CapabilityReceipt(
                "GitHub",
                CapabilityState.DISCOVERED,
                "repo:GlacierEQ/AKOS",
            )
        )
        ledger.record(
            CapabilityReceipt(
                "GitHub",
                CapabilityState.RETURNED,
                "repo:GlacierEQ/AKOS",
                provider_receipt="commit:1",
            )
        )
        ledger.record(
            CapabilityReceipt(
                "GitHub",
                CapabilityState.VERIFIED,
                "repo:GlacierEQ/AKOS",
                provider_receipt="commit:1",
            )
        )
        ledger.record(
            CapabilityReceipt(
                "GitHub",
                CapabilityState.PERSISTED,
                "repo:GlacierEQ/AKOS",
                provider_receipt="commit:1",
                artifact_ref="ledger/1.json",
            )
        )
        self.assertTrue(ledger.fully_operational)
        self.assertEqual(ledger.missing_states(), ())

    def test_capability_regression_is_rejected(self):
        ledger = CapabilityLedger("GitHub")
        ledger.record(
            CapabilityReceipt(
                "GitHub",
                CapabilityState.VERIFIED,
                "repo:GlacierEQ/AKOS",
                provider_receipt="commit:1",
            )
        )
        with self.assertRaises(ValueError):
            ledger.record(
                CapabilityReceipt(
                    "GitHub",
                    CapabilityState.CONNECTED,
                    "repo:GlacierEQ/AKOS",
                )
            )

    def test_scorecard_separates_ceiling_and_reliability(self):
        controls = [
            control
            for control in standard_maturity_controls()
            if control.dimension == MaturityDimension.TOOL_POWER
        ]
        scorecard = ReceiptGroundedScorecard(controls)
        result = scorecard.assess(
            [
                ControlEvidence(
                    "TOOL-01",
                    EvidenceLevel.VERIFIED,
                    True,
                    "manifests/capabilities.json",
                    provider_receipt="commit:a",
                ),
                ControlEvidence(
                    "TOOL-02",
                    EvidenceLevel.OBSERVED,
                    True,
                    "operational_cognition/maturity.py",
                ),
                ControlEvidence(
                    "TOOL-03",
                    EvidenceLevel.NONE,
                    False,
                    "missing",
                ),
            ]
        )
        dimension = result.dimensions[0]
        self.assertGreater(
            dimension.available_ceiling,
            dimension.demonstrated_reliability,
        )
        self.assertEqual(dimension.controls_available, 2)

    def test_persisted_evidence_requires_artifact(self):
        with self.assertRaises(ValueError):
            ControlEvidence(
                "TOOL-01",
                EvidenceLevel.PERSISTED,
                True,
                "manifests/capabilities.json",
                provider_receipt="commit:a",
            ).validate()

    def test_good_draft_is_not_ready(self):
        result = ArtifactClosureGate().evaluate([ArtifactStage.DRAFTED])
        self.assertFalse(result.ready_for_use)
        self.assertIn(ArtifactStage.VERIFIED, result.missing_stages)
        self.assertIn(ArtifactStage.READY_FOR_USE, result.missing_stages)

    def test_stages_nine_through_twelve_are_not_full_closure(self):
        result = ArtifactClosureGate().evaluate(
            [
                ArtifactStage.VERIFIED,
                ArtifactStage.PACKAGED,
                ArtifactStage.STORED,
                ArtifactStage.LOGGED,
            ]
        )
        self.assertFalse(result.ready_for_use)
        self.assertIn(ArtifactStage.READY_FOR_USE, result.missing_stages)

    def test_full_lifecycle_is_ready(self):
        result = ArtifactClosureGate().evaluate(list(ArtifactStage))
        self.assertTrue(result.ready_for_use)
        self.assertIsNone(result.exact_blocker)

    def test_subjective_score_is_unassessed_without_receipts(self):
        controls = [
            control
            for control in standard_maturity_controls()
            if control.dimension == MaturityDimension.MODEL_CAPABILITY
        ]
        result = ReceiptGroundedScorecard(controls).assess([])
        self.assertEqual(result.dimensions[0].band, MaturityBand.UNASSESSED)
        self.assertEqual(
            result.dimensions[0].demonstrated_reliability,
            0.0,
        )

    def test_unknown_control_is_rejected(self):
        scorecard = ReceiptGroundedScorecard(standard_maturity_controls())
        with self.assertRaises(ValueError):
            scorecard.assess(
                [
                    ControlEvidence(
                        "MADE-UP-01",
                        EvidenceLevel.OBSERVED,
                        True,
                        "chat",
                    )
                ]
            )


if __name__ == "__main__":
    unittest.main()
