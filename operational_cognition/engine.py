from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable, Mapping, Sequence


class EvidenceClass(str, Enum):
    VERIFIED_FACT = "verified_fact"
    ARCHITECT_ASSERTION = "architect_assertion"
    CORROBORATED_ASSERTION = "corroborated_assertion"
    RECORD_CONTROLLED_ALLEGATION = "record_controlled_allegation"
    ADVERSE_DOCUMENTARY_CONTRADICTION = "adverse_documentary_contradiction"
    MISSING_REQUIRED_RECORD = "missing_required_record"
    INFERENCE = "inference"
    DISPUTED_ACTOR_NARRATIVE = "disputed_actor_narrative"


class OperationClass(str, Enum):
    READ = "read"
    ANALYZE = "analyze"
    MUTATE_REVERSIBLE = "mutate_reversible"
    MUTATE_IRREVERSIBLE = "mutate_irreversible"
    EXTERNAL_SEND = "external_send"
    LEGAL_FILE = "legal_file"


class PipelinePhase(str, Enum):
    INTAKE = "intake"
    BIND = "bind"
    ROUTE = "route"
    EXECUTE = "execute"
    VALIDATE = "validate"
    REVIEW = "review"
    RELEASE = "release"
    LEDGER = "ledger"
    HANDOFF = "handoff"


class ArtifactStage(str, Enum):
    LOCATED = "located"
    ACQUIRED = "acquired"
    HASHED = "hashed"
    PRESERVED = "preserved"
    PARSED = "parsed"
    CLASSIFIED = "classified"
    CORRELATED = "correlated"
    DRAFTED = "drafted"
    VERIFIED = "verified"
    PACKAGED = "packaged"
    STORED = "stored"
    LOGGED = "logged"
    READY_FOR_USE = "ready_for_use"


class DecisionState(str, Enum):
    EXECUTE = "execute"
    BLOCKED = "blocked"
    COMPLETE = "complete"


class SourceKind(str, Enum):
    PRIVATE_CONNECTED = "private_connected"
    CONVERSATION_FILE = "conversation_file"
    PUBLIC_FRESH = "public_fresh"
    STATIC_GENERAL = "static_general"
    LOCAL_RUNTIME = "local_runtime"


SENSITIVE_OPERATIONS = {
    OperationClass.MUTATE_IRREVERSIBLE,
    OperationClass.EXTERNAL_SEND,
    OperationClass.LEGAL_FILE,
}

WRITE_OPERATIONS = {
    OperationClass.MUTATE_REVERSIBLE,
    OperationClass.MUTATE_IRREVERSIBLE,
    OperationClass.EXTERNAL_SEND,
    OperationClass.LEGAL_FILE,
}

PIPELINE_ORDER = {phase: index for index, phase in enumerate(PipelinePhase)}
ARTIFACT_ORDER = {stage: index for index, stage in enumerate(ArtifactStage)}


@dataclass(frozen=True)
class Claim:
    text: str
    evidence_class: EvidenceClass
    source_ref: str | None = None
    actor: str | None = None
    recorded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def is_active_allegation(self) -> bool:
        return self.evidence_class in {
            EvidenceClass.ARCHITECT_ASSERTION,
            EvidenceClass.CORROBORATED_ASSERTION,
            EvidenceClass.RECORD_CONTROLLED_ALLEGATION,
            EvidenceClass.ADVERSE_DOCUMENTARY_CONTRADICTION,
            EvidenceClass.MISSING_REQUIRED_RECORD,
        }

    @property
    def is_verified(self) -> bool:
        return self.evidence_class == EvidenceClass.VERIFIED_FACT


@dataclass(frozen=True)
class Capability:
    name: str
    systems: frozenset[str]
    operations: frozenset[OperationClass]
    source_kinds: frozenset[SourceKind] = frozenset(SourceKind)
    connected: bool = True
    authenticated: bool = True
    verification_supported: bool = True
    persistence_supported: bool = True
    authoritative_for: frozenset[str] = frozenset()

    def supports(self, target_system: str, operation: OperationClass) -> bool:
        return (
            self.connected
            and self.authenticated
            and operation in self.operations
            and (target_system in self.systems or "*" in self.systems)
        )

    def score(
        self,
        *,
        target_system: str,
        operation: OperationClass,
        source_kind: SourceKind,
    ) -> int:
        if not self.supports(target_system, operation):
            return -1

        score = 100
        if source_kind in self.source_kinds:
            score += 20
        if target_system in self.authoritative_for:
            score += 30
        if self.verification_supported:
            score += 10
        if self.persistence_supported:
            score += 10
        return score


