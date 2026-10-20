"""Punto de entrada: crea la app e incluye routers y manejadores de error."""
from fastapi import FastAPI

from app.config import get_settings
from app.errors import register_error_handlers
from app.routes import router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="Evalúa y estructura prompts con reglas deterministas (sin LLM).",
    )
    register_error_handlers(app)
    app.include_router(router)
    return app


app = create_app()
