"""Load and validate the canonical Infinity Stone registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ManifestError, StoneManifest, UpgradeManifest


class StoneRegistry:
    """In-memory registry with identity, alias, and path validation."""

    def __init__(
        self,
        *,
        root: Path,
        stones: dict[str, StoneManifest],
        upgrades: dict[str, UpgradeManifest],
        aliases: dict[str, str],
    ) -> None:
        self.root = root
        self.stones = stones
        self.upgrades = upgrades
        self.aliases = aliases

    @classmethod
    def load(cls, root: Path) -> "StoneRegistry":
        registry_path = root / "registry" / "stones.json"
        data = _read_json(registry_path)
        if data.get("schema") != "glaciereq.infinity-stone-registry.v1":
            raise ManifestError("unsupported or missing registry schema")
        stone_entries = data.get("stones")
        upgrade_entries = data.get("upgrades")
        if not isinstance(stone_entries, list) or not isinstance(upgrade_entries, list):
            raise ManifestError("registry stones and upgrades must be lists")

        stones: dict[str, StoneManifest] = {}
        upgrades: dict[str, UpgradeManifest] = {}
        aliases: dict[str, str] = {}

        for entry in stone_entries:
            path = _entry_path(entry, "stone")
            raw = _read_json(root / path)
            manifest = StoneManifest.from_dict(raw, path)
            _register_id(stones, manifest.id, manifest, "stone")
            _register_aliases(aliases, manifest.id, (manifest.id, *manifest.aliases))

        for entry in upgrade_entries:
            path = _entry_path(entry, "upgrade")
            raw = _read_json(root / path)
            manifest = UpgradeManifest.from_dict(raw, path)
            _register_id(upgrades, manifest.id, manifest, "upgrade")
            _register_aliases(aliases, manifest.id, (manifest.id, *manifest.aliases))

        return cls(root=root, stones=stones, upgrades=upgrades, aliases=aliases)

    def resolve(self, value: str) -> str:
        normalized = _normalize_alias(value)
        try:
            return self.aliases[normalized]
        except KeyError as exc:
            raise KeyError(f"unknown stone or upgrade: {value}") from exc

    def stone(self, value: str) -> StoneManifest:
        resolved = self.resolve(value)
        try:
            return self.stones[resolved]
        except KeyError as exc:
            raise KeyError(f"{value} resolves to an upgrade, not a stone") from exc

    def upgrade(self, value: str) -> UpgradeManifest:
        resolved = self.resolve(value)
        try:
            return self.upgrades[resolved]
        except KeyError as exc:
            raise KeyError(f"{value} resolves to a stone, not an upgrade") from exc


def _read_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise ManifestError(f"missing manifest: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError(f"{path} must contain a JSON object")
    return data


def _entry_path(entry: Any, kind: str) -> str:
    if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
        raise ManifestError(f"registry {kind} entry must declare path")
    path = entry["path"]
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ManifestError(f"unsafe registry path: {path}")
    return path


def _register_id(target: dict[str, Any], identity: str, manifest: Any, kind: str) -> None:
    if identity in target:
        raise ManifestError(f"duplicate {kind} id: {identity}")
    target[identity] = manifest


def _normalize_alias(value: str) -> str:
    return " ".join(value.strip().lower().replace("_", "-").split())


def _register_aliases(target: dict[str, str], identity: str, values: tuple[str, ...]) -> None:
    for value in values:
        normalized = _normalize_alias(value)
        existing = target.get(normalized)
        if existing is not None and existing != identity:
            raise ManifestError(f"alias collision: {value!r} maps to {existing} and {identity}")
        target[normalized] = identity
