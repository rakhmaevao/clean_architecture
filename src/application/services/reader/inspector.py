import inspect
import json
import os
from pathlib import Path
import sys
from importlib import import_module
from typing import TypeAlias, NamedTuple
from contextlib import suppress

_EntityName: TypeAlias = str


class _EntitySearchingResult(NamedTuple):
    name: _EntityName
    kind: str
    src_module_path: str | None
    using_modules_paths: list[str]


class _EntitiesSearchingResultVault:
    def __init__(self):
        self.entities: dict[_EntityName, _EntitySearchingResult] = {}

    def add(
        self,
        entity_name: _EntityName,
        entity_type: str,
        src_module_path: str | None,
        using_path: str,
    ):
        if entity_name not in self.entities:
            self.entities[entity_name] = _EntitySearchingResult(
                name=entity_name,
                kind=entity_type,
                src_module_path=src_module_path,
                using_modules_paths=[using_path],
            )
        else:
            self.entities[entity_name].using_modules_paths.append(using_path)

    def values(self) -> list[_EntitySearchingResult]:
        return list(self.entities.values())


IGNORE_PATHS = (".venv", "tests")

if __name__ == "__main__":
    entities = _EntitiesSearchingResultVault()
    for root, _, files in os.walk(os.getcwd()):
        if any(
            Path(root).is_relative_to(Path.cwd() / Path(i_path))
            for i_path in IGNORE_PATHS
        ):
            continue
        for file in files:
            if file.endswith(".py"):
                sys.path.append(root)
                module_name = os.path.splitext(file)[0]
                if module_name == "__init__":
                    module_name = os.path.basename(root)
                try:
                    for name, obj in inspect.getmembers(import_module(module_name)):
                        if inspect.ismodule(obj):
                            # TODO: Для случая form pkg import module
                            pass
                        if inspect.isclass(obj):
                            with suppress(TypeError):
                                entities.add(
                                    entity_name=name,
                                    entity_type="class",
                                    src_module_path=inspect.getfile(obj),
                                    using_path=os.path.join(root, file),
                                )
                        elif inspect.isfunction(obj):
                            entities.add(
                                entity_name=name,
                                entity_type="function",
                                src_module_path=inspect.getfile(obj),
                                using_path=os.path.join(root, file),
                            )
                        elif not name.startswith("__") and not inspect.ismodule(obj):
                            entities.add(
                                entity_name=name,
                                entity_type="variable",
                                src_module_path=None,
                                using_path=os.path.join(root, file),
                            )
                except ImportError as error:
                    print(
                        f"Error importing module {module_name}.\n{error}",
                        file=sys.stderr,
                    )
    print(json.dumps(entities.entities))
