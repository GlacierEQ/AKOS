from operational_cognition.action_protocol import (
    ActionAttempt,
    ActionPolicy,
    ActionStage,
    AttemptOutcome,
    MemoryFirstActionProtocol,
)


def attempt(stage: ActionStage, outcome: AttemptOutcome, *, receipt: str | None = None, blocker: str | None = None) -> ActionAttempt:
    return ActionAttempt(stage=stage, action=f"perform {stage.value}", outcome=outcome, receipt=receipt, blocker=blocker)


def test_blocks_response_without_memory_tool_cure_and_innovation() -> None:
    gate = MemoryFirstActionProtocol().evaluate([])
    assert not gate.allowed
    assert gate.missing_stages == (
        ActionStage.MEMORY,
        ActionStage.TOOL,
        ActionStage.CURE,
        ActionStage.INNOVATE,
    )


def test_blocks_premature_response_even_when_later_attempts_exist() -> None:
    attempts = [
        attempt(ActionStage.RESPOND, AttemptOutcome.SKIPPED),
        attempt(ActionStage.MEMORY, AttemptOutcome.SUCCEEDED, receipt="memory:1"),
        attempt(ActionStage.TOOL, AttemptOutcome.SUCCEEDED, receipt="tool:1"),
        attempt(ActionStage.CURE, AttemptOutcome.SUCCEEDED, receipt="cure:1"),
        attempt(ActionStage.INNOVATE, AttemptOutcome.SUCCEEDED, receipt="innovation:1"),
    ]
    gate = MemoryFirstActionProtocol().evaluate(attempts)
    assert not gate.allowed
    assert gate.exact_blocker == "response was attempted before required action stages"


def test_requires_more_cure_effort_before_failure_report() -> None:
    attempts = [
        attempt(ActionStage.MEMORY, AttemptOutcome.SUCCEEDED, receipt="memory:1"),
        attempt(ActionStage.TOOL, AttemptOutcome.SUCCEEDED, receipt="tool:1"),
        attempt(ActionStage.CURE, AttemptOutcome.FAILED),
        attempt(ActionStage.INNOVATE, AttemptOutcome.SUCCEEDED, receipt="innovation:1"),
    ]
    gate = MemoryFirstActionProtocol(ActionPolicy(maximum_cure_attempts=3)).evaluate(attempts)
    assert not gate.allowed
    assert gate.exact_blocker == "additional bounded cure effort is required before reporting failure"


def test_allows_response_after_successful_cure() -> None:
    attempts = [
        attempt(ActionStage.MEMORY, AttemptOutcome.SUCCEEDED, receipt="memory:1"),
        attempt(ActionStage.TOOL, AttemptOutcome.SUCCEEDED, receipt="tool:1"),
        attempt(ActionStage.CURE, AttemptOutcome.SUCCEEDED, receipt="cure:1"),
        attempt(ActionStage.INNOVATE, AttemptOutcome.SUCCEEDED, receipt="innovation:1"),
    ]
    gate = MemoryFirstActionProtocol().evaluate(attempts)
    assert gate.allowed
    assert gate.successful_cures == 1


def test_allows_truthful_failure_report_after_bounded_exhaustion() -> None:
    policy = ActionPolicy(minimum_cure_attempts=1, maximum_cure_attempts=2)
    attempts = [
        attempt(ActionStage.MEMORY, AttemptOutcome.SUCCEEDED, receipt="memory:1"),
        attempt(ActionStage.TOOL, AttemptOutcome.SUCCEEDED, receipt="tool:1"),
        attempt(ActionStage.CURE, AttemptOutcome.BLOCKED, blocker="provider denied mutation"),
        attempt(ActionStage.CURE, AttemptOutcome.FAILED),
        attempt(ActionStage.INNOVATE, AttemptOutcome.SUCCEEDED, receipt="fallback-designed"),
    ]
    assert MemoryFirstActionProtocol(policy).evaluate(attempts).allowed


def test_receipt_is_machine_readable() -> None:
    attempts = [
        attempt(ActionStage.MEMORY, AttemptOutcome.SUCCEEDED, receipt="memory:1"),
        attempt(ActionStage.TOOL, AttemptOutcome.SUCCEEDED, receipt="tool:1"),
        attempt(ActionStage.CURE, AttemptOutcome.SUCCEEDED, receipt="cure:1"),
        attempt(ActionStage.INNOVATE, AttemptOutcome.SUCCEEDED, receipt="innovation:1"),
    ]
    receipt = MemoryFirstActionProtocol().receipt(attempts)
    assert receipt["schema"] == "glaciereq.akos.memory-first-action-receipt.v1"
    assert receipt["allowed_to_respond"] is True
