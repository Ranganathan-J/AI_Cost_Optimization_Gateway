from aicog_v2.core.routing import ModelRouter

def test_classify_task_reasoning():
    router = ModelRouter()
    assert router.classify_task("Explain why gravity exists") == "reasoning"

def test_classify_task_summarization():
    router = ModelRouter()
    assert router.classify_task("Summarize this article: ...") == "summarization"

def test_classify_task_general():
    router = ModelRouter()
    assert router.classify_task("Hi, how are you?") == "general"

def test_routing_logic_fast_task():
    router = ModelRouter()
    # Short general prompt should use 8B
    provider, model = router.route("Hello", 10)
    assert provider == "groq"
    assert model == "llama-3.1-8b-instant"

def test_routing_logic_complex_task():
    router = ModelRouter()
    # Complex/Reasoning prompt should use 70B
    provider, model = router.route("Explain why gravity exists", 50)
    assert provider == "groq"
    assert model == "llama-3.3-70b-versatile"
