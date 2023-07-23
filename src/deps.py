import subprocess
import json
import tomli


def get_deps(srv_path: str) -> dict:
    used_libs = _read_used_libraries(srv_path)
    result = subprocess.run(
        f"poetry run pydeps {srv_path}/main.py --max-bacon=0  --exclude {' '.join(used_libs)} --show-deps --noshow --no-output",
        shell=True,
        capture_output=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        raise RuntimeError(f"Pydeps failed {result.stderr}")

    return json.loads(result.stdout)


def _read_used_libraries(srv_path: str) -> list[str]:
    with open(f"{srv_path}/pyproject.toml", "rb") as f:
        pyproject_toml = tomli.load(f)
    return pyproject_toml["tool"]["poetry"]["dependencies"].keys()
