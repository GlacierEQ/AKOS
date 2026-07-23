from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import Iterable, Mapping, Sequence

from .engine import ArtifactStage


class CapabilityState(str, Enum):
    DECLARED = "declared"
    DISCOVERED = "discovered"
    CONNECTED = "connected"
    AUTHENTICATED = "authenticated"
    AUTHORIZED = "authorized"
    INVOKED = "invoked"
    RETURNED = "returned"
    VERIFIED = "verified"
    PERSISTED = "persisted"


CAPABILITY_ORDER = {
    state: index for index, state in enumerate(CapabilityState)
}


class EvidenceLevel(IntEnum):
    NONE = 0
    ASSERTED = 1
    OBSERVED = 2
    PROVIDER_RECEIPT = 3
    VERIFIED = 4
    PERSISTED = 5


class MaturityDimension(str, Enum):
    MODEL_CAPABILITY = "model_capability"
    TOOL_POWER = "tool_power"
    SOURCE_SELECTION_LITERACY = "source_selection_literacy"
    LEGAL_DOCUMENT_LITERACY = "legal_document_literacy"
    EVIDENCE_FORENSIC_DOCUMENT_LITERACY = "evidence_forensic_document_literacy"
    DEVELOPER_TOOL_LITERACY = "developer_tool_literacy"
    ARCHITECTURE_LITERACY = "architecture_literacy"
    MULTI_TOOL_ORCHESTRATION = "multi_tool_orchestration"
    END_TO_END_EXECUTION = "end_to_end_execution"
    ARTIFACT_CLOSURE = "artifact_closure"
    PERSISTENT_SYSTEM_STATE = "persistent_system_state"
    PHYSICAL_SCIENCE_FORENSICS = "physical_science_forensics"


class MaturityBand(str, Enum):
    UNASSESSED = "unassessed"
    DECLARED = "declared"
    OBSERVED = "observed"
    RECEIPT_BACKED = "receipt_backed"
    VERIFIED = "verified"
    PERSISTED = "persisted"


@dataclass(frozen=True)
class CapabilityReceipt:
    capability: str
    state: CapabilityState
    source_ref: str
    provider_receipt: str | None = None
    artifact_ref: str | None = None
    complete_data: bool = False
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def validate(self) -> None:
        if not self.capability.strip():
            raise ValueError("capability is required")
        if not self.source_ref.strip():
            raise ValueError("capability receipt requires a source_ref")
        if self.state in {
            CapabilityState.RETURNED,
            CapabilityState.VERIFIED,
            CapabilityState.PERSISTED,
        } and not self.provider_receipt:
            raise ValueError(
                f"{self.state.value} requires a provider_receipt"
            )
        if self.state == CapabilityState.PERSISTED and not self.artifact_ref:
            raise ValueError("persisted capability requires an artifact_ref")


@dataclass
class CapabilityLedger:
    capability: str
    receipts: list[CapabilityReceipt] = field(default_factory=list)

    def record(self, receipt: CapabilityReceipt) -> None:
        receipt.validate()
        if receipt.capability != self.capability:
            raise ValueError("receipt capability does not match ledger")
        if self.receipts:
            previous = self.receipts[-1].state
            if CAPABILITY_ORDER[receipt.state] < CAPABILITY_ORDER[previous]:
                raise ValueError(
                    f"capability regression: {receipt.state.value} follows "
                    f"{previous.value}"
                )
            if receipt.state == previous:
                raise ValueError(
                    f"duplicate capability state: {receipt.state.value}"
                )
        self.receipts.append(receipt)

    @property
    def current_state(self) -> CapabilityState | None:
        return self.receipts[-1].state if self.receipts else None

    @property
    def fully_operational(self) -> bool:
        return self.current_state == CapabilityState.PERSISTED

    def missing_states(
        self,
        target: CapabilityState = CapabilityState.PERSISTED,
    ) -> tuple[CapabilityState, ...]:
        current_index = (
            CAPABILITY_ORDER[self.current_state]
            if self.current_state is not None
            else -1
        )
        target_index = CAPABILITY_ORDER[target]
        return tuple(
            state
            for state in CapabilityState
            if current_index < CAPABILITY_ORDER[state] <= target_index
        )


