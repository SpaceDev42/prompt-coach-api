# Criterios de evaluación

El puntaje es `100 × criterios aprobados / 6`. Niveles: `good` ≥ 80, `acceptable` ≥ 50, `weak` < 50
(el umbral de `good` es configurable con `PROMPT_GOOD_SCORE`).

| Criterio | Aprueba si... | Cómo corregirlo |
|---|---|---|
| `longitud` | Tiene al menos 8 palabras (`PROMPT_MIN_WORDS`) | Añade detalle sobre qué se espera |
| `objetivo` | Contiene un verbo de acción (redacta, resume, compara, write, explain...) | Empieza con una acción clara |
| `contexto` | Menciona rol, audiencia o propósito (actúa como, para que, audiencia...) | Indica quién lo usará y para qué |
| `formato` | Define formato de salida (lista, tabla, JSON, nº de palabras, pasos...) | Especifica estructura y longitud |
| `restricciones` | Define límites o prohibiciones (debes, evita, máximo, solo, sin...) | Indica qué evitar, tono y límites |
| `claridad` | **No** contiene términos vagos (cosas, algo, stuff, etc...) | Sustituye por detalles concretos |

## Limitaciones

La evaluación es heurística (palabras clave en español e inglés). Un prompt bueno
redactado con otras palabras puede puntuar bajo; úsala como guía, no como veredicto.
