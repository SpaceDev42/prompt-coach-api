# Prompt Coach API

API mínima con **FastAPI** que evalúa la calidad de un prompt con reglas deterministas
(sin LLM) y lo estructura, más una **skill propia** (`.github/skills/prompt-coach/`) que
hace que un agente use esa API antes de responder pedidos sobre prompts.

## 1. Funcionalidad de la API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/health` | Estado y versión |
| POST | `/api/v1/prompts/analyze` | Puntaje 0-100, nivel (`weak`/`acceptable`/`good`) y sugerencias por criterio |
| POST | `/api/v1/prompts/refine` | Prompt estructurado con las secciones faltantes marcadas como `[Completa: ...]` |

Criterios evaluados: longitud, objetivo, contexto, formato, restricciones y claridad
(detalle en `.github/skills/prompt-coach/references/criteria.md`). La evaluación es
heurística (palabras clave en español e inglés).

Ejemplo:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/prompts/analyze \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Resume este artículo sobre inflación en 5 viñetas, máximo 80 palabras."}'
```

Errores: formato único `{"error": {"code", "message", "details"}}` (422 validación, 404/405 HTTP, 500 interno).
Documentación interactiva en `http://127.0.0.1:8000/docs`.

## Ejecución (Python 3.10+)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
pytest
```

Variables opcionales: `PROMPT_MIN_WORDS` (8), `PROMPT_MAX_CHARS` (4000), `PROMPT_GOOD_SCORE` (80).

## Estructura

```
app/
  main.py      # crea la app, registra router y errores
  routes.py    # endpoints (solo HTTP)
  services.py  # lógica de negocio (reglas de evaluación)
  schemas.py   # modelos Pydantic y validaciones
  config.py    # configuración por variables de entorno
  errors.py    # manejo de errores centralizado
tests/         # lógica de servicio y endpoints
.github/skills/prompt-coach/
  SKILL.md
  scripts/call_api.py
  references/criteria.md
```

No hay capa de acceso a datos: la API es sin estado y no usa base de datos.

## 2. Propósito y funcionamiento de la skill

`prompt-coach` enseña al agente a **medir antes de opinar**: cuando el usuario pide escribir
o mejorar un prompt, el agente (1) llama a `analyze`, (2) si el nivel no es `good` llama a
`refine`, (3) completa los huecos con datos del usuario (máx. 3 preguntas o supuestos
marcados) y (4) responde con un formato fijo: puntaje, qué faltaba, prompt mejorado y supuestos.
El `description` del `SKILL.md` define cuándo se activa; `scripts/` y `references/` se cargan solo si hacen falta.

## 3. Cómo la skill modifica el comportamiento del agente

Sin la skill, el agente responde con su criterio propio y formato libre. Con la skill:
- **Procedimiento:** debe consultar la API antes de juzgar el prompt.
- **Decisión:** entrega tal cual si es `good`; si no, refina.
- **Límites:** máximo 3 preguntas, sin requisitos inventados, sin fabricar resultados si la API falla.
- **Formato:** salida estandarizada.

**Cómo comprobarlo:** pedir al agente "mejora este prompt: haz una app de notas" con y sin la skill
y comparar (ver evidencia abajo).

## 4. Evidencia del uso consciente de herramientas de IA

> Completar con tu experiencia real antes de entregar (2-3 casos bastan).

| Herramienta | Qué sugirió | Qué validé / ajusté y por qué |
|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

Capturas de la comparación con/sin skill: [COMPLETAR: agregar en `docs/` o enlazar aquí].
