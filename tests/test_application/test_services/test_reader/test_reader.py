import pytest
from src.application.services.reader.reader import (
    _raw_read_all_py_modules,
    _get_python_files,
    _generate_module_name,
    _read_py_modules,
    read_project,
)
from src.application.project import PythonModule, PythonProject
from pathlib import Path, PosixPath


@pytest.mark.parametrize(
    "path, root_path, m_name",
    [
        (Path("some_soot_path/main.py"), Path("some_soot_path"), "main"),
        (
            Path("some_soot_path/some_pkg/some_module.py"),
            Path("some_soot_path"),
            "some_pkg.some_module",
        ),
        (
            Path("some_soot_path/some_pkg/__init__.py"),
            Path("some_soot_path"),
            "some_pkg",
        ),
    ],
)
def test_module_name_generation(path, root_path, m_name):
    assert _generate_module_name(path, root_path) == m_name


def test_simple_read():
    assert _raw_read_all_py_modules(Path("tests/mock_component")) == {
        "main": PythonModule(
            name="main",
            path=PosixPath("tests/mock_component/main.py"),
            imported_entities={"src.app": {"Application"}, "src.config": {"Config"}},
            exported_entities=set(),
        ),
        "src.app": PythonModule(
            name="src.app",
            path=PosixPath("tests/mock_component/src/app.py"),
            imported_entities={
                "src.config": {"Config"},
                "src.presentation.api": {"router"},
            },
            exported_entities=set(),
        ),
        "src.config": PythonModule(
            name="src.config",
            path=PosixPath("tests/mock_component/src/config.py"),
            imported_entities={},
            exported_entities=set(),
        ),
        "src": PythonModule(
            name="src",
            path=PosixPath("tests/mock_component/src/__init__.py"),
            imported_entities={},
            exported_entities=set(),
        ),
        "src.application.parser": PythonModule(
            name="src.application.parser",
            path=PosixPath("tests/mock_component/src/application/parser.py"),
            imported_entities={"src.application.message": {"Message"}},
            exported_entities=set(),
        ),
        "src.application.message": PythonModule(
            name="src.application.message",
            path=PosixPath("tests/mock_component/src/application/message.py"),
            imported_entities={},
            exported_entities=set(),
        ),
        "src.application": PythonModule(
            name="src.application",
            path=PosixPath("tests/mock_component/src/application/__init__.py"),
            imported_entities={},
            exported_entities=set(),
        ),
        "src.presentation.api": PythonModule(
            name="src.presentation.api",
            path=PosixPath("tests/mock_component/src/presentation/api.py"),
            imported_entities={"src.application.parser": {"parse_message"}},
            exported_entities=set(),
        ),
    }


def test_get_all_python_files():
    assert _get_python_files(Path("tests/mock_component")) == [
        PosixPath("tests/mock_component/main.py"),
        PosixPath("tests/mock_component/src/app.py"),
        PosixPath("tests/mock_component/src/config.py"),
        PosixPath("tests/mock_component/src/__init__.py"),
        PosixPath("tests/mock_component/src/application/parser.py"),
        PosixPath("tests/mock_component/src/application/message.py"),
        PosixPath("tests/mock_component/src/application/__init__.py"),
        PosixPath("tests/mock_component/src/presentation/api.py"),
    ]


def test_read_project():
    assert _read_py_modules(Path("tests/mock_component")) == {
        "main": PythonModule(
            name="main",
            path=PosixPath("tests/mock_component/main.py"),
            imported_entities={"src.app": {"Application"}, "src.config": {"Config"}},
            exported_entities=set(),
        ),
        "src.app": PythonModule(
            name="src.app",
            path=PosixPath("tests/mock_component/src/app.py"),
            imported_entities={
                "src.config": {"Config"},
                "src.presentation.api": {"router"},
            },
            exported_entities={"Application"},
        ),
        "src.config": PythonModule(
            name="src.config",
            path=PosixPath("tests/mock_component/src/config.py"),
            imported_entities={},
            exported_entities={"Config"},
        ),
        "src": PythonModule(
            name="src",
            path=PosixPath("tests/mock_component/src/__init__.py"),
            imported_entities={},
            exported_entities=set(),
        ),
        "src.application.parser": PythonModule(
            name="src.application.parser",
            path=PosixPath("tests/mock_component/src/application/parser.py"),
            imported_entities={"src.application.message": {"Message"}},
            exported_entities={"parse_message"},
        ),
        "src.application.message": PythonModule(
            name="src.application.message",
            path=PosixPath("tests/mock_component/src/application/message.py"),
            imported_entities={},
            exported_entities={"Message"},
        ),
        "src.application": PythonModule(
            name="src.application",
            path=PosixPath("tests/mock_component/src/application/__init__.py"),
            imported_entities={},
            exported_entities=set(),
        ),
        "src.presentation.api": PythonModule(
            name="src.presentation.api",
            path=PosixPath("tests/mock_component/src/presentation/api.py"),
            imported_entities={"src.application.parser": {"parse_message"}},
            exported_entities={"router"},
        ),
    }


def test_read_project():
    assert read_project(Path("tests/mock_component")) == PythonProject(
        modules={
            "main": PythonModule(
                name="main",
                path=PosixPath("tests/mock_component/main.py"),
                imported_entities={
                    "src.app": {"Application"},
                    "src.config": {"Config"},
                },
                exported_entities=set(),
            ),
            "src.app": PythonModule(
                name="src.app",
                path=PosixPath("tests/mock_component/src/app.py"),
                imported_entities={
                    "src.config": {"Config"},
                    "src.presentation.api": {"router"},
                },
                exported_entities={"Application"},
            ),
            "src.config": PythonModule(
                name="src.config",
                path=PosixPath("tests/mock_component/src/config.py"),
                imported_entities={},
                exported_entities={"Config"},
            ),
            "src": PythonModule(
                name="src",
                path=PosixPath("tests/mock_component/src/__init__.py"),
                imported_entities={},
                exported_entities=set(),
            ),
            "src.application.parser": PythonModule(
                name="src.application.parser",
                path=PosixPath("tests/mock_component/src/application/parser.py"),
                imported_entities={"src.application.message": {"Message"}},
                exported_entities={"parse_message"},
            ),
            "src.application.message": PythonModule(
                name="src.application.message",
                path=PosixPath("tests/mock_component/src/application/message.py"),
                imported_entities={},
                exported_entities={"Message"},
            ),
            "src.application": PythonModule(
                name="src.application",
                path=PosixPath("tests/mock_component/src/application/__init__.py"),
                imported_entities={},
                exported_entities=set(),
            ),
            "src.presentation.api": PythonModule(
                name="src.presentation.api",
                path=PosixPath("tests/mock_component/src/presentation/api.py"),
                imported_entities={"src.application.parser": {"parse_message"}},
                exported_entities={"router"},
            ),
        },
        path=PosixPath("tests/mock_component"),
    )
