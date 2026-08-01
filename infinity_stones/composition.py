"""Deterministic composition of stones and cross-stone upgrades."""

from __future__ import annotations

from collections.abc import Iterable

from .models import CompositionPlan, ManifestError
from .receipts import digest
from .registry import StoneRegistry


def compose_loadout(
    registry: StoneRegistry,
    *,
    stones: Iterable[str],
    upgrades: Iterable[str] = (),
) -> CompositionPlan:
    selected = tuple(registry.stone(value) for value in stones)
    selected_upgrades = tuple(registry.upgrade(value) for value in upgrades)
    if not selected:
        raise ManifestError("a loadout must contain at least one stone")

    selected_ids = tuple(manifest.id for manifest in selected)
    if len(set(selected_ids)) != len(selected_ids):
        raise ManifestError("a loadout cannot contain the same stone twice")

    selected_set = set(selected_ids)
    for manifest in selected:
        conflict = selected_set & set(manifest.incompatible_stones)
        if conflict:
            raise ManifestError(
                f"{manifest.id} is incompatible with {', '.join(sorted(conflict))}"
            )

    upgrade_ids = tuple(manifest.id for manifest in selected_upgrades)
    if len(set(upgrade_ids)) != len(upgrade_ids):
        raise ManifestError("a loadout cannot contain the same upgrade twice")

    for upgrade in selected_upgrades:
        unsupported = [
            stone_id
            for stone_id in selected_ids
            if upgrade.compatible_stones and stone_id not in upgrade.compatible_stones
        ]
        if unsupported:
            raise ManifestError(
                f"{upgrade.id} is not compatible with {', '.join(sorted(unsupported))}"
            )
        for stone in selected:
            if stone.compatible_upgrades and upgrade.id not in stone.compatible_upgrades:
                raise ManifestError(f"{stone.id} does not permit upgrade {upgrade.id}")

    laws = _ordered_unique(
        law
        for manifest in selected
        for law in manifest.governing_laws
    )
    invariants = _ordered_unique(
        invariant
        for upgrade in selected_upgrades
        for invariant in upgrade.invariants
    )
    forbidden = _ordered_unique(
        item
        for manifest in selected
        for item in manifest.forbidden
    )
    outputs = _ordered_unique(
        output
        for manifest in selected
        for output in manifest.outputs
    )
    precedence = (
        "kernel-constitution",
        *selected_ids,
        *upgrade_ids,
        "mission-specific-instructions",
    )
    payload = {
        "stones": selected_ids,
        "upgrades": upgrade_ids,
        "precedence": precedence,
        "governing_laws": (*laws, *invariants),
        "forbidden": forbidden,
        "outputs": outputs,
    }
    return CompositionPlan(
        stones=selected_ids,
        upgrades=upgrade_ids,
        precedence=precedence,
        governing_laws=tuple(payload["governing_laws"]),
        forbidden=forbidden,
        outputs=outputs,
        digest=digest(payload),
        metadata={"schema": "glaciereq.infinity-loadout.v1"},
    )


def _ordered_unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))
