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
SrcM: TypeAlias = str
UsingM: TypeAlias = str


@dataclass
class ClassSearchingResult:
    class_name: str
    source_module_path: Path
    using_modules_paths: set[Path]


class ClassesSearchingResultVault:
    def __init__(self):
        self.classes: dict[ClassName, ClassSearchingResult] = dict()

    def add(self, class_name: str, src_path: Path, using_path: Path):
        if class_name not in self.classes:
            self.classes[class_name] = ClassSearchingResult(
                class_name=class_name,
                source_module_path=src_path,
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
                        src_path = Path(inspect.getfile(obj))
                        if src_path.is_relative_to(
                            "/home/rahmaevao/Projects/clean_architecture/.venv"
                        ):
                            continue

                        module_path = os.path.join(root, file)
                        classes.add(name, Path(src_path), Path(module_path))

    sys.path = origin_sys_path
    sys.modules = origin_modules
    return [c for c in classes.values()]
