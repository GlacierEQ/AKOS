from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from operational_cognition.connectors.live_memory import (
    ConnectorConfigurationError,
    LiveMemoryBridge,
    MemoryPluginClient,
    MoonshotClient,
    ProviderHTTPError,
    write_receipt,
)


class FakeTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, method, url, headers, body, timeout):
        self.calls.append((method, url, dict(headers), body, timeout))
        return self.responses.pop(0)


class LiveMemoryTests(unittest.TestCase):
    def test_missing_secret_is_rejected(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConnectorConfigurationError):
                LiveMemoryBridge.from_env()

    def test_moonshot_probe_uses_official_models_endpoint(self):
        transport = FakeTransport([(200, {"x-request-id": "req-1"}, b'{"object":"list","data":[]}')])
        client = MoonshotClient(api_key="secret", transport=transport)
        result = client.probe()
        method, url, headers, body, _ = transport.calls[0]
        self.assertEqual((method, url, body), ("GET", "https://api.moonshot.ai/v1/models", None))
        self.assertEqual(headers["Authorization"], "Bearer secret")
        self.assertEqual(result.receipt.request_id, "req-1")

    def test_memory_create_date_prefix_and_source(self):
        transport = FakeTransport([(200, {}, b'{"done":"ok","memoryId":"abc"}')])
        client = MemoryPluginClient(api_key="secret", transport=transport, source="akos-test")
        client.create_memory("Connector is live.", date_override="2026-07-26")
        _, url, _, body, _ = transport.calls[0]
        self.assertEqual(url, "https://www.memoryplugin.com/api/memory")
        payload = json.loads(body.decode("utf-8"))
        self.assertEqual(payload["text"], "2026-07-26 - Connector is live.")
        self.assertEqual(payload["source"], "akos-test")

    def test_bridge_injects_memory_into_kimi_request(self):
        transport = FakeTransport(
            [
                (200, {}, b'{"memories":[{"text":"Use AKOS as governance root."}],"buckets":[]}'),
                (200, {}, b'{"choices":[{"message":{"content":"Acknowledged."}}]}'),
            ]
        )
        bridge = LiveMemoryBridge(
            MoonshotClient(api_key="moon", transport=transport),
            MemoryPluginClient(api_key="memory", transport=transport),
        )
        result = bridge.ask("Where does Kimi fit?")
        self.assertEqual(result["memory_count"], 1)
        chat_payload = json.loads(transport.calls[1][3].decode("utf-8"))
        self.assertIn("Use AKOS as governance root.", chat_payload["messages"][1]["content"])
        self.assertEqual(chat_payload["model"], "kimi-k3")

    def test_provider_error_does_not_echo_secret(self):
        transport = FakeTransport([(401, {}, b'{"error":{"message":"invalid key"}}')])
        client = MoonshotClient(api_key="super-secret", transport=transport)
        with self.assertRaises(ProviderHTTPError) as caught:
            client.probe()
        self.assertNotIn("super-secret", str(caught.exception))

    def test_receipt_file_contains_no_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_receipt(tmp, {"connected": True, "provider": "moonshot"}, prefix="probe")
            text = Path(path).read_text(encoding="utf-8")
            self.assertIn('"connected": true', text)
            self.assertNotIn("Bearer", text)
            self.assertNotIn("API_KEY", text)


if __name__ == "__main__":
    unittest.main()
