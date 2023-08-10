from loguru import logger
from .component import Component, PythonModule
from .imports import get_imported_entities
from loguru import logger
import tomli
from functools import lru_cache
import sys


def _read_module(path: str, service_path: str) -> PythonModule:
    imported_entities = get_imported_entities(path)
    return PythonModule(
        name="main",
        path=path,
        imported_entities={
            module_name: set(imported_entities.get(module_name))
            for module_name in imported_entities.get_modules()
            if not is_lib(module_name, service_path)
        },
        exported_entities=set(),
    )


def read_project(path: str) -> Component:
    mod = _read_module(f"{path}/main.py", path)
    logger.info(f"Imported entities: {mod.to_dict()}")


@lru_cache
def _read_used_libraries(srv_path: str) -> set[str]:
    with open(f"{srv_path}/poetry.lock", "rb") as f:
        poetry_lock = tomli.load(f)["package"]
    pkgs = {pkg["name"].replace("-", "_") for pkg in poetry_lock}
    libs = pkgs | sys.stdlib_module_names
    return libs


def is_lib(module_name, srv_path) -> bool:
    libs = _read_used_libraries(srv_path)
    if module_name.split(".")[0] in libs:
        return True
    return False
