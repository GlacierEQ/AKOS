import re
import unittest
from pathlib import Path

from infinity_stones.projections import (
    ProjectionLayer,
    build_projection,
    build_projection_bundle,
    canonical_stone_payload,
)
from infinity_stones.receipts import canonical_json
from infinity_stones.registry import StoneRegistry

ROOT = Path(__file__).resolve().parents[1]


class InfinityStoneProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = StoneRegistry.load(ROOT)
        cls.manifest = cls.registry.stone("web design pro")

    def test_bundle_contains_exactly_four_layers_with_one_truth_digest(self) -> None:
        bundle = build_projection_bundle(self.manifest)
        self.assertEqual(
            bundle["layers"],
            ["recruiter", "master", "machine", "mesh"],
        )
        self.assertEqual(set(bundle["projections"]), set(bundle["layers"]))
        canonical_digests = {
            projection["canonical_digest"]
            for projection in bundle["projections"].values()
        }
        self.assertEqual(canonical_digests, {bundle["canonical_digest"]})

    def test_projections_are_deterministic(self) -> None:
        first = build_projection_bundle(self.manifest)
        second = build_projection_bundle(self.manifest)
        self.assertEqual(first, second)

    def test_recruiter_layer_preserves_status_and_truth_boundary(self) -> None:
        projection = build_projection(self.manifest, ProjectionLayer.RECRUITER)
        self.assertEqual(projection.payload["identity"]["status"], self.manifest.status)
        self.assertEqual(projection.payload["trace"]["status"], self.manifest.status)
        self.assertTrue(
            projection.payload["trace"]["claims_must_not_exceed_canonical_status"]
        )
        self.assertEqual(projection.payload["boundaries"], list(self.manifest.forbidden))

    def test_master_layer_contains_complete_normalized_manifest(self) -> None:
        projection = build_projection(self.manifest, ProjectionLayer.MASTER)
        self.assertEqual(
            projection.payload["canonical_manifest"],
            canonical_stone_payload(self.manifest),
        )
        self.assertEqual(
            projection.payload["architecture"]["governing_laws"],
            list(self.manifest.governing_laws),
        )

    def test_machine_layer_uses_canonical_json_and_real_proto_contract(self) -> None:
        projection = build_projection(self.manifest, ProjectionLayer.MACHINE)
        self.assertEqual(
            projection.payload["canonical_json"],
            canonical_json(canonical_stone_payload(self.manifest)),
        )
        contract = projection.payload["wire_contract"]
        self.assertEqual(contract["format"], "Protocol Buffers v3")
        proto_path = ROOT / contract["schema_path"]
        proto = proto_path.read_text(encoding="utf-8")
        self.assertIn('syntax = "proto3";', proto)
        self.assertIn("message InfinityStoneProjection", proto)
        self.assertIn("PROJECTION_LAYER_RECRUITER = 1;", proto)
        self.assertIn("PROJECTION_LAYER_MASTER = 2;", proto)
        self.assertIn("PROJECTION_LAYER_MACHINE = 3;", proto)
        self.assertIn("PROJECTION_LAYER_MESH = 4;", proto)
        field_numbers = [
            int(value)
            for value in re.findall(r"^\s+(?:repeated\s+)?[\w.]+\s+\w+\s+=\s+(\d+);", proto, re.MULTILINE)
        ]
        self.assertEqual(len(field_numbers), len(set(field_numbers)))

    def test_mesh_layer_exposes_capability_and_compatibility_edges(self) -> None:
        projection = build_projection(self.manifest, ProjectionLayer.MESH)
        edges = projection.payload["graph"]["edges"]
        relationships = {edge["relationship"] for edge in edges}
        self.assertIn("provides", relationships)
        self.assertIn("governed-by", relationships)
        self.assertIn("emits", relationships)
        if self.manifest.compatible_stones:
            self.assertIn("compatible-with", relationships)


if __name__ == "__main__":
    unittest.main()
