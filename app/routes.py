"""Endpoints HTTP. Solo traducen request/response; la lógica vive en services."""
from typing import Annotated

from fastapi import APIRouter, Depends

from app import services
from app.config import Settings, get_settings
from app.schemas import AnalysisResponse, HealthResponse, PromptRequest, RefineResponse

router = APIRouter(prefix="/api/v1")

SettingsDep = Annotated[Settings, Depends(get_settings)]


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health(settings: SettingsDep) -> HealthResponse:
    """Verifica que la API está disponible."""
    return HealthResponse(status="ok", version=settings.version)


@router.post("/prompts/analyze", response_model=AnalysisResponse, tags=["prompts"])
def analyze(body: PromptRequest, settings: SettingsDep) -> AnalysisResponse:
    """Evalúa la calidad de un prompt: puntaje, nivel y sugerencias por criterio."""
    return services.analyze_prompt(body.prompt, settings)


@router.post("/prompts/refine", response_model=RefineResponse, tags=["prompts"])
def refine(body: PromptRequest, settings: SettingsDep) -> RefineResponse:
    """Devuelve el prompt estructurado con las secciones que faltan por completar."""
    return services.refine_prompt(body.prompt, settings)
