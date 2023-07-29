from src.imports import get_imported_entities_by_modules
import pytest


@pytest.mark.parametrize("path,expected_n", [("tests/testdata/a.py", 5)])
def test_get_imported_entities_by_modules(path, expected_n):
    imported_entities = get_imported_entities_by_modules(path)

    assert [
        {module: imported_entities.get(module)}
        for module in imported_entities.get_modules()
    ] == [
        {"a1": {"A1", "A3", "A2"}},
        {"adf.asdd": {"Asdf"}},
        {"adf1": {"Asdfdd"}},
        {"a4": {"S1", "S4"}},
        {"a2": {"qazxc", "Dfg", "T"}},
        {"a8": {"qwer", "fgh"}},
    ]
