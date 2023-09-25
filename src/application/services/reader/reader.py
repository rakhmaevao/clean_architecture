from loguru import logger
from src.application.project import PythonProject, PythonModule, ModuleName
import tomli
from functools import lru_cache
import sys
from pathlib import Path
from src.application.services.reader.inspector import get_all_classes


def _generate_module_name(path: Path, root_path: Path) -> str:
    m_name = path.with_suffix("").as_posix().replace("/", ".")[1:]
    if m_name.split(".")[-1] == "__init__":
        m_name = ".".join(m_name.split(".")[:-1])
    return m_name


def _get_python_files(root_path: Path) -> set[Path]:
    return {path for path in (root_path / "src").rglob("*.py")} | {
        root_path / "main.py"
    }


def _raw_read_all_py_modules(
    root_path: Path, main_modules: list[str]
) -> dict[ModuleName, PythonModule]:
    ex_libs = _read_used_libraries(root_path)
    ex_libs |= _read_ignore_imports(root_path)
    all_modules = {}
    all_classes = get_all_classes(root_path, main_modules)
    for path in _get_python_files(root_path):
        for using_class in all_classes:
            src_class_module_name = _generate_module_name(
                using_class.source_module_path, root_path
            )
            for using_module_path in using_class.using_modules_paths:
                if using_module_path == path:
                    module_name = _generate_module_name(path, root_path)
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


def _read_py_modules(root_path: Path, main_modules: list[str]) -> list[PythonModule]:
    raw_py_modules = _raw_read_all_py_modules(root_path, main_modules)
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


def read_project(root_path: Path, main_modules: list[str]) -> PythonProject:
    return PythonProject(
        modules=_read_py_modules(root_path, main_modules),
        path=root_path,
    )


@lru_cache
def _read_used_libraries(srv_path: Path) -> set[str]:
    with open(srv_path / "poetry.lock", "rb") as f:
        poetry_lock = tomli.load(f)["package"]
    pkgs = {pkg["name"].replace("-", "_") for pkg in poetry_lock}
    return pkgs | sys.stdlib_module_names


def _read_ignore_imports(srv_path: Path) -> set[str]:
    with open(srv_path / "pyproject.toml", "rb") as f:
        pyproject = tomli.load(f)
    return set(
        pyproject.get("tool")
        .get("clean_architecture", {})
        .get("ignore_import_names", [])
    )
