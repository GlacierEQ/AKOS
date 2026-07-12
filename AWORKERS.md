# AWorkers — Workers of Workers + Unified Memory

Meta layer for GlacierEQ: plan → dispatch workers → merge shared memory.

## Architecture

```
L0 META     plan / assign / merge memory
L1 LOCAL    flippers (zero LLM, parallel)
L1.5 RESEARCH  Smithery Exa (+ Tavily when connected)
L2 SWARM    pistons + codex / stealth / omni
L3 SDAL     Notion case workers (1FDV lattice)
L4 MESH     notion-workers-mesh waves
     ↕
UNIFIED MEMORY  hot → warm → cool → cold
```

**Memory rule:** facts + pointers only — never full dumps into hot memory.

## Local control plane (operator machine)

```bash
python3 ~/GlacierEQ_Swarm/automations/aworkers_orchestrator.py status
python3 ~/GlacierEQ_Swarm/automations/aworkers_orchestrator.py run \
  --goal "massive pack" \
  --cathedral "Family Court" \
  --case "1FDV-23-0001009"
```

### State files

| Path | Role |
|------|------|
| `GlacierEQ_Swarm/state/unified_memory.json` | Shared bus |
| `GlacierEQ_Swarm/state/aworkers_registry.json` | Layer registry |
| `GlacierEQ_Swarm/state/aworkers_last_run.json` | Last pack result |
| `GlacierEQ_Swarm/state/research_last.json` | L1.5 research ptr |

### L1 flippers (default pack)

- `device-stability-flipper.py`
- `token-100pct-savings-flipper.py`
- `github-ecosystem-analyzer.py`
- `aeon-moc-procode-scanner.py`
- `qualification-savings-flipper.py`

## Always-on agent core (Grok)

From `~/AGENTS.md`:

1. **token-saver** — externalize, pure_pointer for large payloads
2. **sequential_thinking** MCP — multi-step reason / revise / branch
3. **ai-humanizer** MCP — final user-facing prose only (never code/evidence/JSON)

## Notion

- AWorkers page under AKOS + Grok Control Hub (workspace FIRST)
- SDAL workers dashboard (1FDV)
- Worker Registry & Health

## Massive work recipe

1. Load unified_memory + cathedral/case
2. Sequential → packets
3. L1 first (cheap parallel)
4. L1.5 research if needed
5. L3/L4 case mesh
6. L2 LLM only for residue
7. Merge memory · humanize final prose · Verification Ledger if claiming live

## Packet contract

`goal_id · worker_id · layer · inputs_ptr · outputs_ptr · memory_write · status`

---
*Synced from local GlacierEQ_Swarm · 2026-07-12*
