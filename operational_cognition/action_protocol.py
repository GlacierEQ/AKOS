from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable, Mapping


class ActionStage(str, Enum):
    MEMORY = "memory"
    TOOL = "tool"
    CURE = "cure"
    INNOVATE = "innovate"
    RESPOND = "respond"


class AttemptOutcome(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class ActionAttempt:
    stage: ActionStage
    action: str
    outcome: AttemptOutcome
    receipt: str | None = None
    blocker: str | None = None
    reversible: bool = True
    recorded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def validate(self) -> None:
        if not self.action.strip():
            raise ValueError("action must not be empty")
        if self.outcome == AttemptOutcome.SUCCEEDED and not self.receipt:
            raise ValueError("successful attempts require a receipt")
        if self.outcome == AttemptOutcome.BLOCKED and not self.blocker:
            raise ValueError("blocked attempts require an exact blocker")


@dataclass(frozen=True)
class ActionPolicy:
    require_memory_first: bool = True
    require_tool_effort: bool = True
    require_cure_before_report: bool = True
    require_innovation_pass: bool = True
    minimum_cure_attempts: int = 1
    maximum_cure_attempts: int = 5

    def validate(self) -> None:
        if self.minimum_cure_attempts < 1:
            raise ValueError("minimum_cure_attempts must be at least 1")
        if self.maximum_cure_attempts < self.minimum_cure_attempts:
            raise ValueError("maximum_cure_attempts must not be below minimum")


@dataclass(frozen=True)
class ResponseGate:
    allowed: bool
    exact_blocker: str | None
    missing_stages: tuple[ActionStage, ...]
    cure_attempts: int
    successful_cures: int


class MemoryFirstActionProtocol:
    """Enforces memory -> tools -> cure -> innovate -> response.

    Read-only investigation may support a mission, but it cannot satisfy the tool or
    cure stages when a safe authorized mutation, repair, retry, fallback, or creation
    remains available.
    """

    def __init__(self, policy: ActionPolicy | None = None) -> None:
        self.policy = policy or ActionPolicy()
        self.policy.validate()

    def evaluate(self, attempts: Iterable[ActionAttempt]) -> ResponseGate:
        items = list(attempts)
        for item in items:
            item.validate()

        observed = {item.stage for item in items}
        cure_items = [item for item in items if item.stage == ActionStage.CURE]
        successful_cures = sum(item.outcome == AttemptOutcome.SUCCEEDED for item in cure_items)
        missing: list[ActionStage] = []

        if self.policy.require_memory_first and ActionStage.MEMORY not in observed:
            missing.append(ActionStage.MEMORY)
        if self.policy.require_tool_effort and ActionStage.TOOL not in observed:
            missing.append(ActionStage.TOOL)
        if self.policy.require_cure_before_report and len(cure_items) < self.policy.minimum_cure_attempts:
            missing.append(ActionStage.CURE)
        if self.policy.require_innovation_pass and ActionStage.INNOVATE not in observed:
            missing.append(ActionStage.INNOVATE)

        order = [item.stage for item in items]
        if ActionStage.RESPOND in observed:
            response_index = order.index(ActionStage.RESPOND)
            required_before_response = [ActionStage.MEMORY, ActionStage.TOOL, ActionStage.CURE, ActionStage.INNOVATE]
            premature = [stage for stage in required_before_response if stage not in order[:response_index]]
            if premature:
                return ResponseGate(False, "response was attempted before required action stages", tuple(premature), len(cure_items), successful_cures)

        if missing:
            return ResponseGate(False, "required action stages are incomplete", tuple(missing), len(cure_items), successful_cures)

        unresolved = [item for item in cure_items if item.outcome in {AttemptOutcome.FAILED, AttemptOutcome.BLOCKED}]
        exhausted = len(cure_items) >= self.policy.maximum_cure_attempts
        cured = successful_cures > 0
        if unresolved and not cured and not exhausted:
            return ResponseGate(False, "additional bounded cure effort is required before reporting failure", (), len(cure_items), successful_cures)

        return ResponseGate(True, None, (), len(cure_items), successful_cures)

    def receipt(self, attempts: Iterable[ActionAttempt]) -> Mapping[str, object]:
        items = list(attempts)
        gate = self.evaluate(items)
        return {
            "schema": "glaciereq.akos.memory-first-action-receipt.v1",
            "allowed_to_respond": gate.allowed,
            "exact_blocker": gate.exact_blocker,
            "missing_stages": [stage.value for stage in gate.missing_stages],
            "cure_attempts": gate.cure_attempts,
            "successful_cures": gate.successful_cures,
            "attempts": [
                {
                    "stage": item.stage.value,
                    "action": item.action,
                    "outcome": item.outcome.value,
                    "receipt": item.receipt,
                    "blocker": item.blocker,
                    "reversible": item.reversible,
                    "recorded_at": item.recorded_at,
                }
                for item in items
            ],
        }
