import subprocess
import json


def get_deps(source_path: str) -> dict:
    result = subprocess.run(
        f"poetry run pydeps {source_path} --max-bacon=10  --exclude fastapi pydantic matplotlib numpy sqlalchemy requests zmq markdown --show-deps --noshow --no-output",
        shell=True,
        capture_output=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        raise RuntimeError(f"Pydeps failed {result.stderr}")

    return json.loads(result.stdout)
