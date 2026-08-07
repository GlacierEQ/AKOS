"""Verify the canonical stone registry and emit atomic receipts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from infinity_stones.composition import compose_loadout
from infinity_stones.models import AudienceContext
from infinity_stones.projections import ProjectionLayer, build_projection_bundle
from infinity_stones.psysoc_x import calibrate
from infinity_stones.receipts import digest, write_atomic_json
from infinity_stones.registry import StoneRegistry


def _projection_receipt(registry: StoneRegistry) -> dict[str, object]:
    bundles = [
        build_projection_bundle(registry.stones[stone_id])
        for stone_id in sorted(registry.stones)
    ]
    receipt: dict[str, object] = {
        "schema": "glaciereq.infinity-stone-projection-receipt.v1",
        "layers": [layer.value for layer in ProjectionLayer],
        "stone_count": len(bundles),
        "projection_count": len(bundles) * len(ProjectionLayer),
        "bundles": bundles,
        "conclusion": "VERIFIED",
    }
    receipt["digest"] = digest(receipt)
    return receipt


def verify(root: Path) -> dict[str, object]:
    registry = StoneRegistry.load(root)
    loadout = compose_loadout(
        registry,
        stones=["stone-psysoc-x"],
        upgrades=["upgrade-do-it-again"],
    )
    cases_path = root / "stones" / "psysoc-x" / "tests" / "cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    results: list[dict[str, object]] = []
    failures: list[str] = []

    for case in cases["cases"]:
        profile = calibrate(AudienceContext(**case["context"]))
        actual = {
            "humor_mode": profile.humor_mode,
            "tone": profile.tone,
            "density": profile.density,
            "confidence": profile.confidence,
        }
        expected = case["expect"]
        passed = all(actual[key] == value for key, value in expected.items())
        if not passed:
            failures.append(case["id"])
        results.append({"id": case["id"], "passed": passed, "actual": actual})

    projection_receipt = _projection_receipt(registry)
    receipt = {
        "schema": "glaciereq.infinity-stone-verification-receipt.v2",
        "registry": {
            "stones": sorted(registry.stones),
            "upgrades": sorted(registry.upgrades),
        },
        "loadout": {
            "stones": loadout.stones,
            "upgrades": loadout.upgrades,
            "digest": loadout.digest,
        },
        "cases": results,
        "case_count": len(results),
        "passed": len(results) - len(failures),
        "failed": len(failures),
        "failures": failures,
        "projection_receipt": projection_receipt,
        "conclusion": "VERIFIED" if not failures else "FAILED",
    }
    receipt["digest"] = digest(receipt)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/ci/infinity-stone-receipt.json"),
    )
    parser.add_argument(
        "--projection-output",
        type=Path,
        default=Path("artifacts/ci/infinity-stone-projections.json"),
    )
    args = parser.parse_args(argv)
    receipt = verify(args.root.resolve())
    write_atomic_json(args.output, receipt)
    write_atomic_json(args.projection_output, receipt["projection_receipt"])
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if receipt["conclusion"] == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
