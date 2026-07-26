"""Authenticated Kimi + MemoryPlugin bridge for AKOS.

Secrets are read only from environment variables. No credential value is ever
written to a receipt or returned by the CLI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, MutableMapping, Sequence
from zoneinfo import ZoneInfo

Transport = Callable[[str, str, Mapping[str, str], bytes | None, float], tuple[int, Mapping[str, str], bytes]]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ConnectorConfigurationError(f"Missing required environment variable: {name}")
    return value


class ConnectorConfigurationError(RuntimeError):
    """Raised when required secret or endpoint configuration is absent."""


class ProviderHTTPError(RuntimeError):
    """Raised for non-success provider responses without exposing secrets."""

    def __init__(self, provider: str, status_code: int, message: str) -> None:
        super().__init__(f"{provider} request failed ({status_code}): {message}")
        self.provider = provider
        self.status_code = status_code
        self.message = message


@dataclass(frozen=True)
class ProviderReceipt:
    provider: str
    operation: str
    status_code: int
    occurred_at: str
    request_id: str | None
    response_sha256: str
    artifact_reference: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProviderResult:
    data: Any
    receipt: ProviderReceipt


def urllib_transport(
    method: str,
    url: str,
    headers: Mapping[str, str],
    body: bytes | None,
    timeout: float,
) -> tuple[int, Mapping[str, str], bytes]:
    request = urllib.request.Request(url=url, data=body, headers=dict(headers), method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return int(response.status), dict(response.headers.items()), response.read()
    except urllib.error.HTTPError as exc:
        return int(exc.code), dict(exc.headers.items()), exc.read()


@dataclass
class BearerJsonClient:
    provider: str
    api_key: str
    base_url: str
    transport: Transport = urllib_transport
    timeout: float = 30.0

    def _request(
        self,
        method: str,
        path: str,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Mapping[str, Any] | None = None,
        operation: str,
    ) -> ProviderResult:
        base = self.base_url.rstrip("/")
        url = f"{base}/{path.lstrip('/')}"
        if query:
            encoded = urllib.parse.urlencode(
                [
                    (key, str(value).lower() if isinstance(value, bool) else str(value))
                    for key, value in query.items()
                    if value is not None
                ]
            )
            url = f"{url}?{encoded}"

        body = None if payload is None else _canonical_json(payload).encode("utf-8")
        headers: MutableMapping[str, str] = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "AKOS-CONN-KIMI-001/0.2.0",
        }
        if body is not None:
            headers["Content-Type"] = "application/json"

        status, response_headers, response_body = self.transport(method, url, headers, body, self.timeout)
        response_sha = _sha256_bytes(response_body)
        request_id = (
            response_headers.get("x-request-id")
            or response_headers.get("X-Request-Id")
            or response_headers.get("request-id")
        )
        artifact_reference = url.split("?", 1)[0]

        try:
            data = json.loads(response_body.decode("utf-8")) if response_body else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            data = {"raw": response_body.decode("utf-8", errors="replace")}

        if not 200 <= status < 300:
            message = "provider error"
            if isinstance(data, Mapping):
                error = data.get("error")
                if isinstance(error, Mapping):
                    message = str(error.get("message") or error.get("code") or message)
                elif error:
                    message = str(error)
            raise ProviderHTTPError(self.provider, status, message)

        receipt = ProviderReceipt(
            provider=self.provider,
            operation=operation,
            status_code=status,
            occurred_at=_utc_now(),
            request_id=str(request_id) if request_id else None,
            response_sha256=response_sha,
            artifact_reference=artifact_reference,
            metadata={"response_bytes": len(response_body)},
        )
        return ProviderResult(data=data, receipt=receipt)


@dataclass
class MoonshotClient(BearerJsonClient):
    provider: str = "moonshot"
    api_key: str = ""
    base_url: str = "https://api.moonshot.ai"
    model: str = "kimi-k3"

    @classmethod
    def from_env(cls, *, transport: Transport = urllib_transport) -> "MoonshotClient":
        return cls(
            api_key=_require_env("MOONSHOT_API_KEY"),
            base_url=os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.ai").strip(),
            model=os.getenv("KIMI_MODEL", "kimi-k3").strip() or "kimi-k3",
            transport=transport,
        )

    def probe(self) -> ProviderResult:
        return self._request("GET", "/v1/models", operation="list_models")

    def balance(self) -> ProviderResult:
        return self._request("GET", "/v1/users/me/balance", operation="check_balance")

    def chat(
        self,
        messages: Sequence[Mapping[str, Any]],
        *,
        reasoning_effort: str = "high",
        max_completion_tokens: int = 2048,
    ) -> ProviderResult:
        payload = {
            "model": self.model,
            "messages": list(messages),
            "reasoning_effort": reasoning_effort,
            "max_completion_tokens": max_completion_tokens,
        }
        return self._request("POST", "/v1/chat/completions", payload=payload, operation="chat_completion")


@dataclass
class MemoryPluginClient(BearerJsonClient):
    provider: str = "memoryplugin"
    api_key: str = ""
    base_url: str = "https://www.memoryplugin.com"
    source: str = "akos-kimi"
    user_timezone: str = "Pacific/Honolulu"

    @classmethod
    def from_env(cls, *, transport: Transport = urllib_transport) -> "MemoryPluginClient":
        return cls(
            api_key=_require_env("MEMORY_PLUGIN_API_KEY"),
            base_url=os.getenv("MEMORY_PLUGIN_BASE_URL", "https://www.memoryplugin.com").strip(),
            source=os.getenv("AKOS_MEMORY_SOURCE", "akos-kimi").strip() or "akos-kimi",
            user_timezone=os.getenv("USER_TIMEZONE", "Pacific/Honolulu").strip() or "Pacific/Honolulu",
            transport=transport,
        )

    def probe(self) -> ProviderResult:
        return self.get_memories(latest=True, count=1)

    def get_memories(
        self,
        *,
        query_text: str | None = None,
        all_memories: bool | None = None,
        latest: bool | None = None,
        count: int = 10,
        skip: int = 0,
        bucket_id: int | None = None,
    ) -> ProviderResult:
        query = {
            "query": query_text,
            "all": all_memories,
            "latest": latest,
            "count": count,
            "skip": skip,
            "bucketId": bucket_id,
            "source": self.source,
            "v": 2,
        }
        return self._request("GET", "/api/v2/memory", query=query, operation="get_memories")

    def create_memory(
        self,
        text: str,
        *,
        bucket_id: int | None = None,
        prepend_date: bool = True,
        date_override: str | None = None,
    ) -> ProviderResult:
        clean = text.strip()
        if not clean:
            raise ValueError("Memory text cannot be empty")
        if prepend_date:
            date_value = date_override or datetime.now(ZoneInfo(self.user_timezone)).date().isoformat()
            if not clean.startswith(f"{date_value} "):
                clean = f"{date_value} - {clean}"
        payload: dict[str, Any] = {"text": clean, "source": self.source}
        if bucket_id is not None:
            payload["bucketId"] = bucket_id
        return self._request("POST", "/api/memory", payload=payload, operation="create_memory")


@dataclass
class LiveMemoryBridge:
    moonshot: MoonshotClient
    memoryplugin: MemoryPluginClient

    @classmethod
    def from_env(cls, *, transport: Transport = urllib_transport) -> "LiveMemoryBridge":
        return cls(MoonshotClient.from_env(transport=transport), MemoryPluginClient.from_env(transport=transport))

    def probe(self) -> dict[str, Any]:
        moonshot = self.moonshot.probe()
        memory = self.memoryplugin.probe()
        return {
            "connected": True,
            "moonshot": moonshot.receipt.to_dict(),
            "memoryplugin": memory.receipt.to_dict(),
        }

    def recall(self, query: str, *, count: int = 5) -> ProviderResult:
        return self.memoryplugin.get_memories(query_text=query, count=count)

    def ask(
        self,
        prompt: str,
        *,
        memory_count: int = 5,
        system_prompt: str | None = None,
        reasoning_effort: str = "high",
        max_completion_tokens: int = 2048,
    ) -> dict[str, Any]:
        recalled = self.recall(prompt, count=memory_count)
        memory_texts: list[str] = []
        data = recalled.data
        if isinstance(data, Mapping):
            memories = data.get("memories")
            if isinstance(memories, Sequence):
                for item in memories:
                    if isinstance(item, Mapping):
                        text = item.get("text")
                        if not isinstance(text, str):
                            metadata = item.get("metadata")
                            if isinstance(metadata, Mapping):
                                text = metadata.get("text")
                        if isinstance(text, str) and text.strip():
                            memory_texts.append(text.strip())
        elif isinstance(data, Sequence) and not isinstance(data, (str, bytes, bytearray)):
            memory_texts.extend(str(item).strip() for item in data if str(item).strip())

        context = "\n\n".join(f"- {text}" for text in memory_texts) or "- No relevant memory returned."
        messages = [
            {
                "role": "system",
                "content": system_prompt
                or "You are Kimi operating as an AKOS edge agent. Use supplied memory as context, not as automatically verified fact. Distinguish facts, assertions, and inferences.",
            },
            {"role": "system", "content": f"Relevant MemoryPlugin context:\n{context}"},
            {"role": "user", "content": prompt},
        ]
        answer = self.moonshot.chat(
            messages,
            reasoning_effort=reasoning_effort,
            max_completion_tokens=max_completion_tokens,
        )
        return {
            "memory_count": len(memory_texts),
            "memory_receipt": recalled.receipt.to_dict(),
            "kimi_receipt": answer.receipt.to_dict(),
            "completion": answer.data,
        }


def write_receipt(receipt_dir: str | os.PathLike[str], payload: Mapping[str, Any], *, prefix: str) -> str:
    root = Path(receipt_dir)
    root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()[:12]
    path = root / f"{prefix}-{timestamp}-{digest}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return str(path)


def _extract_completion_text(data: Any) -> str | None:
    if not isinstance(data, Mapping):
        return None
    choices = data.get("choices")
    if not isinstance(choices, Sequence) or not choices:
        return None
    first = choices[0]
    if not isinstance(first, Mapping):
        return None
    message = first.get("message")
    if not isinstance(message, Mapping):
        return None
    content = message.get("content")
    return content if isinstance(content, str) else None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Authenticated Kimi + MemoryPlugin bridge")
    parser.add_argument("--receipt-dir", default=".akos/receipts/kimi-memory")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("probe", help="Verify both provider credentials")

    recall = sub.add_parser("recall", help="Search MemoryPlugin")
    recall.add_argument("query")
    recall.add_argument("--count", type=int, default=5)

    remember = sub.add_parser("remember", help="Create one MemoryPlugin memory")
    remember.add_argument("text")
    remember.add_argument("--bucket-id", type=int)
    remember.add_argument("--no-date-prefix", action="store_true")

    ask = sub.add_parser("ask", help="Recall memory and ask Kimi")
    ask.add_argument("prompt")
    ask.add_argument("--memory-count", type=int, default=5)
    ask.add_argument("--reasoning-effort", choices=["low", "high", "max"], default="high")
    ask.add_argument("--max-completion-tokens", type=int, default=2048)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    bridge = LiveMemoryBridge.from_env()

    if args.command == "probe":
        payload = bridge.probe()
    elif args.command == "recall":
        result = bridge.recall(args.query, count=args.count)
        payload = {"data": result.data, "receipt": result.receipt.to_dict()}
    elif args.command == "remember":
        result = bridge.memoryplugin.create_memory(
            args.text,
            bucket_id=args.bucket_id,
            prepend_date=not args.no_date_prefix,
        )
        payload = {"data": result.data, "receipt": result.receipt.to_dict()}
    elif args.command == "ask":
        payload = bridge.ask(
            args.prompt,
            memory_count=args.memory_count,
            reasoning_effort=args.reasoning_effort,
            max_completion_tokens=args.max_completion_tokens,
        )
        payload["text"] = _extract_completion_text(payload.get("completion"))
    else:  # pragma: no cover
        raise AssertionError(args.command)

    receipt_path = write_receipt(args.receipt_dir, payload, prefix=args.command)
    print(json.dumps({"result": payload, "receipt_path": receipt_path}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
