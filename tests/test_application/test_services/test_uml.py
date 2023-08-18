from src.application.project import PythonModule, PythonProject
from src.application.services.uml import UmlDrawer
import pytest


@pytest.fixture(scope="session")
def mock_project() -> PythonProject:
    return PythonProject(
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
                exported_entities=set(),
            ),
            "src.config": PythonModule(
                name="src.config",
                path="tests/mock_component/src/config.py",
                imported_entities={},
                exported_entities=set(),
            ),
            "src": PythonModule(
                name="src",
                path="tests/mock_component/src/__init__.py",
                imported_entities={},
                exported_entities=set(),
            ),
            "src.application.parser": PythonModule(
                name="src.application.parser",
                path="tests/mock_component/src/application/parser.py",
                imported_entities={"src.application.message": {"Message"}},
                exported_entities=set(),
            ),
            "src.application.message": PythonModule(
                name="src.application.message",
                path="tests/mock_component/src/application/message.py",
                imported_entities={},
                exported_entities=set(),
            ),
            "src.application": PythonModule(
                name="src.application",
                path="tests/mock_component/src/application/__init__.py",
                imported_entities={},
                exported_entities=set(),
            ),
            "src.presentation.api": PythonModule(
                name="src.presentation.api",
                path="tests/mock_component/src/presentation/api.py",
                imported_entities={"src.application.parser": {"parse_message"}},
                exported_entities=set(),
            ),
        },
        path="tests/mock_component",
    )


def test_uml(mock_project):
    uml_drawer = UmlDrawer()
    uml_drawer.draw(
        mock_project,
        "simple.svg",
    )
