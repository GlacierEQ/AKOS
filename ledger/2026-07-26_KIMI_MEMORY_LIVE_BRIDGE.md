# Kimi + MemoryPlugin Live Bridge Receipt

Date: 2026-07-26  
Connector: `CONN-KIMI-001`  
Repository: `GlacierEQ/AKOS`  
Status: Runtime implemented; authenticated provider probe pending

## Implemented

- standard-library bearer-authenticated HTTP client;
- Moonshot `GET /v1/models` credential probe;
- Moonshot `GET /v1/users/me/balance` support;
- Moonshot `POST /v1/chat/completions` support using `kimi-k3` by default;
- MemoryPlugin `GET /api/v2/memory` recall/search;
- MemoryPlugin `POST /api/memory` creation;
- Honolulu-time date prefix for new memories;
- recalled-memory injection into Kimi with explicit unverified-context framing;
- secret-free SHA-256 provider receipts;
- local secret template with no credential values;
- CLI commands: `probe`, `recall`, `remember`, and `ask`.

## Local verification

```text
python -m compileall -q operational_cognition/connectors
python -m unittest -v operational_cognition.test_live_memory
```

Result:

```text
6 tests passed
```

Covered controls:

- missing-secret rejection;
- official Moonshot models endpoint binding;
- MemoryPlugin create payload and date prefix;
- MemoryPlugin-to-Kimi context injection;
- provider error redaction;
- receipt credential exclusion.

## Provider truth state

```text
Moonshot contract: VERIFIED from current official OpenAPI
MemoryPlugin contract: VERIFIED from current official API documentation
Runtime code: VERIFIED locally
Credential binding: PENDING
Provider invocation: PENDING
Provider return: PENDING
Provider receipt: PENDING
```

The connector remains `Ready for Authenticated Test`, not `CONNECTED`, until both operator credentials are injected outside Git and `python -m operational_cognition.connectors.live_memory probe` returns successfully with persisted provider receipts.

## Security note

Prior project context indicated raw API credentials had previously appeared in portable memory. Existing values should be treated as exposed and rotated before binding. No credential value was read, copied, logged, or committed during this implementation.
