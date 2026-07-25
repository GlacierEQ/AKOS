from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Sequence


class BranchDisposition(str, Enum):
    ALIVE = "alive"
    ABSORB = "absorb"
    TRANSPLANT = "transplant"
    QUARANTINE = "quarantine"
    DISCARD = "discard"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class BranchAssessment:
    repository: str
    branch: str
    canonical_branch: str
    head_sha: str
    ahead_by: int
    behind_by: int
    changed_files: tuple[str, ...] = ()
    associated_pr: int | None = None
    merge_conflict: bool = False
    verified: bool = False
    security_or_secret_risk: bool = False
    duplicate_or_superseded: bool = False
    belongs_here: bool = True
    destination_repository: str | None = None
    destination_branch: str = "main"
    notes: str | None = None

    def validate(self) -> None:
        for name, value in {
            "repository": self.repository,
            "branch": self.branch,
            "canonical_branch": self.canonical_branch,
            "head_sha": self.head_sha,
        }.items():
            if not value.strip():
                raise ValueError(f"{name} is required")
        if self.ahead_by < 0 or self.behind_by < 0:
            raise ValueError("ahead_by and behind_by cannot be negative")
        if self.destination_repository == self.repository and not self.belongs_here:
            raise ValueError(
                "a branch marked as belonging elsewhere cannot target the same repository"
            )


@dataclass(frozen=True)
class StrandDecision:
    disposition: BranchDisposition
    reason: str
    source_repository: str
    source_branch: str
    source_sha: str
    destination_repository: str | None = None
    destination_branch: str | None = None
    required_actions: tuple[str, ...] = ()
    deletion_allowed: bool = False
    exact_blocker: str | None = None


@dataclass(frozen=True)
class ExtinctionReceipt:
    repository: str
    branch: str
    source_sha: str
    disposition: BranchDisposition
    destination_repository: str | None
    destination_sha: str | None
    verification_receipt: str | None
    lineage_receipt: str | None
    pr_closed: bool
    ref_aligned: bool
    provider_deleted: bool


@dataclass(frozen=True)
class ExtinctionGateResult:
    safe_to_delete: bool
    exact_blocker: str | None
    missing_requirements: tuple[str, ...]


