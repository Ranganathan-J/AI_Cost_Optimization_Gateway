import asyncio
import os
import sys
import redis.asyncio as redis
from dotenv import load_dotenv

# Fix for Windows Console encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from aicog_v2 import AiCogClient, GroqProvider, RedisCache

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

async def debug_cache():
    print("--- AiCog V2 Cache Debugger ---")
    
    # 1. Check Redis Connectivity
    print("🔍 Checking Redis connectivity (127.0.0.1:6379)...")
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, socket_connect_timeout=2)
        await r.ping()
        print("✅ Redis is alive and reachable.")
    except Exception as e:
        print(f"❌ Redis Connection Error: {e}")
        print("💡 TIP: Make sure you ran .\\redis-server.exe in the Redis folder.")
        return

    # 2. Setup Client with Cache
    cache = RedisCache(host='127.0.0.1', port=6379)
    providers = {"groq": GroqProvider(api_key=api_key)}
    sdk = AiCogClient(providers=providers, cache=cache)

    prompt = "Tell me a very short joke."
    
    print("\n[Step 1] Sending first request (Should be API Hit)...")
    res1 = await sdk.generate(prompt=prompt)
    res1.display()

    print("\n[Step 2] Sending identical request (Should be REDIS HIT)...")
    res2 = await sdk.generate(prompt=prompt)
    res2.display()

    if res2.cached:
        print("🎉 SUCCESS: Caching is working perfectly!")
    else:
        print("❌ FAILURE: Caching did not trigger on the second request.")

if __name__ == "__main__":
    asyncio.run(debug_cache())
