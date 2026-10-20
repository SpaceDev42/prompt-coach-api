"""Esquemas de entrada y salida (validación con Pydantic)."""
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.config import get_settings

_MAX_CHARS = get_settings().max_chars


class PromptRequest(BaseModel):
    prompt: str = Field(
        ...,
        max_length=_MAX_CHARS,
        description="Texto del prompt a evaluar.",
        examples=["Resume este artículo sobre inflación en 5 viñetas."],
    )

    @field_validator("prompt")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El prompt no puede estar vacío.")
        return value


class CheckResult(BaseModel):
    name: str
    passed: bool
    suggestion: str | None = None


class AnalysisResponse(BaseModel):
    word_count: int
    score: int = Field(ge=0, le=100)
    level: Literal["weak", "acceptable", "good"]
    checks: list[CheckResult]


class RefineResponse(BaseModel):
    original_prompt: str
    missing: list[str]
    refined_prompt: str
    needs_completion: bool


class HealthResponse(BaseModel):
    status: Literal["ok"]
    version: str
