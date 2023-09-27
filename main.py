from pathlib import Path

from pprint import pprint
from loguru import logger
# from src.application.services.metrics import compute_metrics
from src.application.services.reader.reader import ProjectReader
from src.application.services.uml import UmlDrawer

projects = {
    # "blocks": Path("/home/rahmaevao/Projects/konoha/blocks"),
    # "administrator": Path("/home/rahmaevao/Projects/konoha/administrator"),
    # "filesystem": Path("/home/rahmaevao/Projects/konoha/filesystem"),
    # "this": Path("/home/rahmaevao/Projects/clean_architecture"),
    "tests": Path("/home/rahmaevao/Projects/clean_architecture/tests/mock_component"),
}


for project_name, path in projects.items():
    project = ProjectReader(path).read_project()
    pprint(project.modules)
    # metrics = compute_short_metrics(project)
    # metrics = compute_metrics(project)
    # print(metrics.to_string())
    # [print(f"{modd.name}\t{modd.instability}") for modd in project.modules.values()]
    # print(metrics)
    # print(f"{project_name}: {metrics}")
    # pprint(project)
    
    uml_drawer = UmlDrawer()
    uml_drawer.draw(
        project,
        f"{project_name}.svg",
    )
