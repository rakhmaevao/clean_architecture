from __future__ import annotations
from enum import Enum
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
            [
                len(self.imported_entities[module_name])
                for module_name in self.imported_entities.keys()
            ]
        )
        try:
            return fan_out / (fan_in + fan_out)
        except ZeroDivisionError:
            return 0.0

    @property
    def class_instability(self):
        fan_out = len(
            [
                c
                for c in self.exported_entities
                if c.kind == EntityKind.CLASS or c.kind == EntityKind.ABSTRACT
            ]
        )
        fan_in = sum(
            [
                len(
                    [
                        class_entity
                        for class_entity in self.imported_entities[module_name]
                        if class_entity.kind == EntityKind.CLASS
                        or class_entity.kind == EntityKind.ABSTRACT
                    ]
                )
                for module_name in self.imported_entities.keys()
            ]
        )
        try:
            return fan_out / (fan_in + fan_out)
        except ZeroDivisionError:
            return 0.0

    @property
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
        return abs(self.class_instability + self.abstractness - 1)


@dataclass
class PythonProject:
    modules: dict[ModuleName, PythonModule]
    path: Path
