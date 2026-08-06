import unittest
from pathlib import Path

from infinity_stones.composition import compose_loadout
from infinity_stones.models import ManifestError
from infinity_stones.registry import StoneRegistry

ROOT = Path(__file__).resolve().parents[1]


class InfinityStoneRegistryTests(unittest.TestCase):
    def test_registry_loads_canonical_stones_and_upgrades(self) -> None:
        registry = StoneRegistry.load(ROOT)
        self.assertEqual(
            sorted(registry.stones),
            [
                "stone-monolith",
                "stone-psysoc-x",
                "stone-resume-master",
                "stone-web-design-pro",
            ],
        )
        self.assertEqual(
            sorted(registry.upgrades),
            ["upgrade-do-it-again", "upgrade-resume-do-it-again"],
        )
        self.assertEqual(registry.resolve("PSYSOC-X"), "stone-psysoc-x")
        self.assertEqual(registry.resolve("resume master"), "stone-resume-master")
        self.assertEqual(registry.resolve("web design pro"), "stone-web-design-pro")
        self.assertEqual(registry.resolve("website masterclass"), "stone-web-design-pro")
        self.assertEqual(registry.resolve("monolith"), "stone-monolith")
        self.assertEqual(registry.resolve("100 repos"), "stone-monolith")
        self.assertEqual(registry.resolve("do it again"), "upgrade-do-it-again")
        self.assertEqual(
            registry.resolve("resume do it again"),
            "upgrade-resume-do-it-again",
        )

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

    def test_web_monolith_composition_is_deterministic(self) -> None:
        registry = StoneRegistry.load(ROOT)
        first = compose_loadout(
            registry,
            stones=["monolith", "web design pro", "PSYSOC-X"],
            upgrades=["do it again"],
        )
        second = compose_loadout(
            registry,
            stones=["stone-monolith", "stone-web-design-pro", "stone-psysoc-x"],
            upgrades=["upgrade-do-it-again"],
        )
        self.assertEqual(first.digest, second.digest)
        self.assertIn("stone-monolith", first.stones)
        self.assertIn("stone-web-design-pro", first.stones)
        self.assertIn("reconciled-monolith-receipt", first.outputs)
        self.assertIn("multidimensional-experience-graph", first.outputs)

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
