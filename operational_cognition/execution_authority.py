from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class AuthorityDisposition(str, Enum):
    """The action AKOS must take after evaluating execution authority."""

    EXECUTE = "execute"
    CONFIRM = "confirm"
    BLOCK = "block"


class ConfirmationTrigger(str, Enum):
    """Conditions that require an explicit operator decision."""

    DESTRUCTIVE_OR_IRREVERSIBLE = "destructive_or_irreversible"
    MATERIAL_AMBIGUITY = "material_ambiguity"
    SCOPE_EXPANSION = "scope_expansion"
    OBJECTIVE_CHANGE = "objective_change"
    UNCONTROLLED_EXTERNAL_EFFECT = "uncontrolled_external_effect"
    LEGAL_OR_PUBLIC_FILING_NOT_REQUESTED = "legal_or_public_filing_not_requested"
    SECRETS_CREDENTIALS_OR_PRIVILEGE_CHANGE = (
        "secrets_credentials_or_privilege_change"
    )
    NEW_COST = "new_cost"
    SERVICE_INTERRUPTION_RISK = "service_interruption_risk"
    ROLLBACK_UNAVAILABLE_OR_UNVERIFIED = "rollback_unavailable_or_unverified"


@dataclass(frozen=True, slots=True)
class ExecutionAuthorityContext:
    """Evidence used to decide whether AKOS executes or asks."""

    beneficial: bool
    objective_preserving: bool
    within_standing_authority: bool
    recoverable: bool
    verified: bool = False
    immediately_verifiable: bool = False
    safe_release_available: bool = False
    confirmation_triggers: tuple[ConfirmationTrigger, ...] = ()

    @classmethod
    def from_triggers(
        cls,
        *,
        beneficial: bool,
        objective_preserving: bool,
        within_standing_authority: bool,
        recoverable: bool,
        verified: bool = False,
        immediately_verifiable: bool = False,
        safe_release_available: bool = False,
        confirmation_triggers: Iterable[ConfirmationTrigger] = (),
    ) -> ExecutionAuthorityContext:
        return cls(
            beneficial=beneficial,
            objective_preserving=objective_preserving,
            within_standing_authority=within_standing_authority,
            recoverable=recoverable,
            verified=verified,
            immediately_verifiable=immediately_verifiable,
            safe_release_available=safe_release_available,
            confirmation_triggers=tuple(confirmation_triggers),
        )


@dataclass(frozen=True, slots=True)
class ExecutionAuthorityDecision:
    disposition: AuthorityDisposition
    reason: str
    next_action: str
    failed_gates: tuple[str, ...] = ()
    confirmation_triggers: tuple[str, ...] = ()
    redundant_confirmation_allowed: bool = False
    stop_at_proposal_allowed: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "disposition": self.disposition.value,
            "reason": self.reason,
            "next_action": self.next_action,
            "failed_gates": list(self.failed_gates),
            "confirmation_triggers": list(self.confirmation_triggers),
            "redundant_confirmation_allowed": self.redundant_confirmation_allowed,
            "stop_at_proposal_allowed": self.stop_at_proposal_allowed,
        }


def decide_execution_authority(
    context: ExecutionAuthorityContext,
) -> ExecutionAuthorityDecision:
    """Apply LAW-011 and the non-destructive auto-apply contract.

    The function deliberately separates three states:

    - ``execute``: standing authority is sufficient; asking again is forbidden.
    - ``confirm``: a real confirmation trigger or authority boundary exists.
    - ``block``: the action lacks benefit or a usable verification path.
    """

    triggers = tuple(trigger.value for trigger in context.confirmation_triggers)
    if triggers:
        return ExecutionAuthorityDecision(
            disposition=AuthorityDisposition.CONFIRM,
            reason="confirmation_trigger_present",
            next_action="request_explicit_confirmation_for_named_trigger",
            confirmation_triggers=triggers,
        )

    confirmation_gates: list[str] = []
    if not context.objective_preserving:
        confirmation_gates.append("objective_preserving")
    if not context.within_standing_authority:
        confirmation_gates.append("within_standing_authority")
    if not context.recoverable:
        confirmation_gates.append("recoverable")

    if confirmation_gates:
        return ExecutionAuthorityDecision(
            disposition=AuthorityDisposition.CONFIRM,
            reason="confirmation_boundary_reached",
            next_action="request_explicit_confirmation_for_failed_boundary",
            failed_gates=tuple(confirmation_gates),
        )

    if not context.beneficial:
        return ExecutionAuthorityDecision(
            disposition=AuthorityDisposition.BLOCK,
            reason="benefit_not_established",
            next_action="do_not_mutate_without_a_material_improvement",
            failed_gates=("beneficial",),
        )

    if not (context.verified or context.immediately_verifiable):
        return ExecutionAuthorityDecision(
            disposition=AuthorityDisposition.BLOCK,
            reason="verification_path_missing",
            next_action="establish_a_verification_path_before_execution",
            failed_gates=("verified_or_immediately_verifiable",),
        )

    next_action = (
        "execute_verify_persist_release_report"
        if context.safe_release_available
        else "execute_verify_persist_report"
    )
    return ExecutionAuthorityDecision(
        disposition=AuthorityDisposition.EXECUTE,
        reason="standing_authority_and_green_gates",
        next_action=next_action,
        redundant_confirmation_allowed=False,
        stop_at_proposal_allowed=False,
    )
