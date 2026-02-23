from typing import Tuple

class ModelRouter:
    """
    Intelligently routes tasks to the best provider and model based on 
    content and volume.
    """
    
    @staticmethod
    def classify_task(prompt: str) -> str:
        prompt_lower = prompt.lower()
        if any(w in prompt_lower for w in ["reason", "analyze", "explain why", "complex"]):
            return "reasoning"
        if any(w in prompt_lower for w in ["summarize", "tl;dr", "wrap up"]):
            return "summarization"
        if any(w in prompt_lower for w in ["extract", "json", "csv", "format"]):
            return "extraction"
        return "general"

    def route(self, prompt: str, token_count: int) -> Tuple[str, str]:
        """
        Returns (provider_name, model_name)
        """
        task = self.classify_task(prompt)
        
        # 1. High-Volume / Long Context -> Groq (Llama 3.3)
        if token_count > 4000 or task == "summarization":
            return "groq", "llama-3.3-70b-versatile"
        
        # 2. Deep Reasoning -> OpenAI (if configured) or Groq Llama 3.3
        if task == "reasoning":
            return "groq", "llama-3.3-70b-versatile" # Defaulting to Groq for speed
            
        # 3. Fast / Simple Tasks -> Groq (Llama 8B)
        return "groq", "llama-3.1-8b-instant"
