from src.application.services.uml import UmlDrawer
from tests.test_application.const import MOCK_PROJECT


def test_uml():
    uml_drawer = UmlDrawer()
    uml_drawer.draw(
        MOCK_PROJECT,
        "simple.svg",
    )
