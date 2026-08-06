"""Local resource indexing and connector declaration for career evidence."""

from __future__ import annotations

import json
import mimetypes
from pathlib import Path
from typing import Any, Iterable

from .io import sha256_file

_RESOURCE_DIR = Path(__file__).with_name("resources")
_DEFAULT_CONNECTORS = _RESOURCE_DIR / "connector-registry.v1.json"


def load_connector_registry(path: Path = _DEFAULT_CONNECTORS) -> dict[str, Any]:
    """Load declared connector capabilities without executing external actions."""

    return json.loads(path.read_text(encoding="utf-8"))


def index_local_resources(paths: Iterable[Path]) -> list[dict[str, Any]]:
    """Index local files with stable hashes and no content mutation."""

    records: list[dict[str, Any]] = []
    for raw_path in sorted({Path(value) for value in paths}, key=lambda item: item.as_posix()):
        path = raw_path.expanduser()
        if not path.exists() or not path.is_file() or path.is_symlink():
            records.append(
                {
                    "path": path.as_posix(),
                    "state": "UNAVAILABLE",
                    "reason": "missing, non-file, or symlink resource",
                }
            )
            continue
        records.append(
            {
                "path": path.resolve().as_posix(),
                "name": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                "state": "INDEXED_LOCAL",
            }
        )
    return records


def build_resource_index(
    graph_data: dict[str, Any],
    *,
    local_paths: Iterable[Path] = (),
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Combine canonical artifacts, local hashes, and declared connector surfaces."""

    canonical_artifacts = []
    for item in graph_data.get("artifacts", []):
        if isinstance(item, dict):
            canonical_artifacts.append(dict(item))
    return {
        "schema": "glaciereq.career-resource-index.v1",
        "state": "INDEXED",
        "canonical_artifacts": canonical_artifacts,
        "local_resources": index_local_resources(local_paths),
        "provided_catalog": catalog or {},
        "connectors": load_connector_registry().get("connectors", []),
        "execution": {
            "live_connector_queries": 0,
            "external_writes": 0,
            "authorization_required": True,
        },
    }
