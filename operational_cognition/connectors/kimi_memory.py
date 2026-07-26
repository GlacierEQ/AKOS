"""Kimi export -> AKOS portable-memory adapter.

The adapter intentionally does not claim a live Kimi or MemoryPlugin API. It
accepts exported JSON/JSONL, normalizes records, preserves source identity,
refuses silent overwrite on drift, and emits durable import receipts.

Standard-library only so it can run inside the existing AKOS verification lane.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping, MutableMapping, Sequence

_CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _crockford_26(raw: bytes) -> str:
    """Encode the first 130 bits as a ULID-shaped Crockford Base32 token."""
    value = int.from_bytes(raw[:17], "big") >> 6
    chars: list[str] = []
    for _ in range(26):
        chars.append(_CROCKFORD[value & 31])
        value >>= 5
    return "".join(reversed(chars))


def _stable_id(source_system: str, source_object_id: str) -> str:
    seed = f"{source_system}\0{source_object_id}".encode("utf-8")
    token = _crockford_26(hashlib.sha256(seed).digest())
    return f"CBR-CONNECTOR_OBJECT-{token}"


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        return "\n".join(_coerce_text(item) for item in value if _coerce_text(item))
    if isinstance(value, Mapping):
        return _canonical_json(value)
    return str(value).strip()


def _first(mapping: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in mapping and mapping[key] not in (None, ""):
            return mapping[key]
    return None


def _extract_content(raw: Mapping[str, Any]) -> str:
    direct = _first(raw, "content", "memory", "text", "body", "summary", "message")
    if direct is not None:
        return _coerce_text(direct)

    messages = raw.get("messages")
    if isinstance(messages, Sequence) and not isinstance(messages, (str, bytes, bytearray)):
        rendered: list[str] = []
        for message in messages:
            if isinstance(message, Mapping):
                role = _coerce_text(_first(message, "role", "author", "speaker")) or "unknown"
                text = _coerce_text(_first(message, "content", "text", "body", "message"))
                if text:
                    rendered.append(f"{role}: {text}")
            else:
                text = _coerce_text(message)
                if text:
                    rendered.append(text)
        return "\n".join(rendered).strip()

    return ""


def _extract_records(payload: Any) -> list[Mapping[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, Mapping)]
    if isinstance(payload, Mapping):
        for key in ("memories", "records", "items", "conversations", "data"):
            candidate = payload.get(key)
            if isinstance(candidate, list):
                return [item for item in candidate if isinstance(item, Mapping)]
        return [payload]
    raise ValueError("Export root must be an object or array")


def load_export_records(path: str | os.PathLike[str]) -> list[Mapping[str, Any]]:
    """Load a JSON array/object or newline-delimited JSON export."""
    export_path = Path(path)
    text = export_path.read_text(encoding="utf-8-sig")
    stripped = text.lstrip()
    if not stripped:
        return []

    if stripped[0] in "[{":
        try:
            return _extract_records(json.loads(text))
        except json.JSONDecodeError:
            pass

    records: list[Mapping[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at line {line_number}: {exc.msg}") from exc
        if not isinstance(value, Mapping):
            raise ValueError(f"JSONL line {line_number} must contain an object")
        records.append(value)
    return records


class ImportDisposition(str, Enum):
    CREATED = "created"
    UNCHANGED = "unchanged"
    DRIFTED = "drifted"
    REJECTED = "rejected"


@dataclass(frozen=True)
class MemoryRecord:
    casebrain_id: str
    object_type: str
    case_id: str
    title: str
    summary: str
    verification_status: str
    confidence: None
    source: Mapping[str, Any]
    relations: tuple[Mapping[str, Any], ...]
    metadata: Mapping[str, Any]
    created_at: str
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["relations"] = list(self.relations)
        return value

    @property
    def content_sha256(self) -> str:
        return str(self.metadata["content_sha256"])


@dataclass(frozen=True)
class ImportReceipt:
    connector_id: str
    run_id: str
    source_object_id: str
    canonical_id: str | None
    disposition: ImportDisposition
    source_sha256: str | None
    existing_sha256: str | None
    persisted_path: str | None
    occurred_at: str
    reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["disposition"] = self.disposition.value
        return value


@dataclass
class JsonlMemoryStore:
    """Append-only local projection used for deterministic ingestion and tests."""

    root: Path
    records_name: str = "records.jsonl"
    receipts_name: str = "receipts.jsonl"
    drift_name: str = "drift.jsonl"
    _index: MutableMapping[str, Mapping[str, Any]] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._index = self._load_index()

    @property
    def records_path(self) -> Path:
        return self.root / self.records_name

    @property
    def receipts_path(self) -> Path:
        return self.root / self.receipts_name

    @property
    def drift_path(self) -> Path:
        return self.root / self.drift_name

    def _load_index(self) -> dict[str, Mapping[str, Any]]:
        index: dict[str, Mapping[str, Any]] = {}
        if not self.records_path.exists():
            return index
        for line_number, line in enumerate(self.records_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            canonical_id = value.get("casebrain_id")
            if not isinstance(canonical_id, str):
                raise ValueError(f"Missing casebrain_id in {self.records_path}:{line_number}")
            index[canonical_id] = value
        return index

    def get(self, canonical_id: str) -> Mapping[str, Any] | None:
        return self._index.get(canonical_id)

    @staticmethod
    def _append(path: Path, value: Mapping[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(_canonical_json(value) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    def append_record(self, record: MemoryRecord) -> str:
        value = record.to_dict()
        self._append(self.records_path, value)
        self._index[record.casebrain_id] = value
        return str(self.records_path)

    def append_receipt(self, receipt: ImportReceipt) -> str:
        self._append(self.receipts_path, receipt.to_dict())
        return str(self.receipts_path)

    def append_drift(self, value: Mapping[str, Any]) -> str:
        self._append(self.drift_path, value)
        return str(self.drift_path)

    def verify(self) -> dict[str, Any]:
        checked = 0
        mismatches: list[str] = []
        for canonical_id, record in self._index.items():
            checked += 1
            metadata = record.get("metadata") or {}
            content = metadata.get("content")
            expected = metadata.get("content_sha256")
            if not isinstance(content, str) or not isinstance(expected, str):
                mismatches.append(canonical_id)
                continue
            if _sha256_text(content) != expected:
                mismatches.append(canonical_id)
        return {
            "checked": checked,
            "valid": not mismatches,
            "mismatches": mismatches,
            "records_path": str(self.records_path),
        }


@dataclass(frozen=True)
class KimiMemoryAdapter:
    connector_id: str = "CONN-KIMI-001"
    target_system: str = "AKOS"
    default_case_id: str = "GLOBAL"
    default_owner: str = "operator"

    def normalize(
        self,
        raw: Mapping[str, Any],
        *,
        source_uri: str,
        case_id: str | None = None,
        owner: str | None = None,
        imported_at: str | None = None,
    ) -> MemoryRecord:
        content = _extract_content(raw)
        if not content:
            raise ValueError("Record has no importable content")

        source_object_id = _coerce_text(_first(raw, "id", "memory_id", "conversation_id", "uuid"))
        if not source_object_id:
            source_object_id = _sha256_text(_canonical_json(raw))[:24]

        created_at = _coerce_text(_first(raw, "created_at", "createdAt", "timestamp", "date")) or imported_at or _utc_now()
        updated_at = _coerce_text(_first(raw, "updated_at", "updatedAt", "modified_at")) or created_at
        title = _coerce_text(_first(raw, "title", "name", "subject")) or content.splitlines()[0][:120]
        content_sha256 = _sha256_text(content)
        canonical_id = _stable_id("kimi", source_object_id)

        metadata = {
            "connector_id": self.connector_id,
            "content": content,
            "content_sha256": content_sha256,
            "source_object_id": source_object_id,
            "source_system": "kimi",
            "target_system": self.target_system,
            "target_location": "casebrain/connector_object",
            "review_state": "working",
            "owner": owner or self.default_owner,
            "imported_at": imported_at or _utc_now(),
            "raw_metadata": {
                key: value
                for key, value in raw.items()
                if key not in {"content", "memory", "text", "body", "summary", "message", "messages"}
            },
        }

        return MemoryRecord(
            casebrain_id=canonical_id,
            object_type="connector_object",
            case_id=case_id or self.default_case_id,
            title=title,
            summary=content[:500],
            verification_status="unverified",
            confidence=None,
            source={
                "system": "kimi",
                "uri": source_uri,
                "object_id": source_object_id,
                "sha256": content_sha256,
                "page_start": None,
                "page_end": None,
                "line_start": None,
                "line_end": None,
                "time_start_ms": None,
                "time_end_ms": None,
                "extraction_method": "export_normalization",
            },
            relations=(),
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
        )

    def import_records(
        self,
        raw_records: Iterable[Mapping[str, Any]],
        store: JsonlMemoryStore,
        *,
        source_uri: str,
        case_id: str | None = None,
        owner: str | None = None,
        dry_run: bool = False,
        run_id: str | None = None,
    ) -> list[ImportReceipt]:
        run = run_id or f"KIMI-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        receipts: list[ImportReceipt] = []

        for raw in raw_records:
            source_object_id = _coerce_text(_first(raw, "id", "memory_id", "conversation_id", "uuid")) or "derived"
            try:
                record = self.normalize(
                    raw,
                    source_uri=source_uri,
                    case_id=case_id,
                    owner=owner,
                )
            except ValueError as exc:
                receipt = ImportReceipt(
                    connector_id=self.connector_id,
                    run_id=run,
                    source_object_id=source_object_id,
                    canonical_id=None,
                    disposition=ImportDisposition.REJECTED,
                    source_sha256=None,
                    existing_sha256=None,
                    persisted_path=None,
                    occurred_at=_utc_now(),
                    reason=str(exc),
                )
                if not dry_run:
                    store.append_receipt(receipt)
                receipts.append(receipt)
                continue

            existing = store.get(record.casebrain_id)
            if existing is None:
                path = None if dry_run else store.append_record(record)
                disposition = ImportDisposition.CREATED
                existing_sha = None
            else:
                existing_metadata = existing.get("metadata") or {}
                existing_sha = existing_metadata.get("content_sha256")
                if existing_sha == record.content_sha256:
                    disposition = ImportDisposition.UNCHANGED
                    path = str(store.records_path)
                else:
                    disposition = ImportDisposition.DRIFTED
                    path = None
                    if not dry_run:
                        store.append_drift(
                            {
                                "connector_id": self.connector_id,
                                "run_id": run,
                                "canonical_id": record.casebrain_id,
                                "existing_sha256": existing_sha,
                                "incoming_sha256": record.content_sha256,
                                "incoming_record": record.to_dict(),
                                "detected_at": _utc_now(),
                                "review_required": True,
                            }
                        )

            receipt = ImportReceipt(
                connector_id=self.connector_id,
                run_id=run,
                source_object_id=str(record.source["object_id"]),
                canonical_id=record.casebrain_id,
                disposition=disposition,
                source_sha256=record.content_sha256,
                existing_sha256=existing_sha if isinstance(existing_sha, str) else None,
                persisted_path=path,
                occurred_at=_utc_now(),
                reason="silent overwrite blocked" if disposition is ImportDisposition.DRIFTED else None,
            )
            if not dry_run:
                store.append_receipt(receipt)
            receipts.append(receipt)

        return receipts


def memoryplugin_line(record: MemoryRecord) -> str:
    """Render one portable MemoryPlugin line from a normalized record."""
    content = str(record.metadata["content"]).replace("\r\n", "\n").replace("\r", "\n").strip()
    return f"tool=memoryplugin&&memory={content}"


def _summary(receipts: Iterable[ImportReceipt]) -> dict[str, int]:
    counts = {item.value: 0 for item in ImportDisposition}
    for receipt in receipts:
        counts[receipt.disposition.value] += 1
    return counts


def _cmd_import(args: argparse.Namespace) -> int:
    records = load_export_records(args.input)
    store = JsonlMemoryStore(Path(args.store))
    adapter = KimiMemoryAdapter(default_case_id=args.case_id, default_owner=args.owner)
    receipts = adapter.import_records(
        records,
        store,
        source_uri=args.source_uri or Path(args.input).resolve().as_uri(),
        case_id=args.case_id,
        owner=args.owner,
        dry_run=args.dry_run,
    )
    print(json.dumps({"summary": _summary(receipts), "receipts": [r.to_dict() for r in receipts]}, indent=2))
    return 0 if not any(r.disposition is ImportDisposition.REJECTED for r in receipts) else 2


def _cmd_verify(args: argparse.Namespace) -> int:
    result = JsonlMemoryStore(Path(args.store)).verify()
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import Kimi memory exports into an AKOS JSONL projection")
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_parser = subparsers.add_parser("import", help="Normalize and import JSON/JSONL records")
    import_parser.add_argument("--input", required=True)
    import_parser.add_argument("--store", required=True)
    import_parser.add_argument("--source-uri")
    import_parser.add_argument("--case-id", default="GLOBAL")
    import_parser.add_argument("--owner", default="operator")
    import_parser.add_argument("--dry-run", action="store_true")
    import_parser.set_defaults(func=_cmd_import)

    verify_parser = subparsers.add_parser("verify", help="Verify stored content hashes")
    verify_parser.add_argument("--store", required=True)
    verify_parser.set_defaults(func=_cmd_verify)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
