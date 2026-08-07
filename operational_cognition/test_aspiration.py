import pytest

from operational_cognition.aspiration import (
    AspirationAction,
    AspirationAssessment,
    AspirationState,
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


def test_constraint_records_alternative_instead_of_silent_downgrade() -> None:
    assessment = AspirationAssessment(
        vision="Perform a capability that current physics prevents",
        target_spec="Implement the desired capability",
        constraint_reason="Physical constraint prevents the target as stated",
    )

    assert assessment.state is AspirationState.IMPOSSIBLE_OR_UNSAFE
    assert (
        assessment.next_action
        is AspirationAction.RECORD_CONSTRAINT_AND_ALTERNATIVE
    )
    assert assessment.should_rewrite_target_downward is False


def test_abandoned_target_preserves_history() -> None:
    assessment = AspirationAssessment(
        vision="Retired objective",
        target_spec="Old target",
        abandoned=True,
    )

    assert assessment.state is AspirationState.ABANDONED
    assert assessment.next_action is AspirationAction.PRESERVE_HISTORY


def test_verification_without_implementation_is_invalid() -> None:
    assessment = AspirationAssessment(
        vision="Verified target",
        target_spec="Target",
        verification_ref="receipt.json",
    )

    with pytest.raises(ValueError, match="verification requires"):
        _ = assessment.state
