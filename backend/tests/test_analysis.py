import pytest
from fastapi import HTTPException, status

from backend.app.ai.mock_ai_service import MockAIService
from backend.app.schemas import AnalysisSchema, Requirement


@pytest.mark.asyncio
async def test_analysis_success(client):
    response = await client.post(
        "/analyse",
        json={
            "content": (
                "Hi, we're a small e-commerce company selling sports equipment on Shopify."
                "We'd like to improve our organic traffic and rankings."
            )
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["client_summary"]
    assert data["service_type"]
    assert data["requirements"]


@pytest.mark.asyncio
async def test_analysis_requirements(client):
    response = await client.post(
        "/analyse",
        json={
            "content": (
                "Hi, we're a small e-commerce company selling sports equipment on Shopify."
                "We'd like to improve our organic traffic and rankings."
            )
        },
    )
    assert response.status_code == 200
    requirements = response.json()["requirements"]
    for req in requirements:
        assert req["service"]
        assert req["details"]


@pytest.mark.asyncio
async def test_analysis_unavailable_service(client, monkeypatch: pytest.MonkeyPatch):
    async def mock_analysis_unavailable_service(
        self, message_content: str, available_services: list[str]
    ) -> AnalysisSchema:
        return AnalysisSchema(
            client_summary="Client wants a custom website for their business.",
            service_type="Web Development",
            scope="medium",
            requirements=[
                Requirement(
                    service="Custom website",
                    details=["5 pages", "Contact form"],
                )
            ],
            timeline="4 weeks",
            budget=None,
            missing_information=[],
            assumptions=[],
        )

    monkeypatch.setattr(MockAIService, "generate_analysis", mock_analysis_unavailable_service)

    response = await client.post(
        "/analyse",
        json={
            "content": (
                "I need a custom website for my small business with five pages,"
                " a contact form, and basic SEO."
            )
        },
    )

    assert response.status_code == 502


@pytest.mark.asyncio
async def test_analysis_invalid_input(client):
    response = await client.post("/analyse", json={"content": "Too short client message"})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analysis_ai_service_error(client, monkeypatch: pytest.MonkeyPatch):
    async def mock_ai_service_error(
        self, message_content: str, available_services: list[str]
    ) -> AnalysisSchema:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="An error occurred while generating proposal.",
        )

    monkeypatch.setattr(MockAIService, "generate_analysis", mock_ai_service_error)

    response = await client.post(
        "/analyse",
        json={
            "content": (
                "I need a custom website for my small business with five pages,"
                " a contact form, and basic SEO."
            )
        },
    )

    assert response.status_code == 502
