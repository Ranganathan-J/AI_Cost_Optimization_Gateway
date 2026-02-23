import asyncio
import os
import sys
from dotenv import load_dotenv

# Fix for Windows Console encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from aicog_v2 import AiCogClient, GroqProvider

# 1. Load your API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

async def quick_test():
    print("--- Running AiCog V2 Quick Health Check ---")

    if not api_key:
        print("Error: GROQ_API_KEY not found in environment.")
        return

    # 2. Minimal Setup (No Redis/Storage needed for a basic ping)
    providers = {"groq": GroqProvider(api_key=api_key)}
    sdk = AiCogClient(providers=providers)

    try:
        # 3. Test Auto-Routing & Generation
        print("Sending test request (Auto-routing)...")
        res = await sdk.generate(prompt="Ping! Are you working?")
        
        # 4. Display Results
        res.display()
        
        print("Library is WORKING properly!")
        
    except Exception as e:
        print(f"Library test FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(quick_test())
