from fastapi import HTTPException, status
from openai import AsyncOpenAI

from app.ai.base import AIBase
from app.config import settings
from app.schemas import AnalysisSchema, CompanyDataSchema, GeneratedProposalSchema


class AIService(AIBase):
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL

    async def generate_analysis(
        self, message_content: str, available_services: list[str]
    ) -> AnalysisSchema:
        USER_PROMPT = f"""
        AVAILABLE SERVICES:
        {available_services}

        CLIENT MESSAGE:
        {message_content}
        """
        SYSTEM_PROMPT = """
        You are an AI assistant responsible for analyzing incoming client inquiries
        for a service-based business.

        Your task is to extract structured, business-relevant information from the
        client's message so that another part of the system can later prepare a
        pricing estimate and a professional proposal.

        Follow these rules:

        1. Extract only information that is explicitly stated or strongly supported
        by the client's message.

        2. Do not invent requirements, deadlines, budgets, services, or client details.

        3. If important information is missing, list it in `missing_information`.
        Do not try to guess the missing value.

        4. `requirements` must contain only services from the
        `AVAILABLE SERVICES` list.

        5. For each requirement, `service` must use the exact service
        name from `AVAILABLE SERVICES`.

        6. `client_summary` should be a short and factual summary of what the client
        wants. Do not add information that is not present in the message.

        7. `service_type` should identify the general type of service being requested.
        Use a concise label such as "SEO", "web development", "accounting",
        "marketing", or "consulting". If the service cannot be determined,
        use "unknown".

        8. `scope` should represent the apparent size of the requested work:
        - "small" for a limited or simple request
        - "medium" for a request involving several tasks or a moderate amount
            of work
        - "large" for a broad, complex, or multi-stage engagement
        - "unknown" if there is not enough information to estimate the scope

        9. `timeline` should contain the requested deadline or timeframe if one is
        mentioned. Otherwise return null.

        10. `budget` should contain the client's stated budget if one is mentioned.
        Do not estimate or invent a budget. Otherwise return null.

        11. `missing_information` should contain information that would materially
            affect the preparation of a quote. Do not list every possible question;
            focus only on information that is genuinely relevant.

        12. `assumptions` should contain only reasonable assumptions that can be
            made from the message and that may be useful when preparing a preliminary
            quote. If no assumptions are necessary, return an empty list.

        13. Preserve important details such as quantities, platforms, technologies,
            target markets, deadlines, and constraints.

        14. Do not calculate prices. Pricing is handled separately by the
            application.

        15. Do not write a proposal or communicate directly with the client.
            Your output is an internal analysis for the pricing and proposal stages.

        16. If the client's message is vague, incomplete, or ambiguous, reflect that
            uncertainty in the analysis instead of making confident guesses.
        """
        try:
            response = await self.client.responses.parse(
                model=self.model,
                instructions=SYSTEM_PROMPT,
                input=USER_PROMPT,
                text_format=AnalysisSchema,
                max_output_tokens=1000,
            )
            return response.output_parsed
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="An error occured while fetching client message analysis.",
            ) from exc

    async def generate_proposal(
        self, *, analysis: AnalysisSchema, company_data: CompanyDataSchema, price: float
    ) -> GeneratedProposalSchema:
        USER_PROMPT = f"""
        COMPANY DATA:
        {company_data}

        CLIENT MESSAGE ANALYSIS:
        {analysis}

        CALCULATED PRICE:
        {price} {company_data.currency}
        """

        SYSTEM_PROMPT = """
        You are an AI assistant responsible for generating professional business
        proposals for a service-based company.

        Your task is to create a clear, concise, and client-ready proposal based only
        on the provided company data, client message analysis, and calculated price.

        Follow these rules:

        1. Use the CLIENT MESSAGE ANALYSIS as the primary source of information about
        the client's needs.

        2. Use COMPANY DATA to accurately represent the company's services,
        capabilities, business information, and terms.

        3. Do not invent services, deliverables, requirements, deadlines, guarantees,
        technologies, features, or business information that are not supported by
        the provided data.

        4. Include only services that appear in the client's analysis and are available
        in COMPANY DATA.

        5. Respect the `requirements` and their `details` from the analysis. The
        proposal should clearly communicate what will be delivered without adding
        unsupported scope.

        6. Use the CALCULATED PRICE exactly as provided. Do not recalculate, modify,
        discount, increase, round, or otherwise change the price.

        7. The calculated price is determined by the application and is authoritative.
        Never generate or estimate a different price.

        8. If a timeline is provided in the analysis, reflect it accurately.
        If no timeline is provided, do not invent a specific deadline or delivery
        date.

        9. If important information is missing from the analysis, do not invent it.
        Write the proposal in a way that does not make unsupported commitments.

        10. The proposal should be professional, concise, and focused on business
            value. Clearly communicate what the client will receive.

        11. Do not mention the AI, the analysis process, prompts, internal data,
            pricing engine, or any other internal implementation details.

        12. Do not address uncertainty by exposing internal reasoning. The output must
            be a polished client-facing proposal.

        13. The tone should be professional, confident, and straightforward. Avoid
            excessive marketing language, exaggerated claims, and unnecessary
            technical jargon.

        14. Preserve important client-specific details from the analysis so that the
            proposal feels tailored rather than generic.

        15. The proposal should be suitable for sending directly to the client after
            a final human review.

        16. Return only the structured proposal requested by the output schema.
        """
        try:
            response = await self.client.responses.parse(
                model=self.model,
                instructions=SYSTEM_PROMPT,
                input=USER_PROMPT,
                text_format=GeneratedProposalSchema,
                max_output_tokens=800,
            )
            return response.output_parsed
        except Exception as exc:
            print(exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occured while generating proposal.",
            ) from exc
