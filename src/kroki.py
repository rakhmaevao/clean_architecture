import base64
import zlib
import requests
from loguru import logger


def _encode_code(code: str) -> str:
    return base64.urlsafe_b64encode(zlib.compress(code.encode("utf-8"), 9)).decode(
        "ascii"
    )


def draw_plantuml(code: str):
    response = requests.get(f"https://kroki.io/plantuml/svg/{_encode_code(code)}")
    if response.status_code != 200:
        raise RuntimeError(f"Request GET failed {response.content}")
    return response.content


def save_svg(file_path: str, svg: bytes):
    with open(file_path, "wb") as f:
        f.write(svg)