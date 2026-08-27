from typing import Annotated

from fastapi import Depends

from app.ai.base import AIBase
from app.ai.factory import ai_service
from app.service import Service


def get_ai_service() -> AIBase:
    return ai_service()


def get_service(ai: Annotated[AIBase, Depends(get_ai_service)]) -> Service:
    return Service(ai=ai)
