from backend.app.ai.ai_service import AIService
from backend.app.ai.base import AIBase
from backend.app.ai.mock_ai_service import MockAIService
from backend.app.config import settings


def ai_service() -> AIBase:
    if settings.LLM_PROVIDER == "openai":
        return AIService()
    return MockAIService()
