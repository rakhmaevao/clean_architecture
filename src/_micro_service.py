from loguru import logger
import pandas as pd
from ._component import Component, CompName
from .deps import get_deps


class MicroService:
    def __init__(self, path: str) -> None:
        self.__components: dict[CompName, Component] = {
            k: Component.from_dict(v, path) for k, v in get_deps(path).items()
        }
        for comp in self.__components.values():
            comp.set_fan_in(self.__compute_fan_in(comp))
            comp.set_external_used_entities(self.__compute_external_used_entities(comp))

    def __compute_fan_in(self, component: Component) -> int:
        fan_in = 0
        for dependent_component_name in component.imported_by:
            fan_in += self.components[
                dependent_component_name
            ].num_imported_entities_from_module(component.name)
        return fan_in

    def __compute_external_used_entities(self, component: Component) -> set[str]:
        external_used_entities = set()
        for dependent_component_name in component.imported_by:
            external_used_entities |= self.components[
                dependent_component_name
            ].imported_entities_from_module(component.name)
        logger.info(
            f"External_used_entities for {component.name} {external_used_entities}"
        )
        return external_used_entities

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
