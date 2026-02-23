import time
import hashlib
import json
from typing import Optional, Dict, Any, Union

from aicog_v2.core.interfaces import AIResponse, AIProvider
from aicog_v2.cache.redis_backend import RedisCache
from aicog_v2.storage.sqlite_backend import SQLiteStorage
from aicog_v2.core.routing import ModelRouter
from aicog_v2.core.utils import TokenEstimator

class AiCogClient:
    def __init__(
        self,
        providers: Dict[str, AIProvider],
        cache: Optional[RedisCache] = None,
        storage: Optional[SQLiteStorage] = None,
        default_provider: str = "groq"
    ):
        self.providers = providers
        self.cache = cache
        self.storage = storage
        self.default_provider = default_provider
        self.router = ModelRouter()

    def _generate_cache_key(self, prompt: str, model: str, system_prompt: Optional[str]) -> str:
        data = f"{system_prompt or ''}:{prompt}:{model}"
        return hashlib.sha256(data.encode()).hexdigest()

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        provider_name: Optional[str] = None,
        system_prompt: Optional[str] = None,
        use_cache: bool = True,
        **kwargs
    ) -> AIResponse:
        # 0. Auto-Routing (If model is not specified)
        if not model:
            token_est = TokenEstimator.estimate(prompt)
            provider_name, model = self.router.route(prompt, token_est)
        else:
            provider_name = provider_name or self.default_provider
        provider = self.providers.get(provider_name)
        
        if not provider:
            raise ValueError(f"Provider {provider_name} not configured.")

        # 1. Cache Lookup
        cache_key = self._generate_cache_key(prompt, model, system_prompt)
        if use_cache and self.cache:
            cached_val = await self.cache.get(cache_key)
            if cached_val:
                data = json.loads(cached_val)
                return AIResponse(
                    content=data["content"],
                    model=model,
                    provider=provider_name,
                    usage=data.get("usage", {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}),
                    latency=data.get("latency", 0.0),
                    cached=True
                )

        # 2. API Call
        response = await provider.generate(prompt, model, system_prompt, **kwargs)

        # 3. Store in Cache
        if use_cache and self.cache:
            cache_data = {
                "content": response.content,
                "usage": response.usage,
                "latency": response.latency
            }
            await self.cache.set(cache_key, json.dumps(cache_data))

        # 4. Persistence Logging
        if self.storage:
            await self.storage.log_request(
                provider=provider_name,
                model=model,
                prompt=prompt,
                response=response.content,
                latency=response.latency,
                usage=response.usage
            )

        return response
