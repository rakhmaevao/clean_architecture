from src.application.project_reader import read_project, Component


def test_simple_read():
    assert read_project("tests/mock_component") == Component(
        path="tests/mock_component", modules={"a1": {"A1", "A3", "A2"}}
    )
