from app.config import get_settings
from app.services import analyze_prompt, refine_prompt

SETTINGS = get_settings()

GOOD = (
    "Actúa como profesor de historia. Explica la Revolución Francesa a "
    "estudiantes de secundaria en formato de lista, máximo 5 puntos. "
    "Debes evitar tecnicismos."
)


def _check(result, name):
    return next(c for c in result.checks if c.name == name)


def test_good_prompt_gets_full_score():
    result = analyze_prompt(GOOD, SETTINGS)
    assert result.score == 100
    assert result.level == "good"
    assert all(c.passed for c in result.checks)


def test_weak_prompt_fails_every_check():
    result = analyze_prompt("haz cosas", SETTINGS)
    assert result.score == 0
    assert result.level == "weak"
    assert result.word_count == 2


def test_vague_terms_fail_clarity_only():
    prompt = (
        "Explica algo sobre Python para principiantes en formato de lista, "
        "máximo 5 puntos, debes ser breve"
    )
    result = analyze_prompt(prompt, SETTINGS)
    assert not _check(result, "claridad").passed
    assert _check(result, "objetivo").passed
    assert _check(result, "longitud").passed


def test_refine_adds_placeholders_for_missing_sections():
    result = refine_prompt(
        "Resume el siguiente artículo sobre inflación en Latinoamérica", SETTINGS
    )
    assert result.missing == ["contexto", "formato", "restricciones"]
    assert result.needs_completion is True
    assert result.refined_prompt.startswith("Tarea: Resume")
    for section in ("Contexto:", "Formato de salida:", "Restricciones:"):
        assert section in result.refined_prompt


def test_refine_good_prompt_needs_no_completion():
    result = refine_prompt(GOOD, SETTINGS)
    assert result.missing == []
    assert result.needs_completion is False
    assert result.refined_prompt == f"Tarea: {GOOD}"
