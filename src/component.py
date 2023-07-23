from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
from typing import TypeAlias

from loguru import logger
from .finder import num_occurrences

CompName: TypeAlias = str


@dataclass
class Component:
    name: CompName
    path: str
    imports: list[CompName]
    imported_by: list[CompName]

    def __post_init__(self):
        # Удаление таких импортов, которые определяются таковыми,
        # потому, что являются путем к конкретному импорту.
        # То есть при импорте src.file_api.exceptions будет также
        # src.file_api. А он лишний по сути.
        # Такова особенность pydeps
        for imp in self.imports:
            parent = ".".join(imp.split(".")[:-1])
            for imp_other in self.imports:
                if imp_other == parent:
                    self.imports.remove(imp_other)
                    break

        logger.info(f"Импорты для {self.name}: {self.imports}")

    @classmethod
    def from_dict(cls, data: dict) -> Component:
        return cls(
            name=data["name"],
            path=data["path"],
            imports=data.get("imports", []),
            imported_by=data.get("imported_by", []),
        )

    @cached_property
    def instability(self) -> float:
        try:
            return len(self.imports) / (len(self.imported_by) + len(self.imports))
        except ZeroDivisionError:
            return 0.0

    @cached_property
    def abstractness(self) -> float:
        num_classes = num_occurrences(self.path, "class", ["    class Config:"])
        num_abs_classes = num_occurrences(self.path, "ABC")
        try:
            return num_abs_classes / num_classes
        except ZeroDivisionError:
            return 0.0

    @cached_property
    def distance(self) -> float:
        return abs(self.instability + self.abstractness - 1)

    def __str__(self) -> str:
        return f"{self.name} \\n I = {self.instability} \\n A = {self.abstractness}"
