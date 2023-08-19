# from src.app import Application

# if __name__ == "__main__":
#     app = Application(micro_service_path="/home/rahmaevao/Projects/konoha/blocks")
#     app.run()


from pathlib import Path
from src.application.services.metrics import compute_short_metrics
from src.application.services.reader.reader import read_project


projects = {
    # "blocks": Path("/home/rahmaevao/Projects/konoha/blocks"),
    # "administrator": Path("/home/rahmaevao/Projects/konoha/administrator"),
    # "filesystem": Path("/home/rahmaevao/Projects/konoha/filesystem"),
    "this": Path("/home/rahmaevao/Projects/clean_architecture"),
}


for project, path in projects.items():
    metrics = compute_short_metrics(read_project(path))
    print(f"{project}: {metrics}")
