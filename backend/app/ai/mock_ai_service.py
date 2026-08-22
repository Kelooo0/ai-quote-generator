from backend.app.ai.base import AIBase
from backend.app.schemas import AnalysisSchema, CompanyDataSchema, GeneratedProposalSchema, Requirement


class MockAIService(AIBase):
    async def generate_analysis(
        self, message_content: str, available_services: list[str]
    ) -> AnalysisSchema:
        return AnalysisSchema(
            client_summary="Client wants an SEO audit for their Shopify store.",
            service_type="SEO",
            scope="medium",
            requirements=[
                Requirement(
                    service="SEO Audit",
                    details=["Shopify store", "500 products"],
                )
            ],
            timeline="2 weeks",
            budget=None,
            missing_information=["Access to Google Search Console"],
            assumptions=[],
        )

    async def generate_proposal(
        self, *, analysis: AnalysisSchema, company_data: CompanyDataSchema, price: float
    ) -> GeneratedProposalSchema:
        return GeneratedProposalSchema(
            title="SEO Audit and Keyword Research Proposal",
            introduction=(
                "Thank you for reaching out. Based on your requirements, "
                "we can help improve your Shopify store's search visibility "
                "and reach the German market more effectively."
            ),
            scope=[
                "SEO Audit for the Shopify store",
                "Keyword Research focused on the German market",
            ],
            timeline="2 weeks",
        )
