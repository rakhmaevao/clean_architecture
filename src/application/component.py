from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


ModuleName: TypeAlias = str
EntityName: TypeAlias = str


@dataclass
class PythonModule:
    name: str
    path: str
    imported_entities: dict[ModuleName, set[EntityName]]
    exported_entities: set[EntityName]


@dataclass
class Component:
    modules: dict[ModuleName, PythonModule]
    path: str
