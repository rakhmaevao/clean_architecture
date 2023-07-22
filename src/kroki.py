import base64
import zlib
import requests


def _encode_code(code: str) -> str:
    return base64.urlsafe_b64encode(zlib.compress(code.encode("utf-8"), 9)).decode(
        "ascii"
    )


def draw_plantuml(code: str):
    return requests.get(f"https://kroki.io/plantuml/svg/{_encode_code(code)}")
