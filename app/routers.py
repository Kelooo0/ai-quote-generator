from typing import Annotated

from fastapi import APIRouter, Depends

from app.ai.base import AIBase
from app.dependencies import get_ai_service
from app.schemas import AnalysisSchema, ClientMessage

router = APIRouter()


@router.post("/analyse")
async def analyse(
    client_message: ClientMessage, ai: Annotated[AIBase, Depends(get_ai_service)]
) -> AnalysisSchema | None:
    return await ai.analyse_message(client_message.content)
