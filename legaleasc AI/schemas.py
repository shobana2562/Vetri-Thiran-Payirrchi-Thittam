from typing import Literal

from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=6000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=12000
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=1000
    )

    additional_instructions: str = Field(
        default="",
        max_length=6000
    )

    @field_validator(
        "document_type",
        "parties",
        "terms",
        "dates",
        "additional_instructions"
    )
    @classmethod
    def clean_values(cls, value: str) -> str:

        return value.strip()


class GenerateResponse(BaseModel):

    document_type: str

    content: str

    model: str


class ExportRequest(BaseModel):

    document_type: str = Field(
        default="Legal Document",
        min_length=1,
        max_length=120
    )

    content: str = Field(
        ...,
        min_length=1,
        max_length=100000
    )

    format: Literal[
        "txt",
        "docx",
        "pdf"
    ]


class HealthResponse(BaseModel):

    status: str

    gemini_configured: bool

    model: str