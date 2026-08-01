from pathlib import Path

import pytest

from infinity_stones.composition import compose_loadout
from infinity_stones.models import ManifestError
from infinity_stones.registry import StoneRegistry


ROOT = Path(__file__).resolve().parents[1]


def test_registry_loads_canonical_stone_and_upgrade() -> None:
    registry = StoneRegistry.load(ROOT)
    assert sorted(registry.stones) == ["stone-psysoc-x"]
    assert sorted(registry.upgrades) == ["upgrade-do-it-again"]
    assert registry.resolve("PSYSOC-X") == "stone-psysoc-x"
    assert registry.resolve("do it again") == "upgrade-do-it-again"


def test_composition_is_deterministic_and_preserves_kernel_precedence() -> None:
    registry = StoneRegistry.load(ROOT)
    first = compose_loadout(
        registry,
        stones=["PSYSOC-X"],
        upgrades=["do it again"],
    )
    second = compose_loadout(
        registry,
        stones=["stone-psysoc-x"],
        upgrades=["upgrade-do-it-again"],
    )
    assert first.digest == second.digest
    assert first.precedence[0] == "kernel-constitution"
    assert first.precedence[-1] == "mission-specific-instructions"
    assert "preserve all verified gains" in first.governing_laws


def test_composition_rejects_duplicate_stones() -> None:
    registry = StoneRegistry.load(ROOT)
    with pytest.raises(ManifestError, match="same stone twice"):
        compose_loadout(registry, stones=["PSYSOC-X", "stone-psysoc-x"])


def test_unknown_alias_fails_closed() -> None:
    registry = StoneRegistry.load(ROOT)
    with pytest.raises(KeyError, match="unknown stone or upgrade"):
        registry.resolve("imaginary-stone")
