from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_service
from app.schemas import AnalysisSchema, ClientMessage, FinalProposalSchema
from app.service import Service

router = APIRouter()


@router.post("/analyse")
async def analyse(
    client_message: ClientMessage, service: Annotated[Service, Depends(get_service)]
) -> AnalysisSchema:
    return await service.analysis_service(client_message.content)


@router.post("/proposal")
async def proposal(
    analysis: AnalysisSchema, service: Annotated[Service, Depends(get_service)]
) -> FinalProposalSchema:
    return await service.proposal_service(analysis)