@dataclass(frozen=True)
class MaturityControl:
    control_id: str
    dimension: MaturityDimension
    description: str
    weight: int = 1
    minimum_level: EvidenceLevel = EvidenceLevel.VERIFIED

    def validate(self) -> None:
        if not self.control_id.strip():
            raise ValueError("control_id is required")
        if not self.description.strip():
            raise ValueError("control description is required")
        if self.weight <= 0:
            raise ValueError("control weight must be positive")


@dataclass(frozen=True)
class ControlEvidence:
    control_id: str
    level: EvidenceLevel
    available: bool
    source_ref: str
    provider_receipt: str | None = None
    artifact_ref: str | None = None
    notes: str | None = None
    recorded_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def validate(self) -> None:
        if not self.control_id.strip():
            raise ValueError("control evidence requires control_id")
        if not self.source_ref.strip():
            raise ValueError("control evidence requires source_ref")
        if self.level >= EvidenceLevel.PROVIDER_RECEIPT and not self.provider_receipt:
            raise ValueError(
                "provider_receipt evidence level requires provider_receipt"
            )
        if self.level == EvidenceLevel.PERSISTED and not self.artifact_ref:
            raise ValueError("persisted evidence requires artifact_ref")


@dataclass(frozen=True)
class DimensionScore:
    dimension: MaturityDimension
    available_ceiling: float
    demonstrated_reliability: float
    band: MaturityBand
    controls_total: int
    controls_available: int
    controls_satisfied: int
    missing_controls: tuple[str, ...]


@dataclass(frozen=True)
class ScorecardResult:
    dimensions: tuple[DimensionScore, ...]

    @property
    def overall_available_ceiling(self) -> float:
        if not self.dimensions:
            return 0.0
        return round(
            sum(item.available_ceiling for item in self.dimensions)
            / len(self.dimensions),
            1,
        )

    @property
    def overall_demonstrated_reliability(self) -> float:
        if not self.dimensions:
            return 0.0
        return round(
            sum(item.demonstrated_reliability for item in self.dimensions)
            / len(self.dimensions),
            1,
        )

    @property
    def gap(self) -> float:
        return round(
            self.overall_available_ceiling
            - self.overall_demonstrated_reliability,
            1,
        )

    def as_dict(self) -> Mapping[str, object]:
        return {
            "overall_available_ceiling": self.overall_available_ceiling,
            "overall_demonstrated_reliability": (
                self.overall_demonstrated_reliability
            ),
            "gap": self.gap,
            "dimensions": [
                {
                    "dimension": item.dimension.value,
                    "available_ceiling": item.available_ceiling,
                    "demonstrated_reliability": (
                        item.demonstrated_reliability
                    ),
                    "band": item.band.value,
                    "controls_total": item.controls_total,
                    "controls_available": item.controls_available,
                    "controls_satisfied": item.controls_satisfied,
                    "missing_controls": list(item.missing_controls),
                }
                for item in self.dimensions
            ],
        }


