from loguru import logger
from src.application.project import PythonProject, PythonModule, ModuleName, Entity
import tomli
from functools import lru_cache
import sys
from pathlib import Path
from src.application.services.reader.inspector import (
    EntitySearchingResult,
    get_all_entities,
)


class ProjectReader:
    def __init__(self, root_path: Path) -> None:
        self.__root_path = root_path
        self.__ex_libs = self.__read_used_libraries()
        self.__ex_libs |= self.__read_ignore_imports()
        self.__all_modules: dict[ModuleName, PythonModule] = {}

    def read_project(self) -> PythonProject:
        return PythonProject(
            modules=self.__read_py_modules(),
            path=self.__root_path,
        )

    def __add_module(self, path: Path, using_entity: EntitySearchingResult):
        module_name = self._generate_module_name(path)
        src_module_name = self._generate_module_name(using_entity.src_module_path)
        if module_name == src_module_name:
            if module_name not in self.__all_modules:
                self.__all_modules[module_name] = PythonModule(
                    name=module_name,
                    path=path.relative_to(self.__root_path),
                    imported_entities=dict(),
                    exported_entities=set(),
                )
        elif module_name not in self.__all_modules:
            self.__all_modules[module_name] = PythonModule(
                name=module_name,
                path=path.relative_to(self.__root_path),
                imported_entities={
                    src_module_name: set(
                        [Entity(name=using_entity.name, kind=using_entity.kind)]
                    )
                },
                exported_entities=set(),
            )
        else:
            if src_module_name in self.__all_modules[module_name].imported_entities:
                self.__all_modules[module_name].imported_entities[src_module_name].add(
                    Entity(name=using_entity.name, kind=using_entity.kind)
                )
            else:
                self.__all_modules[module_name].imported_entities[
                    src_module_name
                ] = set([Entity(name=using_entity.name, kind=using_entity.kind)])

    def __read_py_modules(self) -> dict[ModuleName, PythonModule]:
        all_entities = get_all_entities(self.__root_path)
        for path in self._get_python_files():
            for using_entity in all_entities:
                if self.__is_ex_lib(using_entity):
                    continue
                for using_module_path in using_entity.using_modules_paths:
                    if using_module_path == path:
                        self.__add_module(path, using_entity)
        self.__set_exported_relationships()
        return self.__all_modules

    def __set_exported_relationships(self):
        for module in self.__all_modules.values():
            for other_module in self.__all_modules.values():
                if module.name in other_module.imported_entities.keys():
                    module.exported_entities |= other_module.imported_entities[
                        module.name
                    ]

    def _generate_module_name(self, path: Path) -> str:
        m_name = (
            path.relative_to(self.__root_path)
            .with_suffix("")
            .as_posix()
            .replace("/", ".")
        )
        if m_name.split(".")[-1] == "__init__":
            m_name = ".".join(m_name.split(".")[:-1])
        return m_name

    def _get_python_files(self) -> set[Path]:
        return {path for path in (self.__root_path / "src").rglob("*.py")} | {
            self.__root_path / "main.py"
        }

    def __is_ex_lib(self, entity: EntitySearchingResult) -> bool:
        try:
            module_name = self._generate_module_name(entity.src_module_path)
            if module_name.startswith("."):
                return True
            return module_name.split(".")[0] in self.__ex_libs
        except Exception:
            return True

    @lru_cache
    def __read_used_libraries(self) -> set[str]:
        with open(self.__root_path / "poetry.lock", "rb") as f:
            poetry_lock = tomli.load(f)["package"]
        pkgs = {pkg["name"].replace("-", "_") for pkg in poetry_lock}
        return pkgs | sys.stdlib_module_names

    def __read_ignore_imports(self) -> set[str]:
        with open(self.__root_path / "pyproject.toml", "rb") as f:
            pyproject = tomli.load(f)
        return set(
            pyproject.get("tool")
            .get("clean_architecture", {})
            .get("ignore_import_names", [])
        )
