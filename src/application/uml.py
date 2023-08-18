from .component import PythonProject
from src.infra import kroki

class UmlDrawer:
    def draw(self, project: PythonProject, path: str):
        uml_code = self.__generate_uml(project)
        kroki.to_svg(uml_code, path)

    
    def __generate_uml(self, project: PythonProject) -> str:
        plant_uml_code = "skinparam componentStyle uml1\n"
        for _, module in project.modules.items():
            plant_uml_code += f"component [{module.name}]\n"

        for _, module in project.modules.items():
            for imported_module in module.imported_entities.keys():
                plant_uml_code += f"{module.name} --> {imported_module}\n"
        return plant_uml_code