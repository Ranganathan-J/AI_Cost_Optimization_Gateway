import time
from typing import Optional, Dict
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential
from aicog_v2.core.interfaces import AIProvider, AIResponse

class GroqProvider(AIProvider):
    def __init__(self, api_key: str):
        self.client = AsyncGroq(api_key=api_key)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def generate(
        self, 
        prompt: str, 
        model: str, 
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        chat_completion = await self.client.chat.completions.create(
            messages=messages,
            model=model,
            **kwargs
        )

        latency = time.time() - start_time
        
        return AIResponse(
            content=chat_completion.choices[0].message.content,
            model=model,
            provider="groq",
            usage={
                "input_tokens": chat_completion.usage.prompt_tokens,
                "output_tokens": chat_completion.usage.completion_tokens,
                "total_tokens": chat_completion.usage.total_tokens
            },
            latency=latency
        )
