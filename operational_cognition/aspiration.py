from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AspirationState(str, Enum):
    """Relationship between intended capability and current implementation."""

    VISION = "vision"
    IMPLEMENTATION_GAP = "implementation_gap"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    ABANDONED = "abandoned"
    IMPOSSIBLE_OR_UNSAFE = "impossible_or_unsafe"


class AspirationAction(str, Enum):
    """Default next move for an aspiration assessment."""

    REFINE_TARGET = "refine_target"
    BUILD_TOWARD_TARGET = "build_toward_target"
    VERIFY_IMPLEMENTATION = "verify_implementation"
    PRESERVE_VERIFIED = "preserve_verified"
    PRESERVE_HISTORY = "preserve_history"
    RECORD_CONSTRAINT_AND_ALTERNATIVE = "record_constraint_and_alternative"


@dataclass(frozen=True)
class AspirationAssessment:
    """Classify a target without mistaking incomplete code for a false aspiration.

    A declared target is allowed to be ahead of implementation. Once a concrete
    target specification exists, absence of implementation is an implementation
    gap and the default direction is to build upward toward the target.
    """

    vision: str
    target_spec: str | None = None
    implementation_ref: str | None = None
    verification_ref: str | None = None
    abandoned: bool = False
    constraint_reason: str | None = None

    def validate(self) -> None:
        if not self.vision.strip():
            raise ValueError("vision is required")
        if self.target_spec is not None and not self.target_spec.strip():
            raise ValueError("target_spec must be non-empty when supplied")
        if self.implementation_ref is not None and not self.implementation_ref.strip():
            raise ValueError("implementation_ref must be non-empty when supplied")
        if self.verification_ref is not None and not self.verification_ref.strip():
            raise ValueError("verification_ref must be non-empty when supplied")
        if self.verification_ref and not self.implementation_ref:
            raise ValueError("verification requires an implementation_ref")
        if self.abandoned and self.constraint_reason:
            raise ValueError("abandoned and constrained are distinct terminal states")

    @property
    def state(self) -> AspirationState:
        self.validate()
        if self.abandoned:
            return AspirationState.ABANDONED
        if self.constraint_reason:
            return AspirationState.IMPOSSIBLE_OR_UNSAFE
        if self.verification_ref:
            return AspirationState.VERIFIED
        if self.implementation_ref:
            return AspirationState.IMPLEMENTED
        if self.target_spec:
            return AspirationState.IMPLEMENTATION_GAP
        return AspirationState.VISION

    @property
    def next_action(self) -> AspirationAction:
        return {
            AspirationState.VISION: AspirationAction.REFINE_TARGET,
            AspirationState.IMPLEMENTATION_GAP: AspirationAction.BUILD_TOWARD_TARGET,
            AspirationState.IMPLEMENTED: AspirationAction.VERIFY_IMPLEMENTATION,
            AspirationState.VERIFIED: AspirationAction.PRESERVE_VERIFIED,
            AspirationState.ABANDONED: AspirationAction.PRESERVE_HISTORY,
            AspirationState.IMPOSSIBLE_OR_UNSAFE: (
                AspirationAction.RECORD_CONSTRAINT_AND_ALTERNATIVE
            ),
        }[self.state]

    @property
    def should_rewrite_target_downward(self) -> bool:
        """Downward rewriting is never the default repair for incomplete code."""

        return False

    def as_dict(self) -> dict[str, str | bool | None]:
        return {
            "vision": self.vision,
            "target_spec": self.target_spec,
            "implementation_ref": self.implementation_ref,
            "verification_ref": self.verification_ref,
            "abandoned": self.abandoned,
            "constraint_reason": self.constraint_reason,
            "state": self.state.value,
            "next_action": self.next_action.value,
            "should_rewrite_target_downward": self.should_rewrite_target_downward,
        }
