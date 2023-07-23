from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
from typing import TypeAlias
from .finder import num_occurrences
CompName: TypeAlias = str


@dataclass
class Component:
    name: CompName
    path: str
    imports: list[CompName]
    imported_by: list[CompName]

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
