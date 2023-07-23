import pandas as pd
from .component import Component, CompName
from .deps import get_deps


class MicroService:
    def __init__(self, path: str) -> None:
        components = {k: Component.from_dict(v) for k, v in get_deps(path).items()}
        self.__components = self.__rm_init_files(components)

    @property
    def components(self) -> dict[CompName, Component]:
        return self.__components

    @staticmethod
    def __rm_init_files(components: dict[CompName, Component]) -> None:
        init_file_names = set()
        for _, component in components.items():
            if component.path is None:
                continue
            if "__init__.py" == component.path.split("/")[-1]:
                init_file_names.add(component.name)

        for key in init_file_names:
            del components[key]

        for _, component in components.items():
            imported_components = set(component.imports)
            imported_components.difference_update(init_file_names)
            component.imports = list(imported_components)

            parent_components = set(component.imported_by)
            parent_components.difference_update(init_file_names)
            component.imported_by = list(parent_components)
        return components

    def get_i_a_statistics(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(
            {
                "component": [comp.name for comp in self.components.values()],
                "I": [comp.instability for comp in self.components.values()],
                "A": [comp.abstractness for comp in self.components.values()],
                "D": [comp.distance for comp in self.components.values()]
            }
        )