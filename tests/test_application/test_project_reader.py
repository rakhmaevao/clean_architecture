from src.application.project_reader import read_project, Component
from src.application.component import PythonModule


def test_simple_read():
    assert read_project("tests/mock_component") == Component(
        path="tests/mock_component",
        modules={
            "main": PythonModule(
                name="main",
                path="main.py",
                imported_entities={"src.app": "Application"},
                exported_entities=set(),
            )
        },
    )
