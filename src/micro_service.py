import pandas as pd
from .component import Component, CompName
from .deps import get_deps


class MicroService:
    def __init__(self, path: str) -> None:
        self.__components = {
            k: Component.from_dict(v, path) for k, v in get_deps(path).items()
        }

    @property
    def components(self) -> dict[CompName, Component]:
        return self.__components

    def get_i_a_statistics(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(
            {
                "component": [comp.name for comp in self.components.values()],
                "I": [comp.instability for comp in self.components.values()],
                "A": [comp.abstractness for comp in self.components.values()],
                "D": [comp.distance for comp in self.components.values()],
            }
        )
