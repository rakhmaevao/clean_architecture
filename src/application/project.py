from __future__ import annotations
from enum import Enum
from functools import cached_property
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, TypeAlias
from dataclasses import asdict

ModuleName: TypeAlias = str
EntityName: TypeAlias = str


class EntityKind(Enum):
    CLASS = "class"
    ABSTRACT = "abstract"
    FUNCTION = "function"
    VARIABLE = "variable"


class Entity(NamedTuple):
    name: EntityName
    kind: EntityKind


@dataclass
class PythonModule:
    name: str
    path: Path
    imported_entities: dict[ModuleName, set[Entity]]
    exported_entities: set[Entity]

    def to_dict(self):
        return asdict(self)

    @property
    def full_instability(self):
        """Неустойчивость модуля по всем сущностям в нем."""
        fan_out = len(self.exported_entities)
        fan_in = sum(
            [len(self.imported_entities.get(m)) for m in self.imported_entities]
        )
        try:
            return fan_out / (fan_in + fan_out)
        except ZeroDivisionError:
            return 0.0

    @cached_property
    def abstractness(self):
        num_classes = len(
            [c for c in self.exported_entities if c.kind == EntityKind.CLASS]
        )
        num_abs_classes = len(
            [c for c in self.exported_entities if c.kind == EntityKind.ABSTRACT]
        )
        try:
            return num_abs_classes / num_classes
        except ZeroDivisionError:
            return 0.0

    @property
    def distance(self) -> float:
        return abs(self.full_instability + self.abstractness - 1)

    @staticmethod
    def _num_occurrences(path: Path, string: str, exclude: list[str] = []) -> int:
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
