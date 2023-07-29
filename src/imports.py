from typing import NamedTuple
from pyparsing import Word, alphas, nums
import ast

entity_name = Word(alphas + "_" + nums)


def _parse_use_from_dot(string: str, module_prefix: str) -> set[str]:
    sub_strings = string.split(f"{module_prefix}.")
    entities = set()
    if len(sub_strings) != 1:
        for s in sub_strings[1:]:
            entities.add(entity_name.parse_string(s).as_list()[0])
    return entities


class ImportedEntitiesStorage:
    def __init__(self) -> None:
        self.__storage = dict()

    def add(self, module: str, entity: str) -> None:
        if module not in self.__storage:
            self.__storage[module] = set()
        self.__storage[module].add(entity)

    def get(self, module: str) -> set[str]:
        if module not in self.__storage:
            return set()
        return self.__storage[module]

    def get_modules(self) -> list[str]:
        return list(self.__storage.keys())


class ImportInstruction(NamedTuple):
    module: str
    alias: str

    @property
    def prefix(self):
        if self.alias is not None:
            return self.alias
        return self.module


def get_imported_entities_by_modules(path: str) -> ImportedEntitiesStorage:
    imported_entities = ImportedEntitiesStorage()
    imported_modules = []
    with open(path, "r") as f:
        ast_code = ast.parse(f.read())
    for node in ast.walk(ast_code):
        if isinstance(node, ast.ImportFrom):
            [imported_entities.add(node.module, name.name) for name in node.names]
        if isinstance(node, ast.Import):
            for module in node.names:
                imported_modules.append(ImportInstruction(module.name, module.asname))

    with open(path, "r") as f:
        for line in f:
            for module in imported_modules:
                entities = _parse_use_from_dot(line, module.prefix)
                if entities:
                    [imported_entities.add(module.module, e) for e in entities]
    return imported_entities
