from src.application.imports import _generate_module_name
import pytest
from pathlib import Path


@pytest.mark.parametrize(
    "ast_module_name, level, path, expected",
    [
        (
            "src.some_package.second",
            0,
            "src.some_package.first",
            "src.some_package.second",
        ),
        (
            "second",
            1,
            "src.some_package.first",
            "src.some_package.second",
        ),
        (
            "second",
            2,
            "src.some_package.first",
            "src.second",
        ),
    ],
)
def test_get_module_name_for_relative_import(ast_module_name, level, path, expected):
    assert _generate_module_name(ast_module_name, level, path) == expected
