import asyncio
import os
from dotenv import load_dotenv
from aicog_v2 import AiCogClient, GroqProvider, OpenAIProvider, RedisCache, SQLiteStorage

# Load environment variables (API Keys)
load_dotenv()

async def run_demo():
    print("--- AiCog V2 Production Demo ---")

    # 1. Initialize Infrastructure (Redis & SQLite Storage)
    # Note: Ensure Redis is running on localhost:6379
    cache = RedisCache(host='127.0.0.1', port=6379)
    storage = SQLiteStorage("aicog_audit_v2.db")
    await storage.init_db()

    # 2. Setup Multi-Provider Access
    providers = {
        "groq": GroqProvider(api_key=os.getenv("GROQ_API_KEY")),
        "openai": OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY", "optional_key_here"))
    }

    # 3. Create the Main Client
    sdk = AiCogClient(
        providers=providers,
        cache=cache,
        storage=storage,
        default_provider="groq"
    )

    prompt = "What are the benefits of using Redis for distributed caching?"
    system_instr = "Answer as a senior DevOps engineer in 2 concise bullet points."

    try:
        # A. First Call (Goes to API)
        print("\n[Request 1] Fetching from API...")
        res1 = await sdk.generate(
            prompt=prompt,
            model="llama-3.1-8b-instant",
            system_prompt=system_instr
        )
        print(f"Content: {res1.content}")
        print(f"Stats: Latency={res1.latency:.2f}s, Cached={res1.cached}, Provider={res1.provider}")

        # B. Second Call (Goes to Redis Cache)
        print("\n[Request 2] Fetching from Redis Cache...")
        res2 = await sdk.generate(
            prompt=prompt,
            model="llama-3.1-8b-instant",
            system_prompt=system_instr
        )
        print(f"Content: {res2.content}")
        print(f"Stats: Latency={res2.latency:.2f}s, Cached={res2.cached}, Provider={res2.provider}")

        # C. Audit Trail Check
        print("\nAudit trail logged to 'aicog_audit_v2.db' for monitoring.")

    except Exception as e:
        print(f"Error occurred: {e}")
        print("Tip: Make sure Redis is running and API keys are valid.")

if __name__ == "__main__":
    asyncio.run(run_demo())
