from src.application.project import PythonModule, PythonProject
from pathlib import PosixPath


MOCK_PROJECT = PythonProject(
    modules={
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
        "src.presentation.api": PythonModule(
            name="src.presentation.api",
            path=PosixPath("tests/mock_component/src/presentation/api.py"),
            imported_entities={"src.application.parser": {"parse_message"}},
            exported_entities={"router"},
        ),
    },
    path=PosixPath("tests/mock_component"),
)
