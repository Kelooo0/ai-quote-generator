from app.ai.base import AIBase
from app.schemas import AnalysisSchema, CompanyDataSchema


class MockAIService(AIBase):
    async def generate_analysis(self, message_content: str):
        return {"status": "this is mock response"}

    async def generate_proposal(
        self, *, analysis: AnalysisSchema, company_data: CompanyDataSchema, price: float
    ):
        return {"status": "this is mock response"}
