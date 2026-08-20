from fastapi import HTTPException, status
from openai import AsyncOpenAI

from app.ai.base import AIBase
from app.config import settings
from app.schemas import AnalysisSchema


class AIService(AIBase):
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL

    async def generate_analysis(self, message_content: str, services: list[str]) -> AnalysisSchema:
        USER_PROMPT = f"""
        AVAILABLE SERVICES:
        {services}

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
