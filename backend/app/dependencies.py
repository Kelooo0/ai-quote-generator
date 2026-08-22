from typing import Annotated

from fastapi import Depends

from backend.app.ai.base import AIBase
from backend.app.ai.factory import ai_service
from backend.app.service import Service


def get_ai_service() -> AIBase:
    return ai_service()


def get_service(ai: Annotated[AIBase, Depends(get_ai_service)]) -> Service:
    return Service(ai=ai)
