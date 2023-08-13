from src.infra.kroki import draw_plantuml, save_svg
from src._plantuml_coder import to_plantuml
from src._micro_service import MicroService
import plotly.express as px
from dash import Dash, html, dcc


class Application:
    def __init__(self, micro_service_path: str) -> None:
        micro_service = MicroService(micro_service_path)

        svg = draw_plantuml(to_plantuml(micro_service.components))
        save_svg(file_path="assets/components_diagrams.svg", svg=svg)

        df = micro_service.get_i_a_statistics()
        print(df)

        self.__app = Dash(__name__)

        self.__app.layout = html.Div(
            [
                dcc.Markdown(
                    """
                    # Анализ сервиса на соответствие критериям сочетаемости компонентов

                    Для каждого компонента приводится:
                    - неустойчивость `I`;
                    - абстрактность `A`;
                    - расстояние от главной последовательности `D`.

                    В целом надо стремится к тому, чтобы расстояние `D` было близким к нулю.
                    """
                ),
                dcc.Markdown(
                    f"""
                    ## Отчет

                    Стандартное отклонение расстояния компонентов сервиса {df['D'].std( )}
                    """
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    figure=px.scatter(
                                        df,
                                        x="I",
                                        y="A",
                                        symbol="component",
                                        range_x=[0, 1],
                                        range_y=[0, 1],
                                    )
                                )
                            ],
                            style={"width": "50%", "display": "inline-block"},
                        ),
                        html.Div(
                            [dcc.Graph(figure=px.scatter(df, x="component", y="D"))],
                            style={"width": "50%", "display": "inline-block"},
                        ),
                    ],
                ),
                html.Img(src="assets/components_diagrams.svg"),
            ]
        )

    def run(self):
        self.__app.run(debug=True)
