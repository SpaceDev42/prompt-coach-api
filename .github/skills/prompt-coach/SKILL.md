---
name: prompt-coach
description: Evalúa y mejora prompts usando la Prompt Coach API local (puntaje, criterios faltantes y plantilla estructurada). Úsala siempre que el usuario pida escribir, revisar, mejorar, validar o estructurar un prompt o una instrucción para una IA, aunque no mencione la API ni la palabra "prompt coach".
---

# Prompt Coach

Convierte pedidos vagos de "hazme un prompt" en prompts completos, usando la API
local como fuente de verdad para evaluar. No juzgues la calidad "a ojo": mide primero.

## Cuándo usar esta skill

- El usuario pide redactar, revisar o mejorar un prompt o instrucción para una IA.
- El usuario pregunta si un prompt es bueno o qué le falta.

## Flujo obligatorio

1. **Verifica la API.** Debe estar corriendo (`uvicorn app.main:app`). URL por defecto:
   `http://127.0.0.1:8000` (configurable con `PROMPT_COACH_URL`).
2. **Analiza** el prompt del usuario:
   `python .github/skills/prompt-coach/scripts/call_api.py analyze "<prompt>"`
3. **Decide según el resultado:**
   - `level` = `good` → entrega el prompt tal cual, con una línea de confirmación.
   - `level` = `acceptable` o `weak` → continúa al paso 4.
4. **Refina:**
   `python .github/skills/prompt-coach/scripts/call_api.py refine "<prompt>"`
   Completa cada `[Completa: ...]` del campo `refined_prompt`:
   - Si el usuario ya dio el dato, úsalo.
   - Si no lo dio, escribe un valor razonable **dentro del prompt con la etiqueta `[Supuesto: ...]`**.
   - Haz como máximo **3 preguntas breves**, solo si el pedido es ambiguo en lo esencial.
   Agrega al final del prompt una sección **Criterios de aceptación** (2-3 puntos)
   derivados únicamente del pedido original del usuario.
5. **Responde** con este formato exacto:
   - **Puntaje inicial:** `score` y `level`.
   - **Qué faltaba:** lista de criterios fallidos (campo `missing`).
   - **Prompt mejorado:** en un bloque de código.
   - **Supuestos:** lista de todo lo marcado como `[Supuesto: ...]`, o "ninguno".

## Reglas

- Nunca inventes resultados de la API. Si no responde, dilo y detente; como alternativa
  manual consulta `references/criteria.md`, indicando que la evaluación no es verificada.
- Todo lo que el usuario no dijo debe ir etiquetado como `[Supuesto: ...]` dentro del prompt;
  nunca lo presentes como requisito firme ni agregues funciones nuevas sin etiquetar.
- Mantén el idioma del prompt original.

## Recursos

- `scripts/call_api.py`: cliente mínimo (solo librería estándar) para `analyze` y `refine`.
- `references/criteria.md`: qué evalúa cada criterio y cómo corregirlo. Léelo solo si
  necesitas explicar un criterio o si la API no está disponible.
