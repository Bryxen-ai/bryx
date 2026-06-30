# Bryx

> *古法编程 — writing agents the old way. One line at a time. No magic.*

[![Python](https://img.shields.io/badge/python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-WIP-orange.svg)]()

[简体中文](docs/README.zh.md)

---

## What is this?

Bryx is an agent loop, written from scratch in a few hundred lines of Python. No LangChain. No LlamaIndex. No AutoGen. Every piece — the tool dispatcher, the message protocol, the streaming client — is written out in the open.

I built this because after using agent frameworks for a while, I realized I couldn't explain how one actually works under the hood. So I tore it down to the bones and rebuilt it. Turns out an agent really is just: an LLM, a tool loop, and some state.

The whole codebase is small enough to read in one sitting. That's the point.

## Why not just use ${FRAMEWORK}?

If you want to ship a product fast, use a framework. Bryx is for when you want to *understand* what's happening — to debug a tool dispatch gone wrong without digging through six layers of abstraction, or to tweak the main loop without reading someone else's 20k-line codebase first.

It's also a decent starting point if you have opinions about how an agent should behave and don't want to fight a framework to express them.

## What's in the box

| What | Status |
|---|---|
| LLM client — Anthropic SDK wrapper with streaming, thinking mode, usage tracking | Done |
| Tool registry — register handlers, export schemas, async dispatch | Done |
| Main agent loop — `reason → act → observe` with error backoff | WIP |
| Built-in tools — `read`, `bash`, `edit`, `write` | Planned |
| Context compaction — auto-summarize when the message log gets too long | Planned |
| Skills — load `skills/<name>/SKILL.md` on demand | Planned |
| Global memory — `MEMORY.md` summary injected into context | Planned |
| Sub-agents — `create_agent` spawns an isolated child | Planned |
| CLI REPL / HTTP API | Planned |
| Self-evolution loop — propose → apply → evaluate, each attempt on its own Git branch | Planned |

First milestone: rebuild the core of an agent I wrote previously, by hand. Start from something that works, not a toy.

## Quick start

Python 3.14+. I use [uv](https://github.com/astral-sh/uv).

```bash
git clone https://github.com/loonghao/bryx.git
cd bryx

uv sync

# drop your API key in .env
cat > .env <<'EOF'
ANTHROPIC_API_KEY=sk-...
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-opus-4-8
EOF

uv run main.py
```

Works with anything that speaks the Anthropic wire format — Claude, DeepSeek through a gateway, etc. Just change `ANTHROPIC_BASE_URL`.

## Using it as a library

```python
import asyncio
from datetime import datetime
from src.agent.tools import ToolDef, ToolRegistry

async def now_handler(inp: dict) -> str:
    return datetime.now().isoformat()

NOW_SCHEMA = {
    "name": "now",
    "description": "get current date and time",
    "input_schema": {"type": "object", "properties": {}, "required": []},
}

registry = ToolRegistry()
registry.register(ToolDef(schema=NOW_SCHEMA, handler=now_handler))

# dispatch a tool call
result = asyncio.run(registry.dispatch("now", {}))
print(result)  # 2026-06-30T12:34:56.789012
```

## How the pieces fit together

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐
│  main.py │───▶│  Agent loop  │───▶│  LLM client  │
└──────────┘    │  (core.py)   │    │  (llm.py)    │
                └──────┬───────┘    └──────────────┘
                       │
                       ▼
                ┌──────────────┐
                │  ToolRegistry│
                │  (tools.py)  │
                └──────────────┘
```

- `llm.py` — thin wrapper around the Anthropic SDK. Streaming, thinking budget, token accounting. Swappable `base_url` for any compatible gateway.
- `tools.py` — register a handler, get schema export + async dispatch. No magic, just a `dict` and an `await`.
- `core.py` — the main loop (coming soon). `reason → act → observe`, repeat.

## Design rules

1. Only the official `anthropic` SDK. No orchestration libraries.
2. Code stays flat. No inheritance trees, no abstract base classes with one implementation.
3. Make it run first. Make it pretty later.
4. Stick to the Anthropic wire format. No custom message protocol.

## Contributing

This is early-stage. If you find a bug, have a use case, or want to port a piece to another LLM provider — open an issue. PRs are welcome but fair warning: I'm opinionated about keeping the codebase small.

## License

[MIT](LICENSE).
