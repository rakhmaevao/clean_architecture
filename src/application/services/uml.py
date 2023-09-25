from src.application.project import PythonModule, PythonProject
from src.infra import kroki


class UmlDrawer:
    def draw(self, project: PythonProject, path: str):
        uml_code = self.__generate_uml(project)
        print(uml_code)
        kroki.to_svg(uml_code, path)

    def __generate_uml(self, project: PythonProject) -> str:
        plant_uml_code = "skinparam componentStyle uml1\n"
        for _, module in project.modules.items():
            plant_uml_code += (
                f"component [{self._module_repr(module)}] as {module.name}\n"
            )

        for _, module in project.modules.items():
            for imported_module in module.imported_entities.keys():
                plant_uml_code += f"{module.name} --> {imported_module}\n"
        return plant_uml_code

    def _module_repr(self, module: PythonModule) -> str:
        return (
            f"{module.name} \\n"
            f"Path: {module.path} \\n"
            f"I = {module.instability} \\n"
            f"A = {module.abstractness} \\n"
            f"++++++++ \\n"
            f"External used entities: {module.exported_entities} \\n"
            f"Imported entities: {module.imported_entities} \\n"
        )
