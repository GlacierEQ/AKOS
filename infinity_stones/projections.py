"""Deterministic audience and machine projections for canonical Infinity Stones."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from .models import StoneManifest
from .receipts import canonical_json, digest


class ProjectionLayer(StrEnum):
    """Supported views over one canonical Stone truth record."""

    RECRUITER = "recruiter"
    MASTER = "master"
    MACHINE = "machine"
    MESH = "mesh"


@dataclass(frozen=True)
class StoneProjection:
    """One traceable projection derived from a canonical Stone manifest."""

    layer: ProjectionLayer
    stone_id: str
    stone_version: str
    canonical_digest: str
    projection_digest: str
    payload: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": "glaciereq.infinity-stone-projection.v1",
            "layer": self.layer.value,
            "stone_id": self.stone_id,
            "stone_version": self.stone_version,
            "canonical_digest": self.canonical_digest,
            "projection_digest": self.projection_digest,
            "payload": self.payload,
        }


def canonical_stone_payload(manifest: StoneManifest) -> dict[str, Any]:
    """Return the complete normalized Stone truth record used by every projection."""

    return {
        "identity": {
            "id": manifest.id,
            "name": manifest.name,
            "version": manifest.version,
            "domain": manifest.domain,
        },
        "status": manifest.status,
        "activation": {"aliases": list(manifest.aliases)},
        "capabilities": {
            "skills": list(manifest.skills),
            "protocols": list(manifest.protocols),
        },
        "judgment": {"governing_laws": list(manifest.governing_laws)},
        "boundaries": {"forbidden": list(manifest.forbidden)},
        "composition": {
            "compatible_stones": list(manifest.compatible_stones),
            "incompatible_stones": list(manifest.incompatible_stones),
            "compatible_upgrades": list(manifest.compatible_upgrades),
        },
        "interfaces": {"outputs": list(manifest.outputs)},
        "source": {"path": manifest.source_path},
    }


def build_projection(
    manifest: StoneManifest,
    layer: ProjectionLayer | str,
) -> StoneProjection:
    """Build one deterministic projection without changing the underlying truth state."""

    selected_layer = ProjectionLayer(layer)
    canonical = canonical_stone_payload(manifest)
    canonical_digest = digest(canonical)
    payload_builders = {
        ProjectionLayer.RECRUITER: _recruiter_payload,
        ProjectionLayer.MASTER: _master_payload,
        ProjectionLayer.MACHINE: _machine_payload,
        ProjectionLayer.MESH: _mesh_payload,
    }
    payload = payload_builders[selected_layer](manifest, canonical, canonical_digest)
    projection_digest = digest(
        {
            "layer": selected_layer.value,
            "canonical_digest": canonical_digest,
            "payload": payload,
        }
    )
    return StoneProjection(
        layer=selected_layer,
        stone_id=manifest.id,
        stone_version=manifest.version,
        canonical_digest=canonical_digest,
        projection_digest=projection_digest,
        payload=payload,
    )


def build_projection_bundle(manifest: StoneManifest) -> dict[str, Any]:
    """Build all four projections and bind them to one canonical digest."""

    projections = {
        layer.value: build_projection(manifest, layer).as_dict()
        for layer in ProjectionLayer
    }
    canonical_digests = {
        projection["canonical_digest"] for projection in projections.values()
    }
    if len(canonical_digests) != 1:
        raise ValueError("projection canonical digests diverged")
    return {
        "schema": "glaciereq.infinity-stone-projection-bundle.v1",
        "stone_id": manifest.id,
        "stone_version": manifest.version,
        "canonical_digest": canonical_digests.pop(),
        "layers": [layer.value for layer in ProjectionLayer],
        "projections": projections,
    }


def _trace(
    manifest: StoneManifest,
    canonical_digest: str,
) -> dict[str, Any]:
    return {
        "stone_id": manifest.id,
        "stone_version": manifest.version,
        "status": manifest.status,
        "source_path": manifest.source_path,
        "canonical_digest": canonical_digest,
        "claims_must_not_exceed_canonical_status": True,
    }


def _recruiter_payload(
    manifest: StoneManifest,
    canonical: dict[str, Any],
    canonical_digest: str,
) -> dict[str, Any]:
    del canonical
    return {
        "identity": {
            "name": manifest.name,
            "domain": manifest.domain,
            "status": manifest.status,
        },
        "decision_summary": (
            f"{manifest.name} is a {manifest.status} specialization for {manifest.domain}."
        ),
        "skills": list(manifest.skills),
        "outputs": list(manifest.outputs),
        "boundaries": list(manifest.forbidden),
        "trace": _trace(manifest, canonical_digest),
    }


def _master_payload(
    manifest: StoneManifest,
    canonical: dict[str, Any],
    canonical_digest: str,
) -> dict[str, Any]:
    return {
        "canonical_manifest": canonical,
        "architecture": {
            "governing_laws": list(manifest.governing_laws),
            "protocols": list(manifest.protocols),
            "compatible_stones": list(manifest.compatible_stones),
            "incompatible_stones": list(manifest.incompatible_stones),
            "compatible_upgrades": list(manifest.compatible_upgrades),
        },
        "trace": _trace(manifest, canonical_digest),
    }


def _machine_payload(
    manifest: StoneManifest,
    canonical: dict[str, Any],
    canonical_digest: str,
) -> dict[str, Any]:
    return {
        "wire_contract": {
            "format": "Protocol Buffers v3",
            "schema_path": "proto/infinity_stone_projection.proto",
            "message": "glaciereq.akos.v1.InfinityStoneProjection",
            "canonical_json_encoding": "UTF-8 RFC 8259; sorted keys; compact separators",
        },
        "canonical_json": canonical_json(canonical),
        "canonical_manifest": canonical,
        "trace": _trace(manifest, canonical_digest),
    }


def _mesh_payload(
    manifest: StoneManifest,
    canonical: dict[str, Any],
    canonical_digest: str,
) -> dict[str, Any]:
    del canonical
    nodes: list[dict[str, str]] = [
        {"id": manifest.id, "kind": "stone", "label": manifest.name},
        {
            "id": f"domain:{manifest.domain}",
            "kind": "domain",
            "label": manifest.domain,
        },
    ]
    edges: list[dict[str, str]] = [
        {
            "source": manifest.id,
            "target": f"domain:{manifest.domain}",
            "relationship": "operates-in",
        }
    ]

    relationship_groups = (
        ("skill", manifest.skills, "provides"),
        ("protocol", manifest.protocols, "implements"),
        ("law", manifest.governing_laws, "governed-by"),
        ("boundary", manifest.forbidden, "forbids"),
        ("output", manifest.outputs, "emits"),
        ("stone", manifest.compatible_stones, "compatible-with"),
        ("stone", manifest.incompatible_stones, "incompatible-with"),
        ("upgrade", manifest.compatible_upgrades, "accepts-upgrade"),
    )
    seen_nodes = {node["id"] for node in nodes}
    for kind, values, relationship in relationship_groups:
        for value in values:
            node_id = value if kind in {"stone", "upgrade"} else f"{kind}:{value}"
            if node_id not in seen_nodes:
                nodes.append({"id": node_id, "kind": kind, "label": value})
                seen_nodes.add(node_id)
            edges.append(
                {
                    "source": manifest.id,
                    "target": node_id,
                    "relationship": relationship,
                }
            )

    return {
        "graph": {
            "directed": True,
            "nodes": nodes,
            "edges": edges,
        },
        "trace": _trace(manifest, canonical_digest),
    }
