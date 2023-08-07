from loguru import logger
from .component import Component, PythonModule
from .imports import get_imported_entities

def read_module(path) -> PythonModule:
    return PythonModule(
        name="main",
        path=path,
        imported_entities=get_imported_entities(path).to_dict(),
        exported_entities=set(),
    )

def read_project(path: str) -> Component:
    mod = read_module(f"{path}/main.py")
    logger.info(f"Imported entities: {mod.to_dict()}")


