"""Configuración de la aplicación (variables de entorno con valores por defecto)."""
import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    app_name: str
    version: str
    min_words: int  # mínimo de palabras para considerar un prompt "suficiente"
    max_chars: int  # tamaño máximo aceptado por la API
    good_score: int  # puntaje desde el cual un prompt se considera "good"


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name="Prompt Coach API",
        version="1.0.0",
        min_words=int(os.getenv("PROMPT_MIN_WORDS", "8")),
        max_chars=int(os.getenv("PROMPT_MAX_CHARS", "4000")),
        good_score=int(os.getenv("PROMPT_GOOD_SCORE", "80")),
    )
