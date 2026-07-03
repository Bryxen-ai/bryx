<div align="center">

# 🧱 BRYX CLI

**一行一行写出来的 Agent。没有魔法，全是明牌。**

几百行 Python —— 工具调度、消息协议、流式客户端，全部摊开。一口气能读完。

[![Python](https://img.shields.io/badge/python-3.14-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-WIP-orange.svg)]()

[介绍](#-这是什么) · [快速开始](#-快速开始) · [当库用](#-当库用) · [原则](#-原则) · [English](../README.md)

</div>

---

## 💡 这是什么

Bryx CLI 是一个从头手写的 Agent 框架，几百行 Python。不用 LangChain，不用 LlamaIndex，不用 AutoGen。工具调度、消息协议、流式客户端 —— 全部摊开在代码里，没有黑盒。

做这个项目的原因很简单：Agent 框架用多了，发现自己其实说不清一个 Agent 到底是怎么转起来的。那就拆到骨头，重新搭一遍。

真拆开了看，一个 Agent 不过就是：一个大模型、一个工具循环、一点状态。几百行 Python，够了。代码量小到能一口气读完，这就是整件事的意义。

---

## 🤔 为什么不用现成的框架

要快速交付产品，用框架。Bryx CLI 适合的场景是：你想*搞懂*一个 Agent 怎么运作 —— 工具调用为什么挂了，不想翻六层抽象去查；想改主循环的行为，不想先啃两万行别人的代码。

如果你对 Agent 的行为有自己的想法，又不想跟框架打架，Bryx CLI 也可以当一个起步的脚手架。

---

## ✅ 路线图

**已完成**

- [x] **LLM 客户端** —— Anthropic SDK 封装，流式、thinking、token 统计
- [x] **工具注册表** —— 注册 handler，导出 schema，异步调度

**进行中**

- [ ] **Agent 主循环** —— `reason → act → observe`，错误退避

**计划中**

- [ ] **内置工具** —— `read`、`bash`、`edit`、`write`
- [ ] **上下文压缩** —— 消息太长时自动摘要
- [ ] **技能加载** —— 按需加载 `skills/<name>/SKILL.md`
- [ ] **全局记忆** —— `MEMORY.md` 摘要注入上下文
- [ ] **子 Agent** —— `create_agent` 创建隔离的子代理
- [ ] **CLI REPL / HTTP API**
- [ ] **自进化循环** —— propose → apply → evaluate，每次实验一个 Git 分支

> 第一个里程碑：把我之前写的另一个 Agent 的核心能力，手写复刻一遍。从能真用的基线开始，不搞玩具 demo。

---

## 🚀 快速开始

Python 3.14+，我用 [uv](https://github.com/astral-sh/uv) 管理依赖。

```bash
git clone https://github.com/loonghao/bryx-cli.git
cd bryx-cli
uv sync

# 把 API key 写进 .env
cat > .env <<'EOF'
ANTHROPIC_API_KEY=sk-...
ANTHROPIC_BASE_URL=https://api.anthropic.com
ANTHROPIC_MODEL=claude-opus-4-8
EOF

uv run main.py
```

只要是 Anthropic 协议兼容的网关都能跑 —— Claude、DeepSeek 网关等等。改一下 `ANTHROPIC_BASE_URL` 就行。

---

## 📦 当库用

```python
import asyncio
from datetime import datetime
from src.agent.tools import ToolDef, ToolRegistry

async def now_handler(inp: dict) -> str:
    return datetime.now().isoformat()

NOW_SCHEMA = {
    "name": "now",
    "description": "获取当前日期时间",
    "input_schema": {"type": "object", "properties": {}, "required": []},
}

registry = ToolRegistry()
registry.register(ToolDef(schema=NOW_SCHEMA, handler=now_handler))

result = asyncio.run(registry.dispatch("now", {}))
print(result)  # 2026-06-30T12:34:56.789012
```

---

## 🧩 结构

```
   ┌──────────┐      ┌──────────────┐      ┌──────────────┐
   │ main.py  │ ───▶ │  Agent 主循环 │ ───▶ │  LLM 客户端  │
   │  (入口)  │      │  (core.py)   │      │   (llm.py)   │
   └──────────┘      └──────┬───────┘      └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  工具注册表  │
                     │  (tools.py)  │
                     └──────────────┘
```

- **`llm.py`** —— Anthropic SDK 的一层薄封装。流式、thinking 预算、token 统计。换 `base_url` 就能切网关。
- **`tools.py`** —— 注册 handler，自动导出 schema，异步调度。没有魔法，就是一个 `dict` 加一个 `await`。
- **`core.py`** —— 主循环（施工中）。`reason → act → observe`，周而复始。

---

## 📐 原则

1. 只依赖官方 `anthropic` SDK，不引入任何编排库。
2. 代码平铺。不搞继承树，不搞只有一个实现的抽象基类。
3. 先跑起来，再想好看。
4. 贴近 Anthropic 原始协议。不自创消息格式。

---

## 🤝 参与

项目还很早期。找到 bug、有使用场景、想适配其他 LLM 厂商 —— 都可以提 issue。欢迎 PR，但提前说清楚：我对保持代码小而精这件事比较执着。

---

## 📄 许可

[MIT](LICENSE)。
