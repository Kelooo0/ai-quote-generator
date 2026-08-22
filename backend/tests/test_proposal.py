import pytest
from fastapi import HTTPException, status

from backend.app.ai.mock_ai_service import MockAIService
from backend.app.schemas import AnalysisSchema, CompanyDataSchema, GeneratedProposalSchema


@pytest.mark.asyncio
async def test_proposal_success(client):
    analysis_response = await client.post(
        "/analyse",
        json={
            "content": (
                "Hi, we're a small e-commerce company selling sports equipment on Shopify."
                "We'd like to improve our organic traffic and rankings."
            )
        },
    )
    analysis = analysis_response.json()
    response = await client.post("/proposal", json=analysis)

    assert response.status_code == 200
    data = response.json()
    assert data["title"]
    assert data["introduction"]
    assert data["scope"]
    assert data["timeline"]


@pytest.mark.asyncio
async def test_proposal_ai_service_error(client, monkeypatch: pytest.MonkeyPatch):
    async def mock_ai_service_error(
        self, *, analysis: AnalysisSchema, company_data: CompanyDataSchema, price: float
    ) -> GeneratedProposalSchema:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="An error occurred while generating proposal.",
        )

    monkeypatch.setattr(MockAIService, "generate_proposal", mock_ai_service_error)

    analysis_response = await client.post(
        "/analyse",
        json={
            "content": (
                "I need a custom website for my small business with five pages,"
                " a contact form, and basic SEO."
            )
        },
    )
    analysis = analysis_response.json()
    response = await client.post("/proposal", json=analysis)

    assert response.status_code == 502
