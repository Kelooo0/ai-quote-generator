import json

from fastapi import HTTPException, status

from app.ai.base import AIBase
from app.config import settings
from app.schemas import AnalysisSchema, CompanyDataSchema, FinalProposalSchema, PricingSchema


class Service:
    def __init__(self, ai: AIBase) -> None:
        self.ai = ai
        try:
            with open(settings.PRICING_FILE, encoding="utf-8") as file:
                self.pricing = json.load(file)
            with open(settings.COMPANY_DATA_FILE, encoding="utf-8") as file:
                self.company_data = json.load(file)
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Application configuration incomplete.",
            ) from exc
        try:
            self.company_data = CompanyDataSchema.model_validate(self.company_data)
            self.pricing = PricingSchema.model_validate(self.pricing)
            self.prices = self.pricing.prices
            self.available_services = self.company_data.services
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Application configuration incorrect.",
            ) from exc
        if set(self.available_services) != set(self.pricing.prices):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Company services and pricing services do not match.",
            )

    def calculate_price(self, required_services: list[str]) -> float:
        price = 0
        for service in required_services:
            price += self.prices[service]
        return price

    async def analysis_service(self, message_content: str) -> AnalysisSchema:
        analysis = await self.ai.generate_analysis(message_content, self.available_services)
        # Add a condition checking if ai returned any requirements
        for r in analysis.requirements:
            if r.service not in self.available_services:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="AI returned an unavailable service.",
                )
        return analysis

    async def proposal_service(self, analysis: AnalysisSchema) -> FinalProposalSchema:
        required_services = [r.service for r in analysis.requirements]
        price = self.calculate_price(required_services)
        generated_proposal = await self.ai.generate_proposal(
            analysis=analysis, company_data=self.company_data, price=price
        )
        return FinalProposalSchema(
            **generated_proposal.model_dump(), price=price, currency=self.company_data.currency
        )
