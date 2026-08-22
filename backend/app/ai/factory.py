from app.ai.ai_service import AIService
from app.ai.base import AIBase
from app.ai.mock_ai_service import MockAIService
from app.config import settings


def ai_service() -> AIBase:
    if settings.LLM_PROVIDER == "openai":
        return AIService()
    return MockAIService()
