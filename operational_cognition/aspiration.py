from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AspirationState(str, Enum):
    """Relationship between intended capability and current development state."""

    VISION = "vision"
    IMPLEMENTATION_GAP = "implementation_gap"
    EXPERIMENTAL_PATH = "experimental_path"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    CURRENT_PATH_BLOCKED = "current_path_blocked"


class AspirationAction(str, Enum):
    """Default next move for an aspiration assessment."""

    REFINE_TARGET = "refine_target"
    BUILD_TOWARD_TARGET = "build_toward_target"
    EXPERIMENT_AND_RECOMBINE = "experiment_and_recombine"
    VERIFY_IMPLEMENTATION = "verify_implementation"
    PRESERVE_VERIFIED = "preserve_verified"
    REROUTE_AROUND_BLOCKER = "reroute_around_blocker"


class AudienceScope(str, Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"


class ClaimKind(str, Enum):
    CURRENT_CAPABILITY = "current_capability"
    FUTURE_VISION = "future_vision"


@dataclass(frozen=True)
class AspirationAssessment:
    """Keep aspiration ahead of implementation without confusing the two.

    A target may be far ahead of current code. Missing implementation creates
    development work. A blocked route creates a rerouting obligation. Neither
    condition authorizes rewriting the target downward.
    """

    vision: str
    target_spec: str | None = None
    experimental_ref: str | None = None
    implementation_ref: str | None = None
    verification_ref: str | None = None
    blocked_reason: str | None = None

    def validate(self) -> None:
        if not self.vision.strip():
            raise ValueError("vision is required")
        for name, value in (
            ("target_spec", self.target_spec),
            ("experimental_ref", self.experimental_ref),
            ("implementation_ref", self.implementation_ref),
            ("verification_ref", self.verification_ref),
            ("blocked_reason", self.blocked_reason),
        ):
            if value is not None and not value.strip():
                raise ValueError(f"{name} must be non-empty when supplied")
        if self.verification_ref and not self.implementation_ref:
            raise ValueError("verification requires an implementation_ref")

    @property
    def state(self) -> AspirationState:
        self.validate()
        if self.verification_ref:
            return AspirationState.VERIFIED
        if self.implementation_ref:
            return AspirationState.IMPLEMENTED
        if self.blocked_reason:
            return AspirationState.CURRENT_PATH_BLOCKED
        if self.experimental_ref:
            return AspirationState.EXPERIMENTAL_PATH
        if self.target_spec:
            return AspirationState.IMPLEMENTATION_GAP
        return AspirationState.VISION

    @property
    def next_action(self) -> AspirationAction:
        return {
            AspirationState.VISION: AspirationAction.REFINE_TARGET,
            AspirationState.IMPLEMENTATION_GAP: AspirationAction.BUILD_TOWARD_TARGET,
            AspirationState.EXPERIMENTAL_PATH: (
                AspirationAction.EXPERIMENT_AND_RECOMBINE
            ),
            AspirationState.IMPLEMENTED: AspirationAction.VERIFY_IMPLEMENTATION,
            AspirationState.VERIFIED: AspirationAction.PRESERVE_VERIFIED,
            AspirationState.CURRENT_PATH_BLOCKED: (
                AspirationAction.REROUTE_AROUND_BLOCKER
            ),
        }[self.state]

    @property
    def should_rewrite_target_downward(self) -> bool:
        """Incomplete or blocked implementation never makes downgrade the default."""

        return False

    def as_dict(self) -> dict[str, str | bool | None]:
        return {
            "vision": self.vision,
            "target_spec": self.target_spec,
            "experimental_ref": self.experimental_ref,
            "implementation_ref": self.implementation_ref,
            "verification_ref": self.verification_ref,
            "blocked_reason": self.blocked_reason,
            "state": self.state.value,
            "next_action": self.next_action.value,
            "should_rewrite_target_downward": self.should_rewrite_target_downward,
        }


@dataclass(frozen=True)
class DeploymentCalibration:
    """Apply strict truth calibration only when representing work externally.

    Internal development may carry vision, target specs, gaps, experiments, and
    blocked routes without pretending they are complete. External current-state
    claims require implementation and verification evidence. External vision is
    allowed when explicitly labeled as future vision.
    """

    scope: AudienceScope
    claim_kind: ClaimKind
    statement: str
    implementation_ref: str | None = None
    verification_ref: str | None = None

    def validate(self) -> None:
        if not self.statement.strip():
            raise ValueError("statement is required")

        if self.scope is AudienceScope.INTERNAL:
            return

        if self.claim_kind is ClaimKind.FUTURE_VISION:
            return

        if not self.implementation_ref:
            raise ValueError(
                "external current-capability claim requires implementation_ref"
            )
        if not self.verification_ref:
            raise ValueError(
                "external current-capability claim requires verification_ref"
            )

    @property
    def publishable(self) -> bool:
        try:
            self.validate()
        except ValueError:
            return False
        return True

    @property
    def preserves_aspiration(self) -> bool:
        """Deployment calibration changes representation, never the target itself."""

        return True
