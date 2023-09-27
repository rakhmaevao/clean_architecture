import ast
from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import TypeAlias

from loguru import logger
from src.application.project import EntityKind
import subprocess

EntityName: TypeAlias = str


@dataclass
class EntitySearchingResult:
    name: EntityName
    kind: EntityKind
    src_module_path: Path
    using_modules_paths: set[Path]


class EntitiesSearchingResultVault:
    def __init__(self):
        self.entities: dict[EntityName, EntitySearchingResult] = dict()

    def add(
        self,
        entity_name: EntityName,
        entity_type: EntityKind,
        src_module_path: Path | None,
        using_path: Path,
    ):
        if entity_name not in self.entities:
            self.entities[entity_name] = EntitySearchingResult(
                name=entity_name,
                kind=entity_type,
                src_module_path=src_module_path,
                using_modules_paths=set([using_path]),
            )
        else:
            self.entities[entity_name].using_modules_paths.add(using_path)

    def values(self) -> list[EntitySearchingResult]:
        return list(self.entities.values())


def get_all_entities(project_path: Path) -> list[EntitySearchingResult]:
    entities = _get_raw_entities(project_path)
    logger.info("All entities found.")
    entities = _set_src_for_globals(entities, project_path)
    logger.info(f"Globals parsed.")
    entities = _set_abc(entities)
    logger.info("Abstract classes parsed.")
    logger.info("All entities parsed.")
    logger.debug(f"Parsed entities:\n{entities}")
    return entities


def _get_raw_entities(project_path: Path) -> list[EntitySearchingResult]:
    results = subprocess.run(
        [
            f"{project_path}/.venv/bin/python",
            f"{os.getcwd()}/src/application/services/reader/inspect2.py",
        ],
        check=False,
        text=True,
        capture_output=True,
        cwd=project_path,
    )
    if results.returncode:
        logger.error(f"Error in inspection: {results.stderr}")
    return [
        EntitySearchingResult(
            name=r[0],
            kind=EntityKind(r[1]),
            src_module_path=Path(r[2]) if r[2] is not None else None,
            using_modules_paths={Path(p) for p in r[3] if p is not None},
        )
        for r in json.loads(results.stdout).values()
    ]


def _set_src_for_globals(
    entities: list[EntitySearchingResult], project_path: Path
) -> list[EntitySearchingResult]:
    for entity in entities:
        if entity.kind is EntityKind.VARIABLE:
            pass

    for root, _, files in os.walk(project_path):
        for filename in files:
            if not filename.endswith(".py"):
                continue
            with open(f"{root}/{filename}", "r") as file:
                code = file.read()

            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            for entity in entities:
                                if (
                                    entity.kind is EntityKind.VARIABLE
                                    and target.id == entity.name
                                ):
                                    entity.src_module_path = Path(f"{root}/{filename}")
    return entities


def _set_abc(entities: list[EntitySearchingResult]) -> list[EntitySearchingResult]:
    for entity in entities:
        if entity.kind is not EntityKind.CLASS:
            continue
        if entity.src_module_path.suffix != ".py":
            continue
        with open(entity.src_module_path, "r") as file:
            code = file.read()
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == entity.name:
                if any([n.id == "ABC" for n in node.bases if isinstance(n, ast.Name)]):
                    entity.kind = EntityKind.ABSTRACT

    return entities


# [
#     EntitySearchingResult(
#         name="Config",
#         kind="class",
#         src_module_path=PosixPath(
#             "/home/rahmaevao/Projects/clean_architecture/tests/mock_component/src/config.py"
#         ),
#         using_modules_paths={PosixPath("src/config.py")},
#     ),
#     EntitySearchingResult(
#         name="dataclass",
#         kind="function",
#         src_module_path=PosixPath("/usr/lib/python3.10/dataclasses.py"),
#         using_modules_paths={PosixPath("src/config.py")},
#     ),
#     EntitySearchingResult(
#         name="SomeModel",
#         kind="class",
#         src_module_path=PosixPath(
#             "/home/rahmaevao/Projects/clean_architecture/tests/mock_component/src/application/models.py"
#         ),
#         using_modules_paths={PosixPath("src/application/models.py")},
#     ),
#     EntitySearchingResult(
#         name="ABC",
#         kind="class",
#         src_module_path=PosixPath("/usr/lib/python3.10/abc.py"),
#         using_modules_paths={PosixPath("src/application/message.py")},
#     ),
#     EntitySearchingResult(
#         name="Message",
#         kind="class",
#         src_module_path=PosixPath(
#             "/home/rahmaevao/Projects/clean_architecture/tests/mock_component/src/application/message.py"
#         ),
#         using_modules_paths={PosixPath("src/application/message.py")},
#     ),
#     EntitySearchingResult(
#         name="SomeInterface",
#         kind="abstract",
#         src_module_path=PosixPath(
#             "/home/rahmaevao/Projects/clean_architecture/tests/mock_component/src/application/message.py"
#         ),
#         using_modules_paths={PosixPath("src/application/message.py")},
#     ),
# ]