class ReceiptGroundedScorecard:
    """Score operational maturity from explicit controls and evidence receipts."""

    def __init__(self, controls: Sequence[MaturityControl]):
        if not controls:
            raise ValueError("scorecard requires at least one control")
        control_ids = [control.control_id for control in controls]
        if len(control_ids) != len(set(control_ids)):
            raise ValueError("scorecard control IDs must be unique")
        for control in controls:
            control.validate()
        self.controls = tuple(controls)

    def assess(self, evidence: Iterable[ControlEvidence]) -> ScorecardResult:
        evidence_by_control: dict[str, ControlEvidence] = {}
        valid_control_ids = {control.control_id for control in self.controls}

        for item in evidence:
            item.validate()
            if item.control_id not in valid_control_ids:
                raise ValueError(
                    f"unknown maturity control: {item.control_id}"
                )
            previous = evidence_by_control.get(item.control_id)
            if previous is None or item.level > previous.level:
                evidence_by_control[item.control_id] = item

        scores = []
        for dimension in MaturityDimension:
            controls = [
                control
                for control in self.controls
                if control.dimension == dimension
            ]
            if not controls:
                continue

            total_weight = sum(control.weight for control in controls)
            available_weight = 0
            demonstrated_weight = 0.0
            satisfied = 0
            missing = []

            levels = []
            for control in controls:
                item = evidence_by_control.get(control.control_id)
                if item and item.available:
                    available_weight += control.weight
                if item:
                    levels.append(item.level)
                    normalized = min(
                        float(item.level) / float(control.minimum_level),
                        1.0,
                    )
                    if item.available:
                        demonstrated_weight += control.weight * normalized
                    if item.available and item.level >= control.minimum_level:
                        satisfied += 1
                    else:
                        missing.append(control.control_id)
                else:
                    levels.append(EvidenceLevel.NONE)
                    missing.append(control.control_id)

            ceiling = round(100.0 * available_weight / total_weight, 1)
            demonstrated = round(
                100.0 * demonstrated_weight / total_weight,
                1,
            )
            band = self._band(levels, demonstrated)
            scores.append(
                DimensionScore(
                    dimension=dimension,
                    available_ceiling=ceiling,
                    demonstrated_reliability=demonstrated,
                    band=band,
                    controls_total=len(controls),
                    controls_available=sum(
                        1
                        for control in controls
                        if evidence_by_control.get(control.control_id)
                        and evidence_by_control[control.control_id].available
                    ),
                    controls_satisfied=satisfied,
                    missing_controls=tuple(missing),
                )
            )

        return ScorecardResult(tuple(scores))

    @staticmethod
    def _band(
        levels: Sequence[EvidenceLevel],
        demonstrated: float,
    ) -> MaturityBand:
        if not levels or max(levels) == EvidenceLevel.NONE:
            return MaturityBand.UNASSESSED
        if demonstrated <= 25:
            return MaturityBand.DECLARED
        if max(levels) <= EvidenceLevel.OBSERVED:
            return MaturityBand.OBSERVED
        if max(levels) == EvidenceLevel.PROVIDER_RECEIPT:
            return MaturityBand.RECEIPT_BACKED
        if max(levels) == EvidenceLevel.VERIFIED:
            return MaturityBand.VERIFIED
        return MaturityBand.PERSISTED


@dataclass(frozen=True)
class ArtifactClosureResult:
    ready_for_use: bool
    highest_stage: ArtifactStage | None
    missing_stages: tuple[ArtifactStage, ...]
    exact_blocker: str | None


class ArtifactClosureGate:
    """Prevent a good draft from being mislabeled as a completed artifact."""

    def __init__(
        self,
        required_stages: Sequence[ArtifactStage] = tuple(ArtifactStage),
    ):
        if not required_stages:
            raise ValueError("closure gate requires at least one stage")
        if len(required_stages) != len(set(required_stages)):
            raise ValueError("closure stages must be unique")
        self.required_stages = tuple(required_stages)

    def evaluate(
        self,
        completed_stages: Iterable[ArtifactStage],
    ) -> ArtifactClosureResult:
        completed = set(completed_stages)
        missing = tuple(
            stage
            for stage in self.required_stages
            if stage not in completed
        )
        completed_ordered = [
            stage for stage in ArtifactStage if stage in completed
        ]
        highest = completed_ordered[-1] if completed_ordered else None
        ready = not missing and ArtifactStage.READY_FOR_USE in completed
        blocker = None
        if not ready:
            blocker = (
                "artifact is not ready for use; missing stages: "
                + ", ".join(stage.value for stage in missing)
            )
        return ArtifactClosureResult(
            ready_for_use=ready,
            highest_stage=highest,
            missing_stages=missing,
            exact_blocker=blocker,
        )


