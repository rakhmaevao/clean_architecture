import base64
import zlib
import requests
from loguru import logger


def _encode_code(code: str) -> str:
    return base64.urlsafe_b64encode(zlib.compress(code.encode("utf-8"), 9)).decode(
        "ascii"
    )


def _draw_plantuml(code: str) -> bytes:
    response = requests.get(f"https://kroki.io/plantuml/svg/{_encode_code(code)}")
    if response.status_code == 400:
        logger.error(f"Request GET failed {response.status_code} for uml code:\n{code}")
    if response.status_code != 200:
        raise RuntimeError(
            f"Request GET failed {response.status_code}\n{response.content.decode('utf-8')}"
        )
    return response.content


def to_svg(code: str, file_path: str):
    svg = _draw_plantuml(code)
    with open(file_path, "wb") as f:
        f.write(svg)
