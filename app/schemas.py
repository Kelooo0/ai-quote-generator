from pydantic import BaseModel, Field, field_validator


class ClientMessage(BaseModel):
    content: str = Field(min_length=50, max_length=5000)

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Client message can not be empty or just whitespaces")
        return v


class Requirement(BaseModel):
    service: str = Field(
        description="The exact name of the requested service from the available services list."
    )
    details: list[str] = Field(
        description="Important client-provided details relevant to this service, "
        "such as quantities, platforms, technologies, target markets, deadlines, or constraints."
    )


class AnalysisSchema(BaseModel):
    service_type: str = Field(description="Type of service the client is requesting.")

    client_summary: str = Field(description="Short summary of what the client wants.")

    requirements: list[Requirement] = Field(
        description=(
            "Services explicitly requested by the client, with relevant details "
            "provided for each service."
        )
    )

    scope: str = Field(
        description="Estimated scope of the requested work: small, medium, or large."
    )

    timeline: str | None = Field(
        default=None, description="Requested deadline or timeline, if mentioned."
    )

    budget: str | None = Field(default=None, description="Client's stated budget, if mentioned.")

    missing_information: list[str] = Field(
        description="Important information missing from the request that may affect the quote."
    )

    assumptions: list[str] = Field(
        description="Reasonable assumptions needed to prepare a preliminary quote."
    )


class CompanyDataSchema(BaseModel):
    company_name: str
    description: str
    services: list[str]
    value_proposition: str
    contact_email: str
    website: str
    currency: str


class PricingSchema(BaseModel):
    prices: dict[str, float]


class ProposalBase(BaseModel):
    title: str = Field(
        description="A concise, professional title for the proposal"
        " that reflects the requested service."
    )

    introduction: str = Field(
        description="A short, personalized introduction that acknowledges the client's"
        " needs and briefly explains how the company can address them."
    )

    scope: list[str] = Field(
        description="A list of specific services, deliverables, or tasks included in"
        " the proposed scope of work. Include only items supported by the"
        " client analysis and available company services."
    )

    timeline: str | None = Field(
        description="The expected project timeline or deadline"
        " based on the client's requested timeframe. Return null if no timeline is provided or"
        " can be determined from the available information."
    )


class GeneratedProposalSchema(ProposalBase):
    pass


class FinalProposalSchema(ProposalBase):
    price: float
    currency: str
