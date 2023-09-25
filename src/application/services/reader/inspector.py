import copy
from dataclasses import dataclass
from importlib import import_module
import os
import inspect
import sys
from pathlib import Path
from loguru import logger
from typing import TypeAlias

ClassName: TypeAlias = str


@dataclass
class ClassSearchingResult:
    class_name: ClassName
    src_module_path: Path
    src_module_name: str
    using_modules_paths: set[Path]


class ClassesSearchingResultVault:
    def __init__(self):
        self.classes: dict[ClassName, ClassSearchingResult] = dict()

    def add(
        self,
        class_name: ClassName,
        src_module_path: Path,
        using_path: Path,
        src_module_name,
    ):
        if class_name not in self.classes:
            self.classes[class_name] = ClassSearchingResult(
                class_name=class_name,
                src_module_path=src_module_path,
                src_module_name=src_module_name,
                using_modules_paths=set([using_path]),
            )
        else:
            self.classes[class_name].using_modules_paths.add(using_path)

    def values(self) -> list[ClassSearchingResult]:
        return list(self.classes.values())


def get_all_classes(project_path: Path) -> list[ClassSearchingResult]:
    origin_sys_path = copy.deepcopy(sys.path)
    sys.path.remove(os.getcwd())

    origin_modules = copy.copy(sys.modules)
    [
        sys.modules.pop(m)
        for m in sys.modules.copy()
        if (m not in sys.stdlib_module_names) and (m != "os.path")
    ]

    classes = ClassesSearchingResultVault()
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                sys.path.append(root)
                module_name = os.path.splitext(file)[0]

                for name, obj in inspect.getmembers(import_module(module_name)):
                    if inspect.isclass(obj):
                        classes.add(
                            class_name=name,
                            src_module_name=inspect.getmodule(obj).__name__,
                            src_module_path=Path(inspect.getfile(obj)),
                            using_path=Path(os.path.join(root, file)),
                        )

    sys.path = origin_sys_path
    sys.modules = origin_modules
    return [c for c in classes.values()]
