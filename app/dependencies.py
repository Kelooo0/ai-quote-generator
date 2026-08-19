from app.ai.base import AIBase
from app.ai.factory import ai_service


def get_ai_service() -> AIBase:
    return ai_service()
