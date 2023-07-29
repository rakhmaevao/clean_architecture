from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
from typing import TypeAlias
from pathlib import Path
from loguru import logger
from .finder import num_occurrences
from .imports import get_imported_entities_by_modules
from .deps import is_lib

CompName: TypeAlias = str


@dataclass
class Component:
    name: CompName
    path: str
    imports: list[CompName]
    imported_by: list[CompName]
    service_path: str

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

        if self.path is None:
            self.path = f"{self.service_path}/main.py"

        self.__entities = get_imported_entities_by_modules(self.path)
        business_modules = []
        for module in self.__entities.get_modules():
            if not is_lib(module, self.service_path):
                business_modules.append(module)
        self.__imported_entities = set()
        for i_e in business_modules:
            self.__imported_entities.update(self.__entities.get(i_e))
        self.__fan_out = sum([len(self.__entities.get(e)) for e in business_modules])
        self.__fan_in = 0
        self.__external_used_entities = []
        logger.info(f"Импорты для {self.name}: {self.imports} {self.__fan_out}")

    def num_imported_entities_from_module(self, module_name) -> int:
        return len(self.__entities.get(module_name))

    def imported_entities_from_module(self, module_name) -> list[str]:
        return self.__entities.get(module_name)

    def set_fan_in(self, fan_in: int) -> None:
        self.__fan_in = fan_in

    def set_external_used_entities(self, external_used_entities: list[str]) -> None:
        self.__external_used_entities = external_used_entities

    @classmethod
    def from_dict(cls, data: dict, service_path: str) -> Component:
        return cls(
            name=data["name"],
            path=data["path"],
            imports=data.get("imports", []),
            imported_by=data.get("imported_by", []),
            service_path=service_path,
        )

    @cached_property
    def instability(self) -> float:
        logger.info(f"INNNNNNNN {self.name} {self.__fan_out} {self.__fan_in}")
        try:
            return self.__fan_out / (self.__fan_in + self.__fan_out)
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
        if self.path is None:
            path = self.name
        else:
            path = Path(self.path).relative_to(Path(self.service_path))
        return (
            f"{self.name} \\n"
            f"Path: {path} \\n"
            f"I = {self.instability} \\n"
            f"A = {self.abstractness} \\n"
            f"++++++++ \\n"
            f"External used entities: {len(self.__external_used_entities)} \\n"
            f"Imported entities: {len(self.__imported_entities)} pieces\\n"
            f"Imported entities: {self.__imported_entities} \\n"
        )
