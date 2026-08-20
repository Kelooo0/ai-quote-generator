from abc import ABC, abstractmethod

from app.schemas import AnalysisSchema, CompanyDataSchema


class AIBase(ABC):
    @abstractmethod
    async def generate_analysis(self, message_content: str):
        pass

    @abstractmethod
    async def generate_proposal(
        self, *, analysis: AnalysisSchema, company_data: CompanyDataSchema, price: float
    ):
        pass
