#!/usr/bin/env python3
"""Cliente mínimo (solo librería estándar) para la Prompt Coach API.

Uso: python call_api.py <analyze|refine> "<prompt>"
"""
import json
import os
import sys
import urllib.error
import urllib.request

BASE_URL = os.getenv("PROMPT_COACH_URL", "http://127.0.0.1:8000")
ACTIONS = {"analyze", "refine"}


def call(action: str, prompt: str) -> dict:
    request = urllib.request.Request(
        f"{BASE_URL}/api/v1/prompts/{action}",
        data=json.dumps({"prompt": prompt}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] not in ACTIONS:
        print('Uso: call_api.py <analyze|refine> "<prompt>"', file=sys.stderr)
        return 2
    try:
        result = call(argv[1], argv[2])
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8"), file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"No se pudo conectar con la API en {BASE_URL}: {exc.reason}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
