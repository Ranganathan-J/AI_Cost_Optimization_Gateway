# AiCog V2 SDK 🚀

A professional, production-ready AI Gateway SDK built for high-performance, cost-efficient, and audited LLM operations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## 💡 What Problem It Solves

Building production-grade AI applications is harder than just calling an API. Developers face significant hurdles:

1.  **Redundant Costs**: Without caching, the same prompt "How does my app work?" costs money every single time.
2.  **Unreliable APIs**: LLM providers go down or timeout. Production apps need automatic retries.
3.  **Model Choice Fatigue**: Deciding which model to use (Llama-3 8B vs 70B) for every task is tedious.
4.  **Zero Visibility**: It's hard to track exactly how much you are spending and what your latency looks like for auditing.

**AiCog V2** solves this by acting as a **smart middleware**. It caches intelligently with Redis, auto-routes your tasks to the most efficient model, and logs every interaction to a local SQLite audit trail for professional monitoring.

---

## ✨ Features

- **Multi-Provider Support**: Unified interface for Groq, OpenAI, and DeepSeek (Anthropic coming soon).
- **Intelligent Auto-Routing**: Automatically selects the best model (e.g., Llama 3.1 8B vs 3.3 70B) based on your prompt's complexity and token length.
- **Async First**: Fully asynchronous architecture designed for high-concurrency modern Python backends (FastAPI, Django).
- **Distributed Caching**: Redis-backed distributed caching for scalable, multi-node deployments.
- **Audit Logging**: SQLite-based persistent storage for every request and response.
- **Fault Tolerance**: Automatic retries with exponential backoff using `Tenacity`.
- **Cost Estimation**: Built-in real-time cost calculation ($ USD) for every request.

---

## 🛠 Installation

### 1. Standard Install

```bash
pip install aicog-v2
```

### 2. Local Development Install

If you are developing or testing locally:

```bash
cd aicog_library_v2
pip install -e .
```

---

## 🚀 Quick Start

Ensure your Redis server is running at `127.0.0.1:6379`.

```python
import asyncio
import os
from aicog_v2 import AiCogClient, GroqProvider, RedisCache, SQLiteStorage

async def main():
    # 1. Initialize Infrastructure
    cache = RedisCache(host='127.0.0.1', port=6379)
    storage = SQLiteStorage("audit_trail.db")
    await storage.init_db()

    # 2. Configure Providers
    groq = GroqProvider(api_key=os.getenv("GROQ_API_KEY"))

    # 3. Initialize Client
    sdk = AiCogClient(
        providers={"groq": groq},
        cache=cache,
        storage=storage
    )

    # 4. Generate with Auto-Routing & Caching
    # No model specified -> The library chooses the best one for you!
    res = await sdk.generate(
        prompt="Explain Redis caching in 3 points",
        system_prompt="You are a systems architect."
    )

    # 5. Professional Display
    res.display()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📊 Usage Examples

### Manual Model Selection

```python
res = await sdk.generate(
    prompt="Write a hello world program",
    model="llama-3.1-8b-instant"
)
```

### Multi-Provider Setup

```python
from aicog_v2 import OpenAIProvider

sdk = AiCogClient(providers={
    "groq": GroqProvider(api_key="..."),
    "openai": OpenAIProvider(api_key="...")
})

# Route to OpenAI manually
res = await sdk.generate(prompt="...", provider_name="openai", model="gpt-4o")
```

### Accessing Audit Data

The audit trail is stored in your SQLite file. You can query it like this:

```python
import sqlite3
conn = sqlite3.connect("audit_trail.db")
cursor = conn.execute("SELECT model, latency, total_tokens FROM requests")
for row in cursor:
    print(row)
```

---

## 📁 Project Structure

- `aicog_v2/core/`: Abstract interfaces and internal utilities (Routing, Token estimation).
- `aicog_v2/providers/`: Concrete LLM implementations (Groq, OpenAI).
- `aicog_v2/cache/`: Redis-backed distributed caching backend.
- `aicog_v2/storage/`: SQLite-backed audit trails for observability.

---

## 🤝 Contributing

We welcome contributions! To get started:

1.  **Fork** the repository.
2.  **Clone** your fork.
3.  **Create a feature branch**: `git checkout -b feature/amazing-feature`
4.  **Install dev dependencies**: `pip install -r requirements.txt`
5.  **Run tests**: `pytest tests/` (Work in progress)
6.  **Commit your changes**: `git commit -m "Add some amazing feature"`
7.  **Push to the branch**: `git push origin feature/amazing-feature`
8.  **Open a Pull Request**.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
