"""Typed career-graph contracts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


class CareerGraphError(ValueError):
    """Raised when career data violates the runtime contract."""


@dataclass(frozen=True)
class TargetProfile:
    """Explicit targeting inputs; no hidden-person inference is permitted."""

    role: str = "general"
    audience: str = "technical recruiter"
    job_text: str = ""
    max_keywords: int = 24

    def __post_init__(self) -> None:
        if not self.role.strip():
            raise CareerGraphError("target role must be non-empty")
        if not self.audience.strip():
            raise CareerGraphError("target audience must be non-empty")
        if not 1 <= self.max_keywords <= 100:
            raise CareerGraphError("max_keywords must be between 1 and 100")


@dataclass(frozen=True)
class CareerGraph:
    """Validated wrapper around one canonical resume source."""

    data: dict[str, Any]
    source_path: Path
    source_sha256: str

    @property
    def identity(self) -> dict[str, Any]:
        return self.data["identity"]

    @property
    def positioning(self) -> dict[str, Any]:
        return self.data["positioning"]

    @property
    def proof(self) -> list[dict[str, Any]]:
        return self.data.get("proof", [])

    @property
    def experience(self) -> list[dict[str, Any]]:
        return self.data.get("experience", [])

    @property
    def capabilities(self) -> dict[str, list[str]]:
        return self.data.get("capabilities", {})

    @property
    def selected_systems(self) -> list[dict[str, Any]]:
        return self.data.get("selected_systems", [])

    @property
    def education(self) -> list[dict[str, Any]]:
        return self.data.get("education", [])

    @property
    def evidence_limits(self) -> list[str]:
        return self.data.get("evidence_limits", [])
