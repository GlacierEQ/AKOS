"""Typed contracts for stones, upgrades, composition, and human calibration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class ManifestError(ValueError):
    """Raised when a stone or upgrade manifest violates the forge contract."""


def _require_nonempty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{field_name} must be a non-empty string")
    return value.strip()


def _string_tuple(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    invalid_item = any(
        not isinstance(item, str) or not item.strip() for item in value
    ) if isinstance(value, list) else True
    if not isinstance(value, list) or invalid_item:
        raise ManifestError(f"{field_name} must be a list of non-empty strings")
    return tuple(item.strip() for item in value)


@dataclass(frozen=True)
class StoneManifest:
    """Validated identity and behavior declaration for one reversible specialization."""

    id: str
    name: str
    version: str
    domain: str
    status: str
    aliases: tuple[str, ...]
    skills: tuple[str, ...]
    protocols: tuple[str, ...]
    governing_laws: tuple[str, ...]
    forbidden: tuple[str, ...]
    compatible_stones: tuple[str, ...]
    incompatible_stones: tuple[str, ...]
    compatible_upgrades: tuple[str, ...]
    outputs: tuple[str, ...]
    source_path: str

    @classmethod
    def from_dict(cls, data: dict[str, Any], source_path: str) -> "StoneManifest":
        identity = data.get("identity")
        if not isinstance(identity, dict):
            raise ManifestError("identity must be an object")
        activation = data.get("activation", {})
        capabilities = data.get("capabilities", {})
        judgment = data.get("judgment", {})
        boundaries = data.get("boundaries", {})
        composition = data.get("composition", {})
        interfaces = data.get("interfaces", {})
        if any(not isinstance(section, dict) for section in (
            activation, capabilities, judgment, boundaries, composition, interfaces
        )):
            raise ManifestError("manifest sections must be objects")

        manifest = cls(
            id=_require_nonempty_string(identity.get("id"), "identity.id"),
            name=_require_nonempty_string(identity.get("name"), "identity.name"),
            version=_require_nonempty_string(identity.get("version"), "identity.version"),
            domain=_require_nonempty_string(identity.get("domain"), "identity.domain"),
            status=_require_nonempty_string(data.get("status"), "status"),
            aliases=_string_tuple(activation.get("aliases"), "activation.aliases"),
            skills=_string_tuple(capabilities.get("skills"), "capabilities.skills"),
            protocols=_string_tuple(capabilities.get("protocols"), "capabilities.protocols"),
            governing_laws=_string_tuple(judgment.get("governing_laws"), "judgment.governing_laws"),
            forbidden=_string_tuple(boundaries.get("forbidden"), "boundaries.forbidden"),
            compatible_stones=_string_tuple(
                composition.get("compatible_stones"), "composition.compatible_stones"
            ),
            incompatible_stones=_string_tuple(
                composition.get("incompatible_stones"), "composition.incompatible_stones"
            ),
            compatible_upgrades=_string_tuple(
                composition.get("compatible_upgrades"), "composition.compatible_upgrades"
            ),
            outputs=_string_tuple(interfaces.get("outputs"), "interfaces.outputs"),
            source_path=source_path,
        )
        if not manifest.skills:
            raise ManifestError("a stone must declare at least one skill")
        if not manifest.governing_laws:
            raise ManifestError("a stone must declare at least one governing law")
        if set(manifest.compatible_stones) & set(manifest.incompatible_stones):
            raise ManifestError("a stone cannot mark the same stone compatible and incompatible")
        return manifest


@dataclass(frozen=True)
class UpgradeManifest:
    """Validated cross-stone modifier."""

    id: str
    name: str
    version: str
    status: str
    aliases: tuple[str, ...]
    compatible_stones: tuple[str, ...]
    protocol: tuple[str, ...]
    invariants: tuple[str, ...]
    source_path: str

    @classmethod
    def from_dict(cls, data: dict[str, Any], source_path: str) -> "UpgradeManifest":
        identity = data.get("identity")
        if not isinstance(identity, dict):
            raise ManifestError("identity must be an object")
        activation = data.get("activation", {})
        composition = data.get("composition", {})
        behavior = data.get("behavior", {})
        if any(not isinstance(section, dict) for section in (activation, composition, behavior)):
            raise ManifestError("upgrade sections must be objects")
        manifest = cls(
            id=_require_nonempty_string(identity.get("id"), "identity.id"),
            name=_require_nonempty_string(identity.get("name"), "identity.name"),
            version=_require_nonempty_string(identity.get("version"), "identity.version"),
            status=_require_nonempty_string(data.get("status"), "status"),
            aliases=_string_tuple(activation.get("aliases"), "activation.aliases"),
            compatible_stones=_string_tuple(
                composition.get("compatible_stones"), "composition.compatible_stones"
            ),
            protocol=_string_tuple(behavior.get("protocol"), "behavior.protocol"),
            invariants=_string_tuple(behavior.get("invariants"), "behavior.invariants"),
            source_path=source_path,
        )
        if not manifest.protocol:
            raise ManifestError("an upgrade must declare a protocol")
        if not manifest.invariants:
            raise ManifestError("an upgrade must declare invariants")
        return manifest


@dataclass(frozen=True)
class AudienceContext:
    """Explicit inputs PSYSOC-X may use; hidden personal traits are out of scope."""

    audience: str
    decision: str
    stakes: str = "medium"
    skepticism: int = 5
    cognitive_load: int = 5
    emotional_weight: int = 5
    evidence_strength: int = 5
    humor_allowed: bool = True
    private_or_sensitive: bool = False
    desired_action: str = "understand"

    def __post_init__(self) -> None:
        if self.stakes not in {"low", "medium", "high", "critical"}:
            raise ValueError("stakes must be low, medium, high, or critical")
        for name in ("skepticism", "cognitive_load", "emotional_weight", "evidence_strength"):
            value = getattr(self, name)
            if not isinstance(value, int) or not 0 <= value <= 10:
                raise ValueError(f"{name} must be an integer from 0 to 10")
        required_text = (self.audience, self.decision, self.desired_action)
        if any(not value.strip() for value in required_text):
            raise ValueError("audience, decision, and desired_action must be non-empty")


@dataclass(frozen=True)
class CalibrationProfile:
    """Human-facing presentation guidance constrained by explicit evidence."""

    attention_strategy: str
    humor_mode: str
    tone: str
    logic_order: tuple[str, ...]
    density: str
    skepticism_response: str
    memory_anchor: str
    dignity_controls: tuple[str, ...]
    warnings: tuple[str, ...]
    confidence: str


@dataclass(frozen=True)
class CompositionPlan:
    """Deterministic result of composing stones and upgrades."""

    stones: tuple[str, ...]
    upgrades: tuple[str, ...]
    precedence: tuple[str, ...]
    governing_laws: tuple[str, ...]
    forbidden: tuple[str, ...]
    outputs: tuple[str, ...]
    digest: str
    metadata: dict[str, Any] = field(default_factory=dict)
