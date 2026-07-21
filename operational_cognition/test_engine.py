from __future__ import annotations

import unittest

from operational_cognition.engine import (
    ArtifactReceipt,
    ArtifactStage,
    Capability,
    CognitionRecord,
    DecisionState,
    EvidenceClass,
    OperationClass,
    OperationalCognitionEngine,
    PhaseReceipt,
    PipelinePhase,
    SourceKind,
    WorkItem,
    route_source,
)


def capability(**overrides):
    base = dict(
        name="GitHub",
        systems=frozenset({"github"}),
        operations=frozenset(OperationClass),
        source_kinds=frozenset(SourceKind),
        authoritative_for=frozenset({"github"}),
    )
    base.update(overrides)
    return Capability(**base)


def work(**overrides):
    base = dict(
        work_id="AKOS-WORK-001",
        goal="Update the canonical repository",
        target_system="github",
        operation=OperationClass.MUTATE_REVERSIBLE,
        source_kind=SourceKind.PRIVATE_CONNECTED,
        expected_outcome="a committed operational cognition module",
        operator_authorized=True,
    )
    base.update(overrides)
    return WorkItem(**base)


class OperationalCognitionTests(unittest.TestCase):
    def setUp(self):
        self.engine = OperationalCognitionEngine()

    def test_authoritative_verified_capability_wins(self):
        weak = capability(
            name="Memory",
            systems=frozenset({"*"}),
            authoritative_for=frozenset(),
            verification_supported=False,
            persistence_supported=False,
        )
        strong = capability(name="GitHub")
        selected = self.engine.select_capability(work(), [weak, strong])
        self.assertEqual(selected.name, "GitHub")

    def test_missing_capability_returns_exact_blocker(self):
        record = CognitionRecord(work())
        decision = self.engine.decide(record, [])
        self.assertEqual(decision.state, DecisionState.BLOCKED)
        self.assertIn("mutate_reversible on github", decision.exact_blocker)

    def test_write_requires_operator_authorization(self):
        record = CognitionRecord(work(operator_authorized=False))
        decision = self.engine.decide(record, [capability()])
        self.assertEqual(decision.reason, "write_not_authorized")

    def test_irreversible_action_requires_explicit_approval(self):
        record = CognitionRecord(
            work(operation=OperationClass.MUTATE_IRREVERSIBLE)
        )
        decision = self.engine.decide(record, [capability()])
        self.assertEqual(decision.reason, "explicit_approval_required")

    def test_plan_does_not_substitute_for_execution(self):
        record = CognitionRecord(work())
        record.record_phase(
            PhaseReceipt(
                phase=PipelinePhase.INTAKE,
                actor="AKOS",
                target="github",
                result="plan written",
            )
        )
        decision = self.engine.decide(record, [capability()])
        self.assertEqual(decision.state, DecisionState.EXECUTE)
        self.assertEqual(decision.reason, "target_action_not_yet_executed")

    def test_write_claim_without_provider_receipt_is_blocked(self):
        record = CognitionRecord(work())
        record.record_phase(
            PhaseReceipt(
                phase=PipelinePhase.EXECUTE,
                actor="AKOS",
                target="github",
                result="claimed commit",
            )
        )
        decision = self.engine.decide(record, [capability()])
        self.assertEqual(decision.reason, "provider_receipt_missing")

    def test_verified_but_unpersisted_work_is_not_complete(self):
        record = CognitionRecord(work())
        record.record_phase(
            PhaseReceipt(
                phase=PipelinePhase.EXECUTE,
                actor="AKOS",
                target="github",
                result="commit created",
                provider_receipt="commit:abc123",
            )
        )
        record.record_phase(
            PhaseReceipt(
                phase=PipelinePhase.VALIDATE,
                actor="AKOS",
                target="github",
                result="commit fetched",
                provider_receipt="commit:abc123",
                verified=True,
            )
        )
        decision = self.engine.decide(record, [capability()])
        self.assertEqual(decision.reason, "persistence_required")

    def test_complete_requires_verified_and_persisted_receipts(self):
        record = CognitionRecord(work())
        record.record_phase(
            PhaseReceipt(
                phase=PipelinePhase.EXECUTE,
                actor="AKOS",
                target="github",
                result="commit created",
                provider_receipt="commit:abc123",
            )
        )
        record.record_phase(
            PhaseReceipt(
                phase=PipelinePhase.VALIDATE,
                actor="AKOS",
                target="github",
                result="commit fetched",
                provider_receipt="commit:abc123",
                verified=True,
            )
        )
        record.record_phase(
            PhaseReceipt(
                phase=PipelinePhase.LEDGER,
                actor="AKOS",
                target="github",
                result="receipt committed",
                artifact="ledger/receipt.md",
                persisted=True,
            )
        )
        record.record_phase(
            PhaseReceipt(
                phase=PipelinePhase.HANDOFF,
                actor="AKOS",
                target="operator",
                result="artifact returned",
                persisted=True,
            )
        )
        decision = self.engine.decide(record, [capability()])
        self.assertEqual(decision.state, DecisionState.COMPLETE)

    def test_architect_assertion_is_active_but_not_auto_verified(self):
        record = CognitionRecord(work())
        claim = record.register_claim(
            "The actor continued after notice.",
            EvidenceClass.ARCHITECT_ASSERTION,
            actor="CSEA",
        )
        self.assertTrue(claim.is_active_allegation)
        self.assertFalse(claim.is_verified)

    def test_pipeline_and_artifact_regression_are_rejected(self):
        record = CognitionRecord(work())
        record.record_phase(
            PhaseReceipt(
                phase=PipelinePhase.VALIDATE,
                actor="AKOS",
                target="github",
                result="validated",
            )
        )
        with self.assertRaises(ValueError):
            record.record_phase(
                PhaseReceipt(
                    phase=PipelinePhase.EXECUTE,
                    actor="AKOS",
                    target="github",
                    result="late execution",
                )
            )

        record.record_artifact(
            ArtifactReceipt(
                stage=ArtifactStage.VERIFIED,
                artifact_id="artifact-1",
                result="verified",
            )
        )
        with self.assertRaises(ValueError):
            record.record_artifact(
                ArtifactReceipt(
                    stage=ArtifactStage.PARSED,
                    artifact_id="artifact-1",
                    result="late parse",
                )
            )

    def test_source_routing_is_explicit(self):
        self.assertEqual(
            route_source(SourceKind.PRIVATE_CONNECTED),
            "connected_private_source",
        )
        self.assertEqual(
            route_source(SourceKind.PUBLIC_FRESH),
            "current_public_web_or_primary_api",
        )


if __name__ == "__main__":
    unittest.main()
