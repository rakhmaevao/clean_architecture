from .component import CompName, Component


def to_plantuml(components: dict[CompName, Component]) -> str:
    plant_uml_code = "skinparam componentStyle uml1\n"
    for _, component in components.items():
        plant_uml_code += f"component [{component}] as {component.name}\n"

    for _, component in components.items():
        for import_comp in component.imports:
            plant_uml_code += f"{component.name} --> {import_comp}\n"
    return plant_uml_code
