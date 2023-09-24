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
    source_module_path: str
    using_modules_paths: set[str]


def get_all_classes(project_path: Path) -> list[ClassSearchingResult]:
    classes: dict[ClassName, ClassSearchingResult] = dict()

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                sys.path.insert(0, root)
                module_name = os.path.splitext(file)[0]
                module_path = os.path.join(root, file)
                logger.info(f"FFFFFF{module_path}")
                print(sys.path)
                # module = importlib.import_module(module_path)
                module = __import__(module_name)

                # Ищем классы в модуле
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj):
                        if name not in classes:
                            classes[name] = ClassSearchingResult(
                                class_name=name,
                                source_module_path=inspect.getfile(obj),
                                using_modules_paths=set([module_path]),
                            )
                        else:
                            classes[name].using_modules_paths.add(module_path)
                # sys.path.remove(root)
                # del sys.modules[module_name]
    return [c for c in classes.values()]


if __name__ == "__main__":
    # Пример использования скрипта
    project_path = "/home/rahmaevao/Projects/clean_architecture/tests/mock_component"
    result = get_all_classes(project_path)
    for ss in result:
        print(f"{ss=}")


[
    "/home/rahmaevao/Projects/clean_architecture",
    "/usr/lib/python310.zip",
    "/usr/lib/python3.10",
    "/usr/lib/python3.10/lib-dynload",
    "/home/rahmaevao/Projects/clean_architecture/.venv/lib/python3.10/site-packages",
    "/home/rahmaevao/Projects/clean_architecture/tests/mock_component",
    "/home/rahmaevao/Projects/clean_architecture/tests/mock_component",
    "/home/rahmaevao/Projects/clean_architecture/tests/mock_component/src",
]
