from typing import NamedTuple
import pandas as pd
from src.application.project import PythonProject


def compute_metrics(project: PythonProject) -> pd.DataFrame:
    """Полные метрики по проекту

    Возвращает датафрейм с метриками по компонентам.
    """
    return pd.concat(
        [
            pd.DataFrame(
                {
                    # "component": [module.name],
                    "I": [module.full_instability],
                    # "A": [module.abstractness],
                    # "D": [module.distance],
                }
            )
            for module in project.modules.values()
        ],
        # ignore_index=True,
    )


class ShortMetrics(NamedTuple):
    mean: float
    std: float


def compute_short_metrics(project: PythonProject) -> ShortMetrics:
    """Короткие метрики: среднее и дисперсия расстояние от главной прямой

    Оба числа должны быть как можно ближе к нулю.
    """
    return ShortMetrics(
        mean=compute_metrics(project)["D"].mean(),
        std=compute_metrics(project)["D"].std(),
    )
