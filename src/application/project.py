from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias
from dataclasses import asdict

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
        pass


@dataclass
class PythonProject:
    modules: dict[ModuleName, PythonModule]
    path: Path
