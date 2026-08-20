from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_service
from app.schemas import AnalysisSchema, ClientMessage
from app.service import Service

router = APIRouter()


@router.post("/analyse")
async def analyse_message(
    client_message: ClientMessage, service: Annotated[Service, Depends(get_service)]
) -> AnalysisSchema:
    return await service.analyse_message_service(client_message.content)
