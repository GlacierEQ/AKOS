from __future__ import annotations

from operational_cognition.execution_authority import (
    AuthorityDisposition,
    ConfirmationTrigger,
    ExecutionAuthorityContext,
    decide_execution_authority,
)


def green_context(**overrides: object) -> ExecutionAuthorityContext:
    values: dict[str, object] = {
        "beneficial": True,
        "objective_preserving": True,
        "within_standing_authority": True,
        "recoverable": True,
        "verified": True,
    }
    values.update(overrides)
    return ExecutionAuthorityContext(**values)


def test_green_gates_execute_without_redundant_confirmation() -> None:
    decision = decide_execution_authority(green_context())

    assert decision.disposition is AuthorityDisposition.EXECUTE
    assert decision.reason == "standing_authority_and_green_gates"
    assert decision.next_action == "execute_verify_persist_report"
    assert decision.redundant_confirmation_allowed is False
    assert decision.stop_at_proposal_allowed is False


def test_safe_verified_release_must_not_stop_at_pull_request() -> None:
    decision = decide_execution_authority(
        green_context(safe_release_available=True)
    )

    assert decision.disposition is AuthorityDisposition.EXECUTE
    assert decision.next_action == "execute_verify_persist_release_report"
    assert decision.stop_at_proposal_allowed is False


def test_named_confirmation_trigger_requires_operator_decision() -> None:
    decision = decide_execution_authority(
        green_context(
            confirmation_triggers=(
                ConfirmationTrigger.DESTRUCTIVE_OR_IRREVERSIBLE,
            )
        )
    )

    assert decision.disposition is AuthorityDisposition.CONFIRM
    assert decision.reason == "confirmation_trigger_present"
    assert decision.confirmation_triggers == ("destructive_or_irreversible",)


def test_objective_change_requires_confirmation() -> None:
    decision = decide_execution_authority(
        green_context(objective_preserving=False)
    )

    assert decision.disposition is AuthorityDisposition.CONFIRM
    assert "objective_preserving" in decision.failed_gates


def test_unverified_action_without_verification_path_is_blocked() -> None:
    decision = decide_execution_authority(
        green_context(verified=False, immediately_verifiable=False)
    )

    assert decision.disposition is AuthorityDisposition.BLOCK
    assert decision.reason == "verification_path_missing"


def test_immediately_verifiable_action_may_execute() -> None:
    decision = decide_execution_authority(
        green_context(verified=False, immediately_verifiable=True)
    )

    assert decision.disposition is AuthorityDisposition.EXECUTE
