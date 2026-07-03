<div align="center">

# 🧱 BRYX CLI

**An agent loop, hand-written. One line at a time. No magic.**

A few hundred lines of Python — tool dispatcher, message protocol, streaming client, all in the open. Small enough to read in one sitting.

[![Python](https://img.shields.io/badge/python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-WIP-orange.svg)]()

[What is this](#-what-is-this) · [Quick Start](#-quick-start) · [Library](#-using-it-as-a-library) · [Design](#-design-rules) · [简体中文](docs/README.zh.md)

</div>

---

## 💡 What is this

Bryx CLI is an agent loop, hand-written in a few hundred lines of Python. No LangChain, no LlamaIndex, no AutoGen. The tool dispatcher, the message protocol, the streaming client — every piece is out in the open.

After a while building with agent frameworks, I realized I couldn't explain how one actually worked under the hood. So I tore it down to the bones and rebuilt it. Turns out an agent really is just an LLM, a tool loop, and some state — small enough to read in one sitting. That's the point.

---

## 🤔 Why not just use `<FRAMEWORK>`

If you want to ship a product fast, use a framework. Bryx CLI is for when you want to *understand* what's happening — to debug a tool dispatch without digging through six layers of abstraction, or to tweak the main loop without reading 20k lines of someone else's code first.

It's also a decent scaffold if you have opinions about how an agent should behave and don't want to fight a framework to express them.

---

## ✅ Roadmap

**Shipped**

- [x] **LLM client** — Anthropic SDK wrapper with streaming, thinking mode, usage tracking
- [x] **Tool registry** — register handlers, export schemas, async dispatch

**In progress**

- [ ] **Agent loop** — `reason → act → observe` with error backoff

**Planned**

- [ ] **Built-in tools** — `read`, `bash`, `edit`, `write`
- [ ] **Context compaction** — auto-summarize when the message log grows too long
- [ ] **Skills** — load `skills/<name>/SKILL.md` on demand
- [ ] **Global memory** — `MEMORY.md` summary injected into context
- [ ] **Sub-agents** — `create_agent` spawns an isolated child
- [ ] **CLI REPL / HTTP API**
- [ ] **Self-evolution loop** — propose → apply → evaluate, each attempt on its own Git branch

> First milestone: rebuild the core of an agent I wrote previously, by hand. Start from something that works, not a toy.

---

## 🚀 Quick Start

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

Works with anything that speaks the Anthropic wire format — Claude, DeepSeek through a gateway, etc. Just swap `ANTHROPIC_BASE_URL`.

---

## 📦 Using it as a library

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

result = asyncio.run(registry.dispatch("now", {}))
print(result)  # 2026-06-30T12:34:56.789012
```

---

## 🧩 How the pieces fit together

```
   ┌──────────┐      ┌──────────────┐      ┌──────────────┐
   │ main.py  │ ───▶ │  Agent loop  │ ───▶ │  LLM client  │
   │ (entry)  │      │  (core.py)   │      │   (llm.py)   │
   └──────────┘      └──────┬───────┘      └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ ToolRegistry │
                     │  (tools.py)  │
                     └──────────────┘
```

- **`llm.py`** — thin wrapper around the Anthropic SDK. Streaming, thinking budget, token accounting. Swappable `base_url` for any compatible gateway.
- **`tools.py`** — register a handler, get schema export and async dispatch. No magic, just a `dict` and an `await`.
- **`core.py`** — the main loop (coming soon). `reason → act → observe`, repeat.

---

## 📐 Design rules

1. Only the official `anthropic` SDK. No orchestration libraries.
2. Code stays flat. No inheritance trees, no abstract base classes with one implementation.
3. Make it run first. Make it pretty later.
4. Stick to the Anthropic wire format. No custom message protocol.

---

## 🤝 Contributing

Early stage. If you find a bug, have a use case, or want to port a piece to another LLM provider — open an issue. PRs welcome, with fair warning: I'm opinionated about keeping the codebase small.

---

## 📄 License

[MIT](LICENSE).
