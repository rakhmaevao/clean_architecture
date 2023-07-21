import subprocess
import json

result = subprocess.run(
    "pydeps main.py --max-bacon=10  --exclude fastapi pydantic matplotlib numpy sqlalchemy requests zmq markdown --show-deps --noshow",
    shell=True,
    capture_output=True,
    encoding='utf-8'
)

if result.returncode != 0:
    raise RuntimeError(f"Pydeps failed {result.stderr}")

raw_pydeps = json.loads(result.stdout)

