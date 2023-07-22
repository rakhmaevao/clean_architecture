from src.kroki import draw_plantuml


def test_draw_plantuml():
    assert (
        draw_plantuml(
            """
                        [First component]
    [Another component] as Comp2
    component Comp3
    component [Last\ncomponent] as Comp4
                    """
        )
        == ""
    )
