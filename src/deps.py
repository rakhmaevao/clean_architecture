import subprocess
import json
from loguru import logger
import tomli
from functools import lru_cache
import sys


def get_deps(srv_path: str) -> dict:
    used_libs = read_used_libraries(srv_path)
    result = subprocess.run(
        f"poetry run pydeps {srv_path}/main.py --max-bacon=1000  --exclude {' '.join(used_libs)} --show-deps --noshow --no-output",
        shell=True,
        capture_output=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        raise RuntimeError(f"Pydeps failed {result.stderr}")

    return json.loads(result.stdout)
