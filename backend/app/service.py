import json

from fastapi import HTTPException, status
from loguru import logger

from backend.app.ai.base import AIBase
from backend.app.config import settings
from backend.app.schemas import AnalysisSchema, CompanyDataSchema, FinalProposalSchema, PricingSchema


class Service:
    def __init__(self, ai: AIBase) -> None:
        self.ai = ai
        try:
            with open(settings.PRICING_FILE, encoding="utf-8") as file:
                self.pricing = json.load(file)
            with open(settings.COMPANY_DATA_FILE, encoding="utf-8") as file:
                self.company_data = json.load(file)
        except Exception as exc:
            logger.exception("Mandatory data files missing")
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
            logger.exception("Data files do not match the required schema")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Application configuration incorrect.",
            ) from exc
        if set(self.available_services) != set(self.pricing.prices):
            logger.error("Company services and pricing services do not match")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Application configuration incorrect.",
            )

    def calculate_price(self, required_services: list[str]) -> float:
        logger.debug("Calculating proper price for required services")
        price = 0
        for service in required_services:
            price += self.prices[service]
        logger.info("Returning calculated price")
        return price

    async def analysis_service(self, message_content: str) -> AnalysisSchema:
        logger.debug("Analysing client message")
        analysis = await self.ai.generate_analysis(message_content, self.available_services)
        if not analysis.requirements:
            logger.error("No supported services were identified in the client request")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="No supported services were identified in the client request.",
            )
        for r in analysis.requirements:
            if r.service not in self.available_services:
                logger.error("AI returned an unavailable service")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="AI returned an unavailable service.",
                )
        logger.info("Returning client message analysis")
        return analysis

    async def proposal_service(self, analysis: AnalysisSchema) -> FinalProposalSchema:
        logger.debug("Preparing proposal")
        required_services = [r.service for r in analysis.requirements]
        price = self.calculate_price(required_services)
        generated_proposal = await self.ai.generate_proposal(
            analysis=analysis, company_data=self.company_data, price=price
        )
        logger.info("Returning created proposal")
        return FinalProposalSchema(
            **generated_proposal.model_dump(), price=price, currency=self.company_data.currency
        )
