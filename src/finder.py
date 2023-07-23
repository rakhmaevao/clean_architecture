import subprocess


def num_occurrences(path: str, string: str, exclude: list[str] = []) -> int:
    result = subprocess.run(
        f"grep {string} {path}",
        shell=True,
        capture_output=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        return 0

    num = 0
    for line in result.stdout.splitlines():
        num += 1
        for ex in exclude:
            if ex == line:
                num -= 1
                break

    return num