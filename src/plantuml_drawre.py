import subprocess
import json

plantuml_source = """
title Authentication Sequence

Alice->Bob: Authentication Request
note right of Bob: Bob thinks about it
Bob->Alice: Authentication Response
"""



result = subprocess.run(
    "python3 -m plantuml simple.txt",
    shell=True,
    capture_output=True,
    encoding='utf-8'
)

if result.returncode != 0:
    raise RuntimeError(f"Pydeps failed {result.stderr}")

raw_pydeps = json.loads(result.stdout)

