from pathlib import Path
from src.application.component import PythonModule, PythonProject
from src.application.uml import UmlDrawer


def test_uml():
    uml_drawer = UmlDrawer()
    uml_drawer.draw(
        PythonProject(
            modules={
                "main": PythonModule(
                    name="main",
                    path="tests/mock_component/main.py",
                    imported_entities={
                        "src.app": {"Application"},
                        "src.config": {"Config"},
                    },
                    exported_entities=set(),
                ),
                "src.app": PythonModule(
                    name="src.app",
                    path="tests/mock_component/src/app.py",
                    imported_entities={
                        "src.config": {"Config"},
                        "src.presentation.api": {"router"},
                    },
                    exported_entities={"Application"},
                ),
            },
            path=Path("/")
        ),
        "simple.svg",
    )
