from loguru import logger
from .component import Component, PythonModule
from .imports import get_imported_entities
import tomli
from functools import lru_cache
import sys
from pathlib import Path


def _generate_module_name(path: Path, root_path: Path) -> str:
    m_name = path.relative_to(root_path).with_suffix("").as_posix().replace("/", ".")
    if m_name.split(".")[-1] == "__init__":
        m_name = ".".join(m_name.split(".")[:-1])
    return m_name


def _read_module(path: Path, root_path: Path, ex_libs: set[str]) -> PythonModule:
    name = _generate_module_name(path, root_path)
    imported_entities = get_imported_entities(name, path)
    return PythonModule(
        name=name,
        path=path,
        imported_entities={
            module_name: set(imported_entities.get(module_name))
            for module_name in imported_entities.get_modules()
            if module_name.split(".")[0] not in ex_libs
        },
        exported_entities=set(),
    )


def _get_python_files(root_path: Path) -> list[Path]:
    return [path for path in root_path.rglob("*.py")]


def _read_all_py_modules(root_path: Path) -> list[PythonModule]:
    ex_libs = _read_used_libraries(root_path)
    return [
        _read_module(path, root_path, ex_libs) for path in _get_python_files(root_path)
    ]


@lru_cache
def _read_used_libraries(srv_path: Path) -> set[str]:
    with open(srv_path / "poetry.lock", "rb") as f:
        poetry_lock = tomli.load(f)["package"]
    pkgs = {pkg["name"].replace("-", "_") for pkg in poetry_lock}
    libs = pkgs | sys.stdlib_module_names
    return libs
