import unittest
from pathlib import Path

from infinity_stones.composition import compose_loadout
from infinity_stones.models import ManifestError
from infinity_stones.registry import StoneRegistry

ROOT = Path(__file__).resolve().parents[1]


class InfinityStoneRegistryTests(unittest.TestCase):
    def test_registry_loads_canonical_stone_and_upgrade(self) -> None:
        registry = StoneRegistry.load(ROOT)
        self.assertEqual(sorted(registry.stones), ["stone-psysoc-x"])
        self.assertEqual(sorted(registry.upgrades), ["upgrade-do-it-again"])
        self.assertEqual(registry.resolve("PSYSOC-X"), "stone-psysoc-x")
        self.assertEqual(registry.resolve("do it again"), "upgrade-do-it-again")

    def test_composition_is_deterministic_and_preserves_kernel_precedence(self) -> None:
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
        self.assertEqual(first.digest, second.digest)
        self.assertEqual(first.precedence[0], "kernel-constitution")
        self.assertEqual(first.precedence[-1], "mission-specific-instructions")
        self.assertIn("preserve all verified gains", first.governing_laws)

    def test_composition_rejects_duplicate_stones(self) -> None:
        registry = StoneRegistry.load(ROOT)
        with self.assertRaisesRegex(ManifestError, "same stone twice"):
            compose_loadout(registry, stones=["PSYSOC-X", "stone-psysoc-x"])

    def test_unknown_alias_fails_closed(self) -> None:
        registry = StoneRegistry.load(ROOT)
        with self.assertRaisesRegex(KeyError, "unknown stone or upgrade"):
            registry.resolve("imaginary-stone")


if __name__ == "__main__":
    unittest.main()