@dataclass(frozen=True)
class WorkItem:
    work_id: str
    goal: str
    target_system: str
    operation: OperationClass
    source_kind: SourceKind
    expected_outcome: str
    operator_authorized: bool = True
    explicit_approval: bool = False
    requires_persistence: bool = True
    requires_verification: bool = True

    def validate(self) -> None:
        fields = {
            "work_id": self.work_id,
            "goal": self.goal,
            "target_system": self.target_system,
            "expected_outcome": self.expected_outcome,
        }
        missing = [name for name, value in fields.items() if not value.strip()]
        if missing:
            raise ValueError(f"missing required work fields: {', '.join(missing)}")


@dataclass(frozen=True)
class PhaseReceipt:
    phase: PipelinePhase
    actor: str
    target: str
    result: str
    source: str | None = None
    artifact: str | None = None
    provider_receipt: str | None = None
    content_hash: str | None = None
    verified: bool = False
    persisted: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(frozen=True)
class ArtifactReceipt:
    stage: ArtifactStage
    artifact_id: str
    result: str
    content_hash: str | None = None
    location: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(frozen=True)
class Decision:
    state: DecisionState
    reason: str
    next_action: str | None = None
    capability: str | None = None
    exact_blocker: str | None = None


@dataclass
class CognitionRecord:
    work: WorkItem
    claims: list[Claim] = field(default_factory=list)
    phase_receipts: dict[PipelinePhase, PhaseReceipt] = field(default_factory=dict)
    artifact_receipts: dict[ArtifactStage, ArtifactReceipt] = field(default_factory=dict)

    def register_claim(
        self,
        text: str,
        evidence_class: EvidenceClass,
        *,
        source_ref: str | None = None,
        actor: str | None = None,
    ) -> Claim:
        if not text.strip():
            raise ValueError("claim text must not be empty")
        claim = Claim(
            text=text.strip(),
            evidence_class=evidence_class,
            source_ref=source_ref,
            actor=actor,
        )
        self.claims.append(claim)
        return claim

    def record_phase(self, receipt: PhaseReceipt) -> None:
        if receipt.phase in self.phase_receipts:
            raise ValueError(f"phase already recorded: {receipt.phase.value}")

        prior = [PIPELINE_ORDER[phase] for phase in self.phase_receipts]
        if prior and PIPELINE_ORDER[receipt.phase] < max(prior):
            raise ValueError(
                f"pipeline regression: {receipt.phase.value} follows a later phase"
            )
        self.phase_receipts[receipt.phase] = receipt

    def record_artifact(self, receipt: ArtifactReceipt) -> None:
        if receipt.stage in self.artifact_receipts:
            raise ValueError(f"artifact stage already recorded: {receipt.stage.value}")

        prior = [ARTIFACT_ORDER[stage] for stage in self.artifact_receipts]
        if prior and ARTIFACT_ORDER[receipt.stage] < max(prior):
            raise ValueError(
                f"artifact regression: {receipt.stage.value} follows a later stage"
            )
        self.artifact_receipts[receipt.stage] = receipt

    def has_verified_execution(self) -> bool:
        receipt = self.phase_receipts.get(PipelinePhase.VALIDATE)
        return bool(receipt and receipt.verified and receipt.provider_receipt)

    def has_persisted_ledger(self) -> bool:
        ledger = self.phase_receipts.get(PipelinePhase.LEDGER)
        handoff = self.phase_receipts.get(PipelinePhase.HANDOFF)
        return bool(
            ledger
            and ledger.persisted
            and ledger.artifact
            and handoff
            and handoff.persisted
        )