class MasterStrandEngine:
    """Classify branch value and prevent hidden progress or premature deletion."""

    def decide(self, assessment: BranchAssessment) -> StrandDecision:
        try:
            assessment.validate()
        except ValueError as exc:
            return StrandDecision(
                disposition=BranchDisposition.BLOCKED,
                reason="invalid_branch_assessment",
                source_repository=assessment.repository,
                source_branch=assessment.branch,
                source_sha=assessment.head_sha,
                exact_blocker=str(exc),
            )

        if assessment.branch == assessment.canonical_branch:
            return StrandDecision(
                disposition=BranchDisposition.ALIVE,
                reason="canonical_working_face",
                source_repository=assessment.repository,
                source_branch=assessment.branch,
                source_sha=assessment.head_sha,
                destination_repository=assessment.repository,
                destination_branch=assessment.canonical_branch,
                deletion_allowed=False,
            )

        if assessment.security_or_secret_risk:
            return StrandDecision(
                disposition=BranchDisposition.QUARANTINE,
                reason="unsafe_content_requires_preserved_nonactive_lineage",
                source_repository=assessment.repository,
                source_branch=assessment.branch,
                source_sha=assessment.head_sha,
                required_actions=(
                    "preserve exact source SHA and risk classification",
                    "extract only reviewed safe function",
                    "rotate or remove exposed credentials where applicable",
                    "verify the clean destination mainline",
                    "record quarantine and supersession receipts",
                ),
                deletion_allowed=False,
            )

        if assessment.ahead_by == 0 and not assessment.changed_files:
            return StrandDecision(
                disposition=BranchDisposition.DISCARD,
                reason="no_unique_progress",
                source_repository=assessment.repository,
                source_branch=assessment.branch,
                source_sha=assessment.head_sha,
                destination_repository=assessment.repository,
                destination_branch=assessment.canonical_branch,
                required_actions=(
                    "record source SHA and zero-unique-progress comparison",
                    "close associated PR when present",
                    "align the obsolete ref to canonical head",
                    "delete the obsolete ref",
                ),
                deletion_allowed=True,
            )

        if assessment.duplicate_or_superseded:
            return StrandDecision(
                disposition=BranchDisposition.DISCARD,
                reason="unique_delta_is_duplicate_or_superseded",
                source_repository=assessment.repository,
                source_branch=assessment.branch,
                source_sha=assessment.head_sha,
                destination_repository=assessment.repository,
                destination_branch=assessment.canonical_branch,
                required_actions=(
                    "identify the canonical replacement commit",
                    "record supersession lineage",
                    "close associated PR when present",
                    "align and delete the obsolete ref",
                ),
                deletion_allowed=False,
                exact_blocker=(
                    "deletion requires the canonical replacement commit and lineage receipt"
                ),
            )

        if not assessment.belongs_here:
            if not assessment.destination_repository:
                return StrandDecision(
                    disposition=BranchDisposition.BLOCKED,
                    reason="destination_repository_unresolved",
                    source_repository=assessment.repository,
                    source_branch=assessment.branch,
                    source_sha=assessment.head_sha,
                    exact_blocker=(
                        "valuable function belongs elsewhere but no destination repository "
                        "has been identified"
                    ),
                    required_actions=(
                        "classify the capability by repository responsibility and data ownership",
                        "select the canonical destination repository",
                    ),
                )
            return StrandDecision(
                disposition=BranchDisposition.TRANSPLANT,
                reason="valuable_function_belongs_to_another_pillar",
                source_repository=assessment.repository,
                source_branch=assessment.branch,
                source_sha=assessment.head_sha,
                destination_repository=assessment.destination_repository,
                destination_branch=assessment.destination_branch,
                required_actions=(
                    "extract the exact functional delta and tests",
                    "apply it directly to the destination canonical mainline",
                    "verify destination behavior and interfaces",
                    "record source-to-destination lineage",
                    "close associated PR when present",
                    "align and delete the source ref",
                ),
                deletion_allowed=False,
                exact_blocker="destination verification and lineage receipt required",
            )

        if assessment.merge_conflict:
            return StrandDecision(
                disposition=BranchDisposition.ABSORB,
                reason="valuable_delta_requires_manual_reconstruction_on_main",
                source_repository=assessment.repository,
                source_branch=assessment.branch,
                source_sha=assessment.head_sha,
                destination_repository=assessment.repository,
                destination_branch=assessment.canonical_branch,
                required_actions=(
                    "identify exact valuable files, behavior, tests, and interfaces",
                    "reapply the functional delta directly to canonical mainline",
                    "verify the reconstructed behavior",
                    "record source SHA and destination commit lineage",
                    "close associated PR when present",
                    "align and delete the obsolete ref",
                ),
                deletion_allowed=False,
                exact_blocker="manual absorption and verification required",
            )

        return StrandDecision(
            disposition=BranchDisposition.ABSORB,
            reason=(
                "verified_function_ready_for_mainline"
                if assessment.verified
                else "functional_delta_requires_mainline_verification"
            ),
            source_repository=assessment.repository,
            source_branch=assessment.branch,
            source_sha=assessment.head_sha,
            destination_repository=assessment.repository,
            destination_branch=assessment.canonical_branch,
            required_actions=(
                "integrate the complete functional delta into canonical mainline",
                "run acceptance and regression verification",
                "record provider and lineage receipts",
                "close associated PR when present",
                "align and delete the obsolete ref",
            ),
            deletion_allowed=False,
            exact_blocker=(
                None if assessment.verified else "mainline verification receipt required"
            ),
        )


class BranchExtinctionGate:
    """Require retained value, verification, and lineage before ref deletion."""

    def evaluate(self, receipt: ExtinctionReceipt) -> ExtinctionGateResult:
        missing: list[str] = []

        if receipt.disposition == BranchDisposition.ALIVE:
            missing.append("canonical working face cannot be deleted")

        retained_value_required = receipt.disposition in {
            BranchDisposition.ABSORB,
            BranchDisposition.TRANSPLANT,
        }
        if retained_value_required and not receipt.destination_sha:
            missing.append("destination commit SHA")
        if retained_value_required and not receipt.verification_receipt:
            missing.append("destination verification receipt")

        if receipt.disposition in {
            BranchDisposition.ABSORB,
            BranchDisposition.TRANSPLANT,
            BranchDisposition.QUARANTINE,
            BranchDisposition.DISCARD,
        } and not receipt.lineage_receipt:
            missing.append("lineage or disposition receipt")

        if not receipt.ref_aligned:
            missing.append("obsolete ref aligned to canonical destination")

        if receipt.disposition == BranchDisposition.BLOCKED:
            missing.append("resolved branch disposition")

        return ExtinctionGateResult(
            safe_to_delete=not missing,
            exact_blocker=(
                None
                if not missing
                else "branch deletion blocked: " + ", ".join(missing)
            ),
            missing_requirements=tuple(missing),
        )


def summarize_decisions(
    decisions: Iterable[StrandDecision],
) -> dict[str, object]:
    items = tuple(decisions)
    counts = {
        disposition.value: sum(
            1 for item in items if item.disposition == disposition
        )
        for disposition in BranchDisposition
    }
    return {
        "total": len(items),
        "counts": counts,
        "blocked": [
            {
                "repository": item.source_repository,
                "branch": item.source_branch,
                "blocker": item.exact_blocker,
            }
            for item in items
            if item.disposition == BranchDisposition.BLOCKED
        ],
    }
