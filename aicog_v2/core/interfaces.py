from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class AIResponse(BaseModel):
    content: str
    model: str
    provider: str
    usage: Dict[str, int]
    latency: float
    cached: bool = False

    @property
    def estimated_cost(self) -> float:
        """
        Heuristic cost calculation based on average market prices ($/1M tokens).
        Returns 0.0 if retrieved from cache.
        """
        if self.cached:
            return 0.0

        input_tokens = self.usage.get("input_tokens", 0)
        output_tokens = self.usage.get("output_tokens", 0)
        
        # Heuristic rates per 1M tokens
        rates = {
            "llama-3.3-70b-versatile": (0.59, 0.79),
            "llama-3.1-8b-instant": (0.05, 0.08),
            "gpt-4o": (5.0, 15.0),
            "gpt-4o-mini": (0.15, 0.60),
        }
        
        rate = rates.get(self.model, (0.10, 0.40)) # Default average rate
        cost = (input_tokens / 1_000_000 * rate[0]) + (output_tokens / 1_000_000 * rate[1])
        return cost

    def display(self):
        """
        Prints a professional, formatted summary of the response.
        """
        source = "REDIS CACHE (0 Tokens / $0.00)" if self.cached else f"LIVE API ({self.provider})"
        tokens_display = "0 (Cached)" if self.cached else str(self.usage.get('total_tokens', 0))
        
        print("\n" + "="*50)
        print(f"🤖 RESPONSE FROM: {source}")
        print("-" * 50)
        print(f"📄 Model   : {self.model}")
        print(f"⏱️ Latency : {self.latency:.3f}s")
        print(f"🎫 Tokens  : {tokens_display}")
        print(f"💰 Cost    : ${self.estimated_cost:.6f}")
        print("-" * 50)
        print(f"{self.content}")
        print("="*50 + "\n")

class AIProvider(ABC):
    @abstractmethod
    async def generate(
        self, 
        prompt: str, 
        model: str, 
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        pass

class AICache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    async def set(self, key: str, value: str, ttl: int = 3600):
        pass

class AIStorage(ABC):
    @abstractmethod
    async def log_request(
        self, 
        provider: str, 
        model: str, 
        prompt: str, 
        response: str, 
        latency: float, 
        usage: Dict[str, int]
    ):
        pass
