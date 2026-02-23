import asyncio
import os
import sys
from dotenv import load_dotenv

# Windows console fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from aicog_v2 import AiCogClient, GroqProvider, RedisCache

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

async def run_test():
    # 1. Setup with Redis Cache
    cache = RedisCache(host='127.0.0.1', port=6379)
    providers = {"groq": GroqProvider(api_key=api_key)}
    sdk = AiCogClient(providers=providers, cache=cache)

    prompt = "i have 8 eggs, i break two blend two and roast two and ate two.how many egg i have?"

    print("\n--- REQUEST 1 (Should be LIVE) ---")
    res1 = await sdk.generate(prompt=prompt)
    res1.display()

    print("\n--- REQUEST 2 (Should be CACHED) ---")
    res2 = await sdk.generate(prompt=prompt)
    res2.display()

if __name__ == "__main__":
    asyncio.run(run_test())
