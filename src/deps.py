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


@lru_cache
def read_used_libraries(srv_path: str) -> list[str]:
    with open(f"{srv_path}/poetry.lock", "rb") as f:
        poetry_lock = tomli.load(f)["package"]
    pkgs = [pkg["name"].replace("-", "_") for pkg in poetry_lock]
    libs = pkgs + list(sys.stdlib_module_names)
    return libs


def is_lib(module_name, srv_path) -> bool:
    libs = read_used_libraries(srv_path)
    if module_name.split(".")[0] in libs:
        return True
    return False
