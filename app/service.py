import json

from fastapi import HTTPException, status

from app.ai.base import AIBase
from app.config import settings
from app.schemas import AnalysisSchema, CompanyDataSchema, PricingSchema


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
            self.services = self.company_data.services
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Application configuration incorrect.",
            ) from exc
        if set(self.services) != set(self.pricing.prices):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Company services and pricing services do not match.",
            )

    async def analyse_message_service(self, message_content: str) -> AnalysisSchema:
        analysis = await self.ai.generate_analysis(message_content, self.services)
        for r in analysis.requirements:
            if r.service not in self.services:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="AI returned an unavailable service.",
                )
        return analysis
