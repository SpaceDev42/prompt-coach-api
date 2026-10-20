"""Lógica de negocio: evaluación y refinamiento de prompts (reglas deterministas)."""
import re
from dataclasses import dataclass

from app.config import Settings
from app.schemas import AnalysisResponse, CheckResult, RefineResponse


def _rx(words: list[str]) -> re.Pattern[str]:
    return re.compile(r"\b(?:" + "|".join(words) + r")\b", re.IGNORECASE)


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    suggestion: str
    inverted: bool = False  # True: la regla pasa cuando el patrón NO aparece
    section: str | None = None  # encabezado en el prompt refinado
    placeholder: str | None = None  # texto a completar en el prompt refinado


RULES: tuple[Rule, ...] = (
    Rule(
        name="objetivo",
        pattern=_rx([
            "escribe", "escribir", "redacta", "redactar", "genera", "generar",
            "crea", "crear", "explica", "explicar", "resume", "resumir",
            "analiza", "analizar", "compara", "comparar", "traduce", "traducir",
            "lista", "enumera", "diseña", "diseñar", "implementa", "implementar",
            "corrige", "corregir", "revisa", "revisar", "write", "create",
            "generate", "explain", "summarize", "analyze", "compare",
            "translate", "list", "design", "implement", "fix", "review",
        ]),
        suggestion="Empieza con una acción clara (p. ej. redacta, resume, compara).",
    ),
    Rule(
        name="contexto",
        pattern=_rx([
            "contexto", "context", "audiencia", "audience", "público",
            "dirigido a", "para que", "so that", "background",
            "actúa como", "act as", "eres un", "eres una", "you are",
        ]),
        suggestion="Añade contexto: rol, audiencia o propósito.",
        section="Contexto",
        placeholder="[Completa: rol, audiencia y propósito]",
    ),
    Rule(
        name="formato",
        pattern=_rx([
            "formato", "format", "json", "tabla", "table", "viñetas", "bullets",
            "markdown", "párrafos", "paragraphs", "palabras", "words", "pasos",
            "steps", "csv",
        ]),
        suggestion="Indica el formato de salida esperado (lista, tabla, JSON, longitud).",
        section="Formato de salida",
        placeholder="[Completa: formato y longitud esperados]",
    ),
    Rule(
        name="restricciones",
        pattern=_rx([
            "debe", "debes", "must", "evita", "avoid", "máximo", "maximum",
            "mínimo", "minimum", "límite", "limit", "solo", "only", "sin",
            "without", "exactamente", "exactly", "at most",
        ]),
        suggestion="Define restricciones (qué evitar, límites, tono).",
        section="Restricciones",
        placeholder="[Completa: límites, tono, qué evitar]",
    ),
    Rule(
        name="claridad",
        pattern=_rx(["cosas", "algo", "stuff", "things", "etc", "whatever", "como sea"]),
        suggestion="Reemplaza términos vagos por detalles concretos.",
        inverted=True,
    ),
)


def analyze_prompt(prompt: str, settings: Settings) -> AnalysisResponse:
    """Evalúa el prompt contra la longitud mínima y las reglas heurísticas."""
    word_count = len(prompt.split())
    long_enough = word_count >= settings.min_words
    checks = [
        CheckResult(
            name="longitud",
            passed=long_enough,
            suggestion=None
            if long_enough
            else f"Usa al menos {settings.min_words} palabras para dar detalle suficiente.",
        )
    ]
    for rule in RULES:
        found = bool(rule.pattern.search(prompt))
        passed = not found if rule.inverted else found
        checks.append(
            CheckResult(
                name=rule.name,
                passed=passed,
                suggestion=None if passed else rule.suggestion,
            )
        )

    score = round(100 * sum(c.passed for c in checks) / len(checks))
    if score >= settings.good_score:
        level = "good"
    elif score >= 50:
        level = "acceptable"
    else:
        level = "weak"
    return AnalysisResponse(
        word_count=word_count, score=score, level=level, checks=checks
    )


def refine_prompt(prompt: str, settings: Settings) -> RefineResponse:
    """Construye una plantilla con el prompt original y las secciones faltantes."""
    analysis = analyze_prompt(prompt, settings)
    missing = [c.name for c in analysis.checks if not c.passed]

    lines = [f"Tarea: {prompt}"]
    for rule in RULES:
        if rule.name in missing and rule.section and rule.placeholder:
            lines.append(f"{rule.section}: {rule.placeholder}")

    return RefineResponse(
        original_prompt=prompt,
        missing=missing,
        refined_prompt="\n".join(lines),
        needs_completion=bool(missing),
    )
