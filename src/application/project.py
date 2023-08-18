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


@dataclass
class PythonProject:
    modules: dict[ModuleName, PythonModule]
    path: Path
