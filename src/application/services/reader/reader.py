from loguru import logger
from src.application.project import PythonProject, PythonModule, ModuleName
import tomli
from functools import lru_cache
import sys
from pathlib import Path
from src.application.services.reader.inspector import get_all_classes


class ProjectReader:
    def __init__(self, root_path: Path) -> None:
        self.__root_path = root_path

    def read_project(self) -> PythonProject:
        return PythonProject(
            modules=self.__read_py_modules(),
            path=self.__root_path,
        )

    def __read_py_modules(self) -> list[PythonModule]:
        raw_py_modules = self._raw_read_all_py_modules()
        for py_module in raw_py_modules.values():
            for i_m_name, i_entities in py_module.imported_entities.items():
                try:
                    raw_py_modules[i_m_name].exported_entities |= i_entities
                except KeyError:
                    logger.warning(f"Module {i_m_name} not found")
                    pass

        blank_modules = set()
        for py_module in raw_py_modules.values():
            if (
                len(py_module.exported_entities) == 0
                and len(py_module.imported_entities) == 0
            ):
                blank_modules.add(py_module.name)

        [raw_py_modules.pop(b_m) for b_m in blank_modules]
        return raw_py_modules

    def _raw_read_all_py_modules(self) -> dict[ModuleName, PythonModule]:
        ex_libs = self._read_used_libraries()
        ex_libs |= self._read_ignore_imports()
        logger.info(f"{ex_libs=}")
        all_modules = {}
        all_classes = get_all_classes(self.__root_path)
        for path in self._get_python_files():
            for using_class in all_classes:
                if self._is_ex_lib(using_class.src_module_name, ex_libs):
                    continue
                for using_module_path in using_class.using_modules_paths:
                    if using_module_path == path:
                        src_class_module_name = self._generate_module_name(
                            using_class.src_module_path
                        )
                        module_name = self._generate_module_name(path)
                        if module_name not in all_modules:
                            all_modules[module_name] = PythonModule(
                                name=module_name,
                                path=path,
                                imported_entities={
                                    src_class_module_name: set([using_class.class_name])
                                },
                                exported_entities=set(),
                            )
                        else:
                            if (
                                src_class_module_name
                                in all_modules[module_name].imported_entities
                            ):
                                all_modules[module_name].imported_entities[
                                    src_class_module_name
                                ].add(using_class.class_name)
                            else:
                                all_modules[module_name].imported_entities[
                                    src_class_module_name
                                ] = set([using_class.class_name])
        return all_modules

    def _generate_module_name(self, path: Path) -> str:
        m_name = (
            path.relative_to(self.__root_path)
            .with_suffix("")
            .as_posix()
            .replace("/", ".")[1:]
        )
        if m_name.split(".")[-1] == "__init__":
            m_name = ".".join(m_name.split(".")[:-1])
        return m_name

    def _get_python_files(self) -> set[Path]:
        return {path for path in (self.__root_path / "src").rglob("*.py")} | {
            self.__root_path / "main.py"
        }

    @staticmethod
    def _is_ex_lib(module_name: str, ex_libs: set[str]) -> bool:
        return module_name.split(".")[0] in ex_libs

    @lru_cache
    def _read_used_libraries(self) -> set[str]:
        with open(self.__root_path / "poetry.lock", "rb") as f:
            poetry_lock = tomli.load(f)["package"]
        pkgs = {pkg["name"].replace("-", "_") for pkg in poetry_lock}
        return pkgs | sys.stdlib_module_names

    def _read_ignore_imports(self) -> set[str]:
        with open(self.__root_path / "pyproject.toml", "rb") as f:
            pyproject = tomli.load(f)
        return set(
            pyproject.get("tool")
            .get("clean_architecture", {})
            .get("ignore_import_names", [])
        )
