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


class AnalysisSchema(BaseModel):
    service_type: str = Field(description="Type of service the client is requesting.")

    client_summary: str = Field(description="Short summary of what the client wants.")

    requirements: list[str] = Field(
        description="Specific requirements explicitly mentioned by the client."
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