class OperationalCognitionEngine:
    """Deterministic policy engine for execution-first AKOS cognition."""

    def select_capability(
        self,
        work: WorkItem,
        capabilities: Iterable[Capability],
    ) -> Capability | None:
        ranked = sorted(
            capabilities,
            key=lambda capability: capability.score(
                target_system=work.target_system,
                operation=work.operation,
                source_kind=work.source_kind,
            ),
            reverse=True,
        )
        if not ranked:
            return None

        top = ranked[0]
        return top if top.score(
            target_system=work.target_system,
            operation=work.operation,
            source_kind=work.source_kind,
        ) >= 0 else None

    def decide(
        self,
        record: CognitionRecord,
        capabilities: Sequence[Capability],
    ) -> Decision:
        try:
            record.work.validate()
        except ValueError as exc:
            return Decision(
                state=DecisionState.BLOCKED,
                reason="invalid_work_item",
                exact_blocker=str(exc),
            )

        capability = self.select_capability(record.work, capabilities)
        if capability is None:
            return Decision(
                state=DecisionState.BLOCKED,
                reason="no_usable_capability",
                exact_blocker=(
                    f"no connected authenticated capability supports "
                    f"{record.work.operation.value} on {record.work.target_system}"
                ),
            )

        if (
            record.work.operation in WRITE_OPERATIONS
            and not record.work.operator_authorized
        ):
            return Decision(
                state=DecisionState.BLOCKED,
                reason="write_not_authorized",
                capability=capability.name,
                exact_blocker="operator authorization is required for target-system mutation",
            )

        if (
            record.work.operation in SENSITIVE_OPERATIONS
            and not record.work.explicit_approval
        ):
            return Decision(
                state=DecisionState.BLOCKED,
                reason="explicit_approval_required",
                capability=capability.name,
                exact_blocker=(
                    f"explicit approval is required for "
                    f"{record.work.operation.value}"
                ),
            )

        execute = record.phase_receipts.get(PipelinePhase.EXECUTE)
        if execute is None:
            return Decision(
                state=DecisionState.EXECUTE,
                reason="target_action_not_yet_executed",
                capability=capability.name,
                next_action=(
                    f"use {capability.name} to perform the smallest target-system "
                    f"action that produces: {record.work.expected_outcome}"
                ),
            )

        if record.work.operation in WRITE_OPERATIONS and not execute.provider_receipt:
            return Decision(
                state=DecisionState.BLOCKED,
                reason="provider_receipt_missing",
                capability=capability.name,
                exact_blocker=(
                    "a target-system write was claimed without a provider receipt"
                ),
            )

        if record.work.requires_verification and not record.has_verified_execution():
            return Decision(
                state=DecisionState.EXECUTE,
                reason="verification_required",
                capability=capability.name,
                next_action=(
                    "verify the result in the authoritative target system and "
                    "record the provider receipt"
                ),
            )

        if record.work.requires_persistence and not record.has_persisted_ledger():
            return Decision(
                state=DecisionState.EXECUTE,
                reason="persistence_required",
                capability=capability.name,
                next_action=(
                    "persist the execution receipt, artifact pointer, and handoff "
                    "in the canonical ledger"
                ),
            )

        return Decision(
            state=DecisionState.COMPLETE,
            reason="verified_and_persisted",
            capability=capability.name,
        )


def route_source(kind: SourceKind) -> str:
    """Return the canonical source-selection rule for a request."""
    return {
        SourceKind.PRIVATE_CONNECTED: "connected_private_source",
        SourceKind.CONVERSATION_FILE: "files_surface",
        SourceKind.PUBLIC_FRESH: "current_public_web_or_primary_api",
        SourceKind.STATIC_GENERAL: "model_reasoning_or_primary_reference",
        SourceKind.LOCAL_RUNTIME: "container_or_repository_runtime",
    }[kind]


def completion_summary(
    record: CognitionRecord,
    decision: Decision,
) -> Mapping[str, object]:
    """Return the minimum machine-readable operator summary."""
    return {
        "work_id": record.work.work_id,
        "state": decision.state.value,
        "completed": decision.state == DecisionState.COMPLETE,
        "reason": decision.reason,
        "capability": decision.capability,
        "next_action": decision.next_action,
        "exact_blocker": decision.exact_blocker,
        "claims": [
            {
                "text": claim.text,
                "evidence_class": claim.evidence_class.value,
                "active_allegation": claim.is_active_allegation,
                "verified": claim.is_verified,
                "source_ref": claim.source_ref,
                "actor": claim.actor,
            }
            for claim in record.claims
        ],
        "phase_receipts": [
            receipt.phase.value for receipt in record.phase_receipts.values()
        ],
        "artifact_stages": [
            receipt.stage.value for receipt in record.artifact_receipts.values()
        ],
    }