def standard_maturity_controls() -> tuple[MaturityControl, ...]:
    """Return transparent controls replacing subjective 1–10 ratings."""

    V = EvidenceLevel.VERIFIED
    P = EvidenceLevel.PERSISTED
    R = EvidenceLevel.PROVIDER_RECEIPT

    definitions = [
        ("MODEL-01", MaturityDimension.MODEL_CAPABILITY, "Task outcomes are evaluated against explicit acceptance criteria.", 2, V),
        ("MODEL-02", MaturityDimension.MODEL_CAPABILITY, "Reasoning claims are separated from verified external facts.", 1, V),
        ("MODEL-03", MaturityDimension.MODEL_CAPABILITY, "Material errors create regression cases or corrected policy.", 2, P),
        ("TOOL-01", MaturityDimension.TOOL_POWER, "A sourced capability inventory records available systems and operations.", 2, V),
        ("TOOL-02", MaturityDimension.TOOL_POWER, "Connection, authentication, authorization, invocation, return, verification, and persistence are distinct states.", 3, P),
        ("TOOL-03", MaturityDimension.TOOL_POWER, "Write capabilities expose provider receipts or exact blockers.", 2, R),
        ("SOURCE-01", MaturityDimension.SOURCE_SELECTION_LITERACY, "Private facts route to connected private sources rather than memory or public web.", 2, V),
        ("SOURCE-02", MaturityDimension.SOURCE_SELECTION_LITERACY, "Metadata is distinguished from content and a file reference from materialized bytes.", 2, V),
        ("SOURCE-03", MaturityDimension.SOURCE_SELECTION_LITERACY, "Search absence is not promoted to proof of nonexistence.", 1, V),
        ("SOURCE-04", MaturityDimension.SOURCE_SELECTION_LITERACY, "Authoritative primary sources outrank summaries when available.", 2, V),
        ("LEGAL-01", MaturityDimension.LEGAL_DOCUMENT_LITERACY, "Legal authorities are verified against current primary sources.", 2, V),
        ("LEGAL-02", MaturityDimension.LEGAL_DOCUMENT_LITERACY, "Actor, duty, trigger, required record, actual act, gap, notice, demand, fork, and remedy are linked.", 3, V),
        ("LEGAL-03", MaturityDimension.LEGAL_DOCUMENT_LITERACY, "Filing artifacts receive signature, date, citation, pagination, exhibit, and service checks.", 3, P),
        ("EVIDENCE-01", MaturityDimension.EVIDENCE_FORENSIC_DOCUMENT_LITERACY, "Original bytes are preserved before transformation.", 2, V),
        ("EVIDENCE-02", MaturityDimension.EVIDENCE_FORENSIC_DOCUMENT_LITERACY, "SHA-256, source URI, acquisition time, custodian, and lineage are recorded.", 3, P),
        ("EVIDENCE-03", MaturityDimension.EVIDENCE_FORENSIC_DOCUMENT_LITERACY, "Original, OCR, transcript, normalized, redacted, and derivative artifacts remain distinct.", 2, V),
        ("EVIDENCE-04", MaturityDimension.EVIDENCE_FORENSIC_DOCUMENT_LITERACY, "Official documents are treated as records containing claims, not automatic proof.", 1, V),
        ("DEV-01", MaturityDimension.DEVELOPER_TOOL_LITERACY, "Repository state is read from the provider before mutation.", 1, V),
        ("DEV-02", MaturityDimension.DEVELOPER_TOOL_LITERACY, "Changes occur on a bounded branch with commit receipts.", 2, R),
        ("DEV-03", MaturityDimension.DEVELOPER_TOOL_LITERACY, "Builds and tests run in the correct execution plane.", 3, V),
        ("DEV-04", MaturityDimension.DEVELOPER_TOOL_LITERACY, "CI, deployment, and release claims are backed by provider receipts.", 3, P),
        ("ARCH-01", MaturityDimension.ARCHITECTURE_LITERACY, "Source, canonical, control, execution, receipt, and mirror planes are mapped.", 3, V),
        ("ARCH-02", MaturityDimension.ARCHITECTURE_LITERACY, "Existing routes are reused before new infrastructure is proposed.", 2, V),
        ("ARCH-03", MaturityDimension.ARCHITECTURE_LITERACY, "Wrong-plane failure is not treated as proof of missing infrastructure.", 2, P),
        ("ARCH-04", MaturityDimension.ARCHITECTURE_LITERACY, "A bounded catalog action, adapter, or route binding precedes a new runner.", 2, V),
        ("ORCH-01", MaturityDimension.MULTI_TOOL_ORCHESTRATION, "The workflow has explicit stages, owners, inputs, outputs, and handoffs.", 3, V),
        ("ORCH-02", MaturityDimension.MULTI_TOOL_ORCHESTRATION, "Operations are idempotent or protected by replay guards.", 2, V),
        ("ORCH-03", MaturityDimension.MULTI_TOOL_ORCHESTRATION, "A failed step resumes from persisted state instead of restarting from conversation.", 3, P),
        ("ORCH-04", MaturityDimension.MULTI_TOOL_ORCHESTRATION, "Cross-tool results preserve source and provider receipts.", 2, P),
        ("EXEC-01", MaturityDimension.END_TO_END_EXECUTION, "The requested target-system action actually occurs.", 3, R),
        ("EXEC-02", MaturityDimension.END_TO_END_EXECUTION, "The result is independently read back or tested.", 3, V),
        ("EXEC-03", MaturityDimension.END_TO_END_EXECUTION, "The changed state is persisted and handed off.", 3, P),
        ("EXEC-04", MaturityDimension.END_TO_END_EXECUTION, "Exact blockers replace fictional completion.", 1, V),
        ("CLOSE-01", MaturityDimension.ARTIFACT_CLOSURE, "Artifact lifecycle receipts cover located through ready_for_use.", 4, P),
        ("CLOSE-02", MaturityDimension.ARTIFACT_CLOSURE, "Packaging includes index, attachments, and manifest.", 2, V),
        ("CLOSE-03", MaturityDimension.ARTIFACT_CLOSURE, "Stored artifacts are re-opened and validated.", 2, V),
        ("CLOSE-04", MaturityDimension.ARTIFACT_CLOSURE, "No good draft is reported as a complete deliverable.", 2, P),
        ("STATE-01", MaturityDimension.PERSISTENT_SYSTEM_STATE, "A canonical ledger records task state, artifacts, receipts, blockers, and next action.", 3, P),
        ("STATE-02", MaturityDimension.PERSISTENT_SYSTEM_STATE, "A unified artifact registry links hashes, locations, versions, and claims.", 3, P),
        ("STATE-03", MaturityDimension.PERSISTENT_SYSTEM_STATE, "Supersession and lineage preserve history rather than overwrite it.", 2, V),
        ("STATE-04", MaturityDimension.PERSISTENT_SYSTEM_STATE, "State survives conversation boundaries and can be resumed deterministically.", 3, P),
        ("PHYS-01", MaturityDimension.PHYSICAL_SCIENCE_FORENSICS, "Physical conclusions rely on qualified instruments, examiners, or laboratories.", 4, V),
        ("PHYS-02", MaturityDimension.PHYSICAL_SCIENCE_FORENSICS, "Validated scientific methods and controls are documented.", 3, V),
        ("PHYS-03", MaturityDimension.PHYSICAL_SCIENCE_FORENSICS, "Chain of custody and laboratory result receipts are preserved.", 3, P),
    ]
    return tuple(
        MaturityControl(
            control_id=control_id,
            dimension=dimension,
            description=description,
            weight=weight,
            minimum_level=minimum,
        )
        for control_id, dimension, description, weight, minimum in definitions
    )
