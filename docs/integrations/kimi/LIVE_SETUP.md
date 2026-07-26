# CONN-KIMI-001 Live Setup

Status: Runtime implemented; secret binding and provider probe pending  
Version: 0.2.0  
Updated: 2026-07-26

## Secret contract

The live bridge reads credentials only from environment variables:

```text
MOONSHOT_API_KEY
MEMORY_PLUGIN_API_KEY
```

Do not place either value in Git, a tracked `.env`, command history, receipts, logs, issue comments, or pull-request text.

Use `config/kimi-memory.env.example` as the non-secret template.

## Local binding

```bash
mkdir -p ~/.config/akos
cp config/kimi-memory.env.example ~/.config/akos/kimi-memory.env
chmod 600 ~/.config/akos/kimi-memory.env
```

Edit `~/.config/akos/kimi-memory.env` and place the two newly issued credential values there. Then load them without echoing them:

```bash
set -a
. ~/.config/akos/kimi-memory.env
set +a
```

Previously exposed or copied credentials should be rotated before use.

## Authenticated probe

```bash
python -m operational_cognition.connectors.live_memory probe
```

The probe performs:

1. `GET https://api.moonshot.ai/v1/models`
2. `GET https://www.memoryplugin.com/api/v2/memory?latest=true&count=1&v=2`
3. secret-free provider receipt creation under `.akos/receipts/kimi-memory/`

A successful command is the first acceptable evidence that both credentials are authenticated. Code presence alone is not connection proof.

## Recall memory

```bash
python -m operational_cognition.connectors.live_memory recall \
  "What decisions did Casey make about Echoes?" \
  --count 5
```

## Store memory

MemoryPlugin requires the date to be prepended. The bridge does this automatically using `Pacific/Honolulu` unless `USER_TIMEZONE` is overridden.

```bash
python -m operational_cognition.connectors.live_memory remember \
  "Echoes uses AKOS governance and MemoryPlugin as a portable edge memory layer."
```

## Recall and ask Kimi

```bash
python -m operational_cognition.connectors.live_memory ask \
  "Summarize the current Echoes memory architecture and identify the next implementation step."
```

The bridge first retrieves relevant MemoryPlugin records, marks them as context rather than verified fact, injects them into the Kimi request, calls `kimi-k3`, and writes receipts for both providers.

## Optional configuration

```text
MOONSHOT_BASE_URL=https://api.moonshot.ai
MEMORY_PLUGIN_BASE_URL=https://www.memoryplugin.com
KIMI_MODEL=kimi-k3
AKOS_MEMORY_SOURCE=akos-kimi
USER_TIMEZONE=Pacific/Honolulu
```

Only override provider base URLs for an explicitly approved proxy or test server.

## Verification

```bash
python -m compileall -q operational_cognition/connectors
python -m unittest -v \
  operational_cognition.test_kimi_memory \
  operational_cognition.test_live_memory
```

Local authenticated-path regression result on 2026-07-26: six live-bridge tests passed. Provider authentication remains pending until a real probe receipt is produced with the operator's rotated keys.

## Truth boundary

- Kimi and MemoryPlugin are connector surfaces, not AKOS canon.
- Recalled memories are contextual records and may contain assertions, stale information, or contradictions.
- No imported or recalled item is automatically promoted to a verified fact, claim, event, evidence item, or legal artifact.
- No connection may be reported as authenticated without a successful provider response and persisted receipt.
