from abc import ABC, abstractmethod

from backend.app.schemas import AnalysisSchema, CompanyDataSchema, GeneratedProposalSchema


class AIBase(ABC):
    @abstractmethod
    async def generate_analysis(
        self, message_content: str, available_services: list[str]
    ) -> AnalysisSchema:
        pass

    @abstractmethod
    async def generate_proposal(
        self, *, analysis: AnalysisSchema, company_data: CompanyDataSchema, price: float
    ) -> GeneratedProposalSchema:
        pass
