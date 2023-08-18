from __future__ import annotations
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias
from dataclasses import asdict

from loguru import logger

ModuleName: TypeAlias = str
EntityName: TypeAlias = str


@dataclass
class PythonModule:
    name: str
    path: str
    imported_entities: dict[ModuleName, set[EntityName]]
    exported_entities: set[EntityName]

    def to_dict(self):
        return asdict(self)

    @property
    def instability(self):
        fan_out = len(self.exported_entities)
        fan_in = sum(
            [len(self.imported_entities.get(m)) for m in self.imported_entities]
        )
        try:
            return fan_out / (fan_in + fan_out)
        except ZeroDivisionError:
            return 0.0

    @property
    def abstractness(self):
        num_classes = self._num_occurrences(self.path, "class", ["    class Config:"])
        num_abs_classes = self._num_occurrences(self.path, "ABC") - 1
        if num_abs_classes < 0:
            num_abs_classes = 0
        try:
            return num_abs_classes / num_classes
        except ZeroDivisionError:
            return 0.0

    @staticmethod
    def _num_occurrences(path: str, string: str, exclude: list[str] = []) -> int:
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


@dataclass
class PythonProject:
    modules: dict[ModuleName, PythonModule]
    path: Path
