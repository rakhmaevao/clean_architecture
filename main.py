from src.kroki import draw_plantuml, save_svg
from src.deps import get_deps


from dash import Dash, html


components = get_deps("/home/rahmaevao/Projects/konoha/administrator")

rejection_keys = set()
for component_name, component in components.items():
    if component["path"] is None:
        continue
    if "__init__.py" == component["path"].split("/")[-1]:
        rejection_keys.add(component_name)

for key in rejection_keys:
    del components[key]


for component_name, component in components.items():
    for i in component.get('imports', []):
        if i in rejection_keys:
            component['imports'].remove(i)

plant_uml_code = "skinparam componentStyle uml1\n"
for _, component in components.items():
    plant_uml_code += f"component [{component['name']}] as {component['name']}\n"

for _, component in components.items():
    for import_comp in  component.get("imports", []):
        plant_uml_code += f"{component['name']} --> {import_comp}\n"

svg = draw_plantuml(plant_uml_code)
save_svg(file_path="assets/components_diagrams.svg", svg=svg)

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(children="Analysis of service"),
        html.Img(src="assets/components_diagrams.svg"),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)


{
    "main.py": {
        "bacon": 0,
        "imports": ["src", "src.app", "src.config"],
        "name": "main.py",
        "path": None,
    },
    "src": {
        "bacon": 1,
        "imported_by": [
            "main.py",
            "src.app",
            "src.routes.bugreports.dependencies",
            "src.routes.bugreports.v1",
            "src.routes.version.models",
            "src.routes.version.v1",
            "src.services.bugreports.bugreports",
            "src.services.user_data.user_data",
            "src.services.version.version",
            "src.services.version.version_service",
        ],
        "name": "src",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/__init__.py",
    },
    "src.app": {
        "bacon": 1,
        "imported_by": ["main.py"],
        "imports": [
            "src",
            "src.config",
            "src.routes",
            "src.routes.bugreports",
            "src.routes.bugreports.v1",
            "src.routes.version",
            "src.routes.version.v1",
        ],
        "name": "src.app",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/app.py",
    },
    "src.config": {
        "bacon": 1,
        "imported_by": [
            "main.py",
            "src.app",
            "src.routes.bugreports.v1",
            "src.routes.version.v1",
            "src.services.bugreports.bugreports",
            "src.services.user_data.user_data",
            "src.services.version.version",
            "src.services.version.version_service",
        ],
        "name": "src.config",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/config.py",
    },
    "src.routes": {
        "bacon": 2,
        "imported_by": ["src.app"],
        "name": "src.routes",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/routes/__init__.py",
    },
    "src.routes.bugreports": {
        "bacon": 2,
        "imported_by": ["src.app"],
        "imports": ["src.routes.bugreports.v1"],
        "name": "src.routes.bugreports",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/routes/bugreports/__init__.py",
    },
    "src.routes.bugreports.dependencies": {
        "bacon": 3,
        "imported_by": ["src.routes.bugreports.v1"],
        "imports": [
            "src",
            "src.services",
            "src.services.user_data",
            "src.services.user_data.models",
            "src.services.user_data.user_data",
        ],
        "name": "src.routes.bugreports.dependencies",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/routes/bugreports/dependencies.py",
    },
    "src.routes.bugreports.models": {
        "bacon": 3,
        "imported_by": ["src.routes.bugreports.v1"],
        "name": "src.routes.bugreports.models",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/routes/bugreports/models.py",
    },
    "src.routes.bugreports.v1": {
        "bacon": 2,
        "imported_by": ["src.app", "src.routes.bugreports"],
        "imports": [
            "src",
            "src.config",
            "src.routes.bugreports.dependencies",
            "src.routes.bugreports.models",
            "src.services",
            "src.services.bugreports",
            "src.services.bugreports.bugreports",
            "src.services.bugreports.models",
            "src.services.user_data",
            "src.services.user_data.models",
        ],
        "name": "src.routes.bugreports.v1",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/routes/bugreports/v1.py",
    },
    "src.routes.version": {
        "bacon": 2,
        "imported_by": ["src.app"],
        "imports": ["src.routes.version.v1"],
        "name": "src.routes.version",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/routes/version/__init__.py",
    },
    "src.routes.version.models": {
        "bacon": 3,
        "imported_by": ["src.routes.version.v1"],
        "imports": [
            "src",
            "src.services",
            "src.services.version",
            "src.services.version.models",
        ],
        "name": "src.routes.version.models",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/routes/version/models.py",
    },
    "src.routes.version.v1": {
        "bacon": 2,
        "imported_by": ["src.app", "src.routes.version"],
        "imports": [
            "src",
            "src.config",
            "src.routes.version.models",
            "src.services",
            "src.services.version",
            "src.services.version.exceptions",
            "src.services.version.models",
            "src.services.version.version",
            "src.services.version.version_service",
        ],
        "name": "src.routes.version.v1",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/routes/version/v1.py",
    },
    "src.services": {
        "bacon": 3,
        "imported_by": [
            "src.routes.bugreports.dependencies",
            "src.routes.bugreports.v1",
            "src.routes.version.models",
            "src.routes.version.v1",
            "src.services.bugreports.bugreports",
            "src.services.user_data.user_data",
            "src.services.version.version_service",
        ],
        "name": "src.services",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/__init__.py",
    },
    "src.services.bugreports": {
        "bacon": 3,
        "imported_by": [
            "src.routes.bugreports.v1",
            "src.services.bugreports.bugreports",
        ],
        "name": "src.services.bugreports",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/bugreports/__init__.py",
    },
    "src.services.bugreports.bugreports": {
        "bacon": 3,
        "imported_by": ["src.routes.bugreports.v1"],
        "imports": [
            "src",
            "src.config",
            "src.services",
            "src.services.bugreports",
            "src.services.bugreports.models",
        ],
        "name": "src.services.bugreports.bugreports",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/bugreports/bugreports.py",
    },
    "src.services.bugreports.models": {
        "bacon": 3,
        "imported_by": [
            "src.routes.bugreports.v1",
            "src.services.bugreports.bugreports",
        ],
        "name": "src.services.bugreports.models",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/bugreports/models.py",
    },
    "src.services.user_data": {
        "bacon": 3,
        "imported_by": [
            "src.routes.bugreports.dependencies",
            "src.routes.bugreports.v1",
            "src.services.user_data.user_data",
        ],
        "name": "src.services.user_data",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/user_data/__init__.py",
    },
    "src.services.user_data.models": {
        "bacon": 3,
        "imported_by": [
            "src.routes.bugreports.dependencies",
            "src.routes.bugreports.v1",
            "src.services.user_data.user_data",
        ],
        "name": "src.services.user_data.models",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/user_data/models.py",
    },
    "src.services.user_data.user_data": {
        "bacon": 4,
        "imported_by": ["src.routes.bugreports.dependencies"],
        "imports": [
            "src",
            "src.config",
            "src.services",
            "src.services.user_data",
            "src.services.user_data.models",
        ],
        "name": "src.services.user_data.user_data",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/user_data/user_data.py",
    },
    "src.services.version": {
        "bacon": 3,
        "imported_by": [
            "src.routes.version.models",
            "src.routes.version.v1",
            "src.services.version.version_service",
        ],
        "name": "src.services.version",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/version/__init__.py",
    },
    "src.services.version.exceptions": {
        "bacon": 3,
        "imported_by": ["src.routes.version.v1"],
        "name": "src.services.version.exceptions",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/version/exceptions.py",
    },
    "src.services.version.models": {
        "bacon": 3,
        "imported_by": [
            "src.routes.version.models",
            "src.routes.version.v1",
            "src.services.version.version",
            "src.services.version.version_service",
        ],
        "name": "src.services.version.models",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/version/models.py",
    },
    "src.services.version.version": {
        "bacon": 3,
        "imported_by": ["src.routes.version.v1"],
        "imports": [
            "src",
            "src.config",
            "src.services.version.models",
            "src.services.version.version_service",
        ],
        "name": "src.services.version.version",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/version/version.py",
    },
    "src.services.version.version_service": {
        "bacon": 3,
        "imported_by": ["src.routes.version.v1", "src.services.version.version"],
        "imports": [
            "src",
            "src.config",
            "src.services",
            "src.services.version",
            "src.services.version.models",
        ],
        "name": "src.services.version.version_service",
        "path": "/home/rahmaevao/Projects/konoha/administrator/src/services/version/version_service.py",
    },
}
