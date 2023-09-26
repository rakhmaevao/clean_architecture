import copy
from dataclasses import dataclass
from enum import Enum
from importlib import import_module
import os
import inspect
import sys
from pathlib import Path
from loguru import logger
from typing import TypeAlias
from src.application.project import EntityKind

EntityName: TypeAlias = str


@dataclass
class EntitySearchingResult:
    name: EntityName
    kind: EntityKind
    src_module_path: Path
    src_module_name: str
    using_modules_paths: set[Path]


class EntitiesSearchingResultVault:
    def __init__(self):
        self.entities: dict[EntityName, EntitySearchingResult] = dict()

    def add(
        self,
        entity_name: EntityName,
        entity_type: EntityKind,
        src_module_path: Path | None,
        using_path: Path,
        src_module_name: str | None,
    ):
        if entity_name not in self.entities:
            self.entities[entity_name] = EntitySearchingResult(
                name=entity_name,
                kind=entity_type,
                src_module_path=src_module_path,
                src_module_name=src_module_name,
                using_modules_paths=set([using_path]),
            )
        else:
            self.entities[entity_name].using_modules_paths.add(using_path)

    def values(self) -> list[EntitySearchingResult]:
        return list(self.entities.values())


def get_all_entities(project_path: Path) -> list[EntitySearchingResult]:
    origin_sys_path = copy.deepcopy(sys.path)
    sys.path.remove(os.getcwd())

    origin_modules = copy.copy(sys.modules)
    [
        sys.modules.pop(m)
        for m in sys.modules.copy()
        if (m not in sys.stdlib_module_names) and (m != "os.path")
    ]

    entities = EntitiesSearchingResultVault()
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                sys.path.append(root)
                module_name = os.path.splitext(file)[0]

                for name, obj in inspect.getmembers(import_module(module_name)):
                    if inspect.isclass(obj):
                        entities.add(
                            entity_name=name,
                            entity_type=EntityKind.CLASS,
                            src_module_name=inspect.getmodule(obj).__name__,
                            src_module_path=Path(inspect.getfile(obj)),
                            using_path=Path(os.path.join(root, file)),
                        )
                    elif inspect.isfunction(obj):
                        entities.add(
                            entity_name=name,
                            entity_type=EntityKind.FUNCTION,
                            src_module_name=inspect.getmodule(obj).__name__,
                            src_module_path=Path(inspect.getfile(obj)),
                            using_path=Path(os.path.join(root, file)),
                        )
                    elif not name.startswith("__") and not inspect.ismodule(obj):
                        entities.add(
                            entity_name=name,
                            entity_type=EntityKind.VARIABLE,
                            src_module_name=None,
                            src_module_path=None,
                            using_path=Path(os.path.join(root, file)),
                        )
    logger.info([e for e in entities.values()])
    sys.path = origin_sys_path
    sys.modules = origin_modules
    return [c for c in entities.values()]
