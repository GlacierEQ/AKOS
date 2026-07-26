from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from operational_cognition.connectors.kimi_memory import (
    ImportDisposition,
    JsonlMemoryStore,
    KimiMemoryAdapter,
    load_export_records,
    memoryplugin_line,
)


class KimiMemoryAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = KimiMemoryAdapter(default_case_id="GLOBAL", default_owner="casey")
        self.raw = {
            "id": "kimi-memory-1",
            "title": "Connector architecture",
            "content": "Kimi is an edge adapter, not the canon.",
            "created_at": "2026-07-26T00:00:00Z",
        }

    def test_normalization_is_deterministic(self) -> None:
        first = self.adapter.normalize(self.raw, source_uri="file:///kimi.json")
        second = self.adapter.normalize(self.raw, source_uri="file:///kimi.json")
        self.assertEqual(first.casebrain_id, second.casebrain_id)
        self.assertEqual(first.content_sha256, second.content_sha256)
        self.assertRegex(first.casebrain_id, r"^CBR-CONNECTOR_OBJECT-[0-9A-HJKMNP-TV-Z]{26}$")
        self.assertEqual(first.verification_status, "unverified")
        self.assertEqual(first.metadata["review_state"], "working")

    def test_create_then_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = JsonlMemoryStore(Path(tmp))
            first = self.adapter.import_records([self.raw], store, source_uri="file:///kimi.json")
            second = self.adapter.import_records([self.raw], store, source_uri="file:///kimi.json")
            self.assertEqual(first[0].disposition, ImportDisposition.CREATED)
            self.assertEqual(second[0].disposition, ImportDisposition.UNCHANGED)
            self.assertEqual(len(store.records_path.read_text(encoding="utf-8").splitlines()), 1)
            self.assertTrue(store.verify()["valid"])

    def test_changed_content_is_reported_as_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = JsonlMemoryStore(Path(tmp))
            self.adapter.import_records([self.raw], store, source_uri="file:///kimi.json")
            changed = dict(self.raw)
            changed["content"] = "Changed content."
            receipt = self.adapter.import_records([changed], store, source_uri="file:///kimi.json")[0]
            self.assertEqual(receipt.disposition, ImportDisposition.DRIFTED)
            self.assertEqual(len(store.records_path.read_text(encoding="utf-8").splitlines()), 1)
            self.assertTrue(store.drift_path.exists())

    def test_rejects_empty_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = JsonlMemoryStore(Path(tmp))
            receipt = self.adapter.import_records([{"id": "empty"}], store, source_uri="file:///kimi.json")[0]
            self.assertEqual(receipt.disposition, ImportDisposition.REJECTED)
            self.assertFalse(store.records_path.exists())

    def test_load_json_and_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            json_path = root / "export.json"
            json_path.write_text(json.dumps({"memories": [self.raw]}), encoding="utf-8")
            self.assertEqual(len(load_export_records(json_path)), 1)

            jsonl_path = root / "export.jsonl"
            jsonl_path.write_text(json.dumps(self.raw) + "\n", encoding="utf-8")
            self.assertEqual(len(load_export_records(jsonl_path)), 1)

    def test_memoryplugin_line(self) -> None:
        record = self.adapter.normalize(self.raw, source_uri="file:///kimi.json")
        self.assertEqual(
            memoryplugin_line(record),
            "tool=memoryplugin&&memory=Kimi is an edge adapter, not the canon.",
        )


if __name__ == "__main__":
    unittest.main()
