import copy
from dataclasses import dataclass
import importlib
import os
import inspect
import sys
from pathlib import Path
from loguru import logger
import importlib.util
from typing import TypeAlias

ClassName: TypeAlias = str
SrcM: TypeAlias = str
UsingM: TypeAlias = str


@dataclass
class ClassSearchingResult:
    class_name: str
    source_module_path: Path
    using_modules_paths: set[Path]


def get_all_classes(project_path: Path) -> list[ClassSearchingResult]:
    classes: dict[ClassName, ClassSearchingResult] = dict()
    origin_sys_path = copy.deepcopy(sys.path)
    origin_modules = copy.copy(sys.modules)

    sys.path.remove(os.getcwd())

    [
        sys.modules.pop(m)
        for m in sys.modules.copy()
        if (m not in sys.stdlib_module_names) and (m != "os.path")
    ]

    other_prj_modules = set()
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                sys.path.append(root)
                module_name = os.path.splitext(file)[0]
                module_path = os.path.join(root, file)
                module = importlib.import_module(module_name)
                other_prj_modules.add(module_name)

                # Ищем классы в модуле
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        source_module_path = Path(inspect.getfile(obj))
                        if source_module_path.is_relative_to(
                            "/home/rahmaevao/Projects/clean_architecture/.venv"
                        ):
                            continue
                        if name not in classes:
                            classes[name] = ClassSearchingResult(
                                class_name=name,
                                source_module_path=source_module_path,
                                using_modules_paths=set([Path(module_path)]),
                            )
                        else:
                            classes[name].using_modules_paths.add(Path(module_path))

    sys.path = origin_sys_path
    sys.modules = origin_modules
    return [c for c in classes.values()]
