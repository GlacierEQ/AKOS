import pytest

from operational_cognition.aspiration import (
    AspirationAction,
    AspirationAssessment,
    AspirationState,
    AudienceScope,
    ClaimKind,
    DeploymentCalibration,
)


def test_vision_without_target_is_refined_not_downgraded() -> None:
    assessment = AspirationAssessment(vision="Build a resumable operating system")

    assert assessment.state is AspirationState.VISION
    assert assessment.next_action is AspirationAction.REFINE_TARGET
    assert assessment.should_rewrite_target_downward is False


def test_target_ahead_of_code_is_an_implementation_gap() -> None:
    assessment = AspirationAssessment(
        vision="Make repository operations fully resumable",
        target_spec="Every mutation emits a durable receipt and recovery checkpoint",
    )

    assert assessment.state is AspirationState.IMPLEMENTATION_GAP
    assert assessment.next_action is AspirationAction.BUILD_TOWARD_TARGET
    assert assessment.should_rewrite_target_downward is False


def test_experimental_path_keeps_aspiration_alive() -> None:
    assessment = AspirationAssessment(
        vision="Give a system durable cross-platform memory",
        target_spec="Continuity survives model and platform boundaries",
        experimental_ref="experiments/memory-bridge.md",
    )

    assert assessment.state is AspirationState.EXPERIMENTAL_PATH
    assert assessment.next_action is AspirationAction.EXPERIMENT_AND_RECOMBINE
    assert assessment.should_rewrite_target_downward is False


def test_blocked_path_triggers_rerouting_not_abandonment() -> None:
    assessment = AspirationAssessment(
        vision="Give a system durable cross-platform memory",
        target_spec="Continuity survives model and platform boundaries",
        blocked_reason="Current provider API does not expose the needed surface",
    )

    assert assessment.state is AspirationState.CURRENT_PATH_BLOCKED
    assert assessment.next_action is AspirationAction.REROUTE_AROUND_BLOCKER
    assert assessment.should_rewrite_target_downward is False


def test_existing_code_moves_to_verification_not_document_reduction() -> None:
    assessment = AspirationAssessment(
        vision="Make repository operations fully resumable",
        target_spec="Every mutation emits a durable receipt and recovery checkpoint",
        implementation_ref="operational_cognition/engine.py",
    )

    assert assessment.state is AspirationState.IMPLEMENTED
    assert assessment.next_action is AspirationAction.VERIFY_IMPLEMENTATION


def test_verified_target_is_preserved() -> None:
    assessment = AspirationAssessment(
        vision="Make repository operations fully resumable",
        target_spec="Every mutation emits a durable receipt and recovery checkpoint",
        implementation_ref="operational_cognition/engine.py",
        verification_ref="receipts/example.json",
    )

    assert assessment.state is AspirationState.VERIFIED
    assert assessment.next_action is AspirationAction.PRESERVE_VERIFIED


def test_internal_development_can_carry_unverified_vision() -> None:
    calibration = DeploymentCalibration(
        scope=AudienceScope.INTERNAL,
        claim_kind=ClaimKind.FUTURE_VISION,
        statement="The target system has durable cross-platform memory.",
    )

    assert calibration.publishable is True
    assert calibration.preserves_aspiration is True


def test_external_future_vision_is_publishable_when_labeled_as_vision() -> None:
    calibration = DeploymentCalibration(
        scope=AudienceScope.EXTERNAL,
        claim_kind=ClaimKind.FUTURE_VISION,
        statement="Roadmap: durable cross-platform memory.",
    )

    assert calibration.publishable is True
    assert calibration.preserves_aspiration is True


def test_external_current_capability_requires_implementation_and_proof() -> None:
    calibration = DeploymentCalibration(
        scope=AudienceScope.EXTERNAL,
        claim_kind=ClaimKind.CURRENT_CAPABILITY,
        statement="The system currently provides durable cross-platform memory.",
    )

    assert calibration.publishable is False
    with pytest.raises(ValueError, match="implementation_ref"):
        calibration.validate()


def test_external_current_capability_passes_with_evidence() -> None:
    calibration = DeploymentCalibration(
        scope=AudienceScope.EXTERNAL,
        claim_kind=ClaimKind.CURRENT_CAPABILITY,
        statement="The system currently provides the tested continuity behavior.",
        implementation_ref="echo/service.py",
        verification_ref="receipts/continuity-test.json",
    )

    assert calibration.publishable is True
    assert calibration.preserves_aspiration is True


def test_verification_without_implementation_is_invalid() -> None:
    assessment = AspirationAssessment(
        vision="Verified target",
        target_spec="Target",
        verification_ref="receipt.json",
    )

    with pytest.raises(ValueError, match="verification requires"):
        _ = assessment.state
