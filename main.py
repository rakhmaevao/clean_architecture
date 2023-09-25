import sys

MAIN_MODULES = list(sys.modules.keys())
from pathlib import Path
from src.application.services.metrics import compute_short_metrics
from src.application.services.reader.reader import read_project
from src.application.services.uml import UmlDrawer

projects = {
    # "blocks": Path("/home/rahmaevao/Projects/konoha/blocks"),
    # "administrator": Path("/home/rahmaevao/Projects/konoha/administrator"),
    # "filesystem": Path("/home/rahmaevao/Projects/konoha/filesystem"),
    # "this": Path("/home/rahmaevao/Projects/clean_architecture"),
    "tests": Path("/home/rahmaevao/Projects/clean_architecture/tests/mock_component"),
}


for project_name, path in projects.items():
    project = read_project(path, MAIN_MODULES)
    metrics = compute_short_metrics(project)
    print(f"{project_name}: {metrics}")
    uml_drawer = UmlDrawer()
    uml_drawer.draw(
        project,
        f"{project_name}.svg",
    )
