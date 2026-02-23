import asyncio
import os
from dotenv import load_dotenv
from aicog_v2 import AiCogClient, GroqProvider, RedisCache, SQLiteStorage

# Load environment variables (API Keys)
load_dotenv()

async def run_pro_demo():
    print("--- AiCog V2 Pro Feature Demo ---")
    print("Features: Auto-Routing, Latency Tracking, Token Usage & Cost Estimation\n")

    # 1. Initialize Infrastructure
    # Ensure Redis is running: .\redis-server.exe redis.windows.conf
    cache = RedisCache(host='127.0.0.1', port=6379)
    storage = SQLiteStorage("aicog_audit_pro.db")
    await storage.init_db()

    # 2. Setup Providers
    providers = {
        "groq": GroqProvider(api_key=os.getenv("GROQ_API_KEY")),
    }

    # 3. Create the Client
    sdk = AiCogClient(
        providers=providers,
        cache=cache,
        storage=storage
    )

    # TEST 1: AUTO-ROUTING (No model specified)
    print("[Task 1] Auto-routing a simple greeting...")
    res1 = await sdk.generate(
        prompt="Hi there! Just say hello.",
    )
    res1.display() # Use the new professional display method

    # TEST 2: COMPLEX TASK (Auto-routes to a larger model)
    print("[Task 2] Auto-routing a complex reasoning task...")
    complex_prompt = (
        "Explain the mathematical relationship between SHA-256 hashing and "
        "merkle trees in a blockchain context. Use technical terms."
    )
    res2 = await sdk.generate(
        prompt=complex_prompt,
        system_prompt="You are a senior cryptography engineer."
    )
    res2.display()

    # TEST 3: CACHING & COST (Zero cost for cache hits)
    print("[Task 3] Re-running Task 2 (Should be instant Redis hit)...")
    res3 = await sdk.generate(
        prompt=complex_prompt,
        system_prompt="You are a senior cryptography engineer."
    )
    res3.display()

if __name__ == "__main__":
    asyncio.run(run_pro_demo())
