from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.ai.base import AIBase
from app.config import settings
from app.dependencies import get_ai_service
from app.main import app


@pytest.fixture(autouse=True)
def useMock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "LLM_PROVIDER", "mock")


@pytest.fixture
def ai_service() -> AIBase:
    return get_ai_service()


@pytest_asyncio.fixture
async def client(ai_service) -> AsyncGenerator[AsyncClient]:
    def override_ai_service():
        yield ai_service

    app.dependency_overrides[get_ai_service] = override_ai_service

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
