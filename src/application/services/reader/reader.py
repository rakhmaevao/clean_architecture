from loguru import logger
from src.application.project import PythonProject, PythonModule, ModuleName
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
    return [path for path in (root_path / "src").rglob("*.py")] + [
        root_path / "main.py"
    ]


def _raw_read_all_py_modules(root_path: Path) -> dict[ModuleName, PythonModule]:
    ex_libs = _read_used_libraries(root_path)
    ex_libs |= _read_ignore_imports(root_path)
    all_modules = {}
    for path in _get_python_files(root_path):
        module = _read_module(path, root_path, ex_libs)
        all_modules[module.name] = module
    return all_modules


def _read_py_modules(root_path: Path) -> list[PythonModule]:
    raw_py_modules = _raw_read_all_py_modules(root_path)
    for py_module in raw_py_modules.values():
        for i_m_name, i_entities in py_module.imported_entities.items():
            try:
                raw_py_modules[i_m_name].exported_entities |= i_entities
            except KeyError:
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


def read_project(root_path: Path) -> PythonProject:
    return PythonProject(
        modules=_read_py_modules(root_path),
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
