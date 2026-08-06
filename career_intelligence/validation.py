"""Fail-closed validation for canonical career facts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .models import CareerGraph

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED_EVIDENCE_STATES = {
    "TEST_VERIFIED",
    "RECORDED_TESTS",
    "REVIEWED_EXECUTION_BLOCKED",
    "BOUNDED_TEST_SCOPE",
    "GENERATED",
    "GENERATED_RENDER_INSPECTED",
    "PACKAGED",
    "IN_PROGRESS_IN_SOURCE_RECORD",
}


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    code: str
    message: str
    severity: str = "error"


def _string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_graph(graph: CareerGraph) -> tuple[ValidationIssue, ...]:
    data = graph.data
    issues: list[ValidationIssue] = []

    if data.get("schema") != "glaciereq.resume-master.v1":
        issues.append(ValidationIssue("schema", "SCHEMA", "unsupported resume-master schema"))
    if data.get("facts_invariant") is not True:
        issues.append(ValidationIssue("facts_invariant", "INVARIANT", "facts_invariant must be true"))

    identity = data.get("identity")
    if not isinstance(identity, dict):
        issues.append(ValidationIssue("identity", "TYPE", "identity must be an object"))
    else:
        for key in ("name", "display_name", "location", "email", "portfolio", "github"):
            if not _string(identity.get(key)):
                issues.append(ValidationIssue(f"identity.{key}", "REQUIRED", "missing value"))
        roles = identity.get("role_labels")
        if not isinstance(roles, list) or not roles or not all(_string(item) for item in roles):
            issues.append(ValidationIssue("identity.role_labels", "REQUIRED", "roles must be non-empty strings"))

    positioning = data.get("positioning")
    if not isinstance(positioning, dict):
        issues.append(ValidationIssue("positioning", "TYPE", "positioning must be an object"))
    else:
        for key in ("headline", "summary"):
            if not _string(positioning.get(key)):
                issues.append(ValidationIssue(f"positioning.{key}", "REQUIRED", "missing value"))

    proof = data.get("proof")
    if not isinstance(proof, list) or not proof:
        issues.append(ValidationIssue("proof", "REQUIRED", "at least one proof item is required"))
    else:
        seen_ids: set[str] = set()
        for index, item in enumerate(proof):
            prefix = f"proof[{index}]"
            if not isinstance(item, dict):
                issues.append(ValidationIssue(prefix, "TYPE", "proof item must be an object"))
                continue
            proof_id = item.get("id")
            if not _string(proof_id):
                issues.append(ValidationIssue(f"{prefix}.id", "REQUIRED", "proof id is required"))
            elif proof_id in seen_ids:
                issues.append(ValidationIssue(f"{prefix}.id", "DUPLICATE", "proof id must be unique"))
            else:
                seen_ids.add(proof_id)
            state = item.get("evidence_state")
            if state not in _ALLOWED_EVIDENCE_STATES:
                issues.append(ValidationIssue(f"{prefix}.evidence_state", "STATE", "unsupported evidence state"))
            if not _string(item.get("claim")):
                issues.append(ValidationIssue(f"{prefix}.claim", "REQUIRED", "proof claim is required"))

    experience = data.get("experience")
    if not isinstance(experience, list) or not experience:
        issues.append(ValidationIssue("experience", "REQUIRED", "at least one experience item is required"))
    else:
        for index, item in enumerate(experience):
            prefix = f"experience[{index}]"
            if not isinstance(item, dict):
                issues.append(ValidationIssue(prefix, "TYPE", "experience item must be an object"))
                continue
            for key in ("organization", "role", "start"):
                if not _string(item.get(key)):
                    issues.append(ValidationIssue(f"{prefix}.{key}", "REQUIRED", "missing value"))
            highlights = item.get("highlights")
            if not isinstance(highlights, list) or not highlights or not all(_string(x) for x in highlights):
                issues.append(ValidationIssue(f"{prefix}.highlights", "REQUIRED", "highlights are required"))

    capabilities = data.get("capabilities")
    if not isinstance(capabilities, dict) or not capabilities:
        issues.append(ValidationIssue("capabilities", "REQUIRED", "capability groups are required"))
    else:
        for key, values in capabilities.items():
            if not _string(key) or not isinstance(values, list) or not values or not all(_string(x) for x in values):
                issues.append(ValidationIssue(f"capabilities.{key}", "TYPE", "capabilities must be non-empty string lists"))

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        issues.append(ValidationIssue("artifacts", "REQUIRED", "artifact identities are required"))
    else:
        names: set[str] = set()
        for index, artifact in enumerate(artifacts):
            prefix = f"artifacts[{index}]"
            if not isinstance(artifact, dict):
                issues.append(ValidationIssue(prefix, "TYPE", "artifact must be an object"))
                continue
            name = artifact.get("name")
            if not _string(name):
                issues.append(ValidationIssue(f"{prefix}.name", "REQUIRED", "artifact name is required"))
            elif name in names:
                issues.append(ValidationIssue(f"{prefix}.name", "DUPLICATE", "artifact name must be unique"))
            else:
                names.add(name)
            digest = artifact.get("sha256")
            if not isinstance(digest, str) or not _HEX64.fullmatch(digest):
                issues.append(ValidationIssue(f"{prefix}.sha256", "HASH", "artifact hash must be lowercase SHA-256"))
            size = artifact.get("bytes")
            if not isinstance(size, int) or size < 0:
                issues.append(ValidationIssue(f"{prefix}.bytes", "SIZE", "artifact bytes must be a non-negative integer"))

    limits = data.get("evidence_limits")
    if not isinstance(limits, list) or not limits or not all(_string(x) for x in limits):
        issues.append(ValidationIssue("evidence_limits", "REQUIRED", "evidence limits must remain explicit"))

    return tuple(issues)
