"""
Подробные метрики:
- таблица метрик по компонентам

Уточненные метрики:
- проблемные модули (расстояние и дисперсия больше чем опр. число: зона бесполезности,
зона боли)

Короткие метрики:
- среднее расстояние и дисперсия
"""
from functools import lru_cache
from typing import NamedTuple
import pandas as pd
from src.application.project import PythonProject


def compute_metrics(project: PythonProject) -> pd.DataFrame:
    return pd.concat(
        [
            pd.DataFrame.from_dict(
                {
                    "component": [module.name],
                    "I": [module.instability],
                    "A": [module.abstractness],
                    "D": [module.distance],
                }
            )
            for module in project.modules.values()
        ],
        ignore_index=True,
    )


class ShortMetrics(NamedTuple):
    mean: float
    std: float


def compute_short_metrics(project: PythonProject) -> ShortMetrics:
    return ShortMetrics(
        mean=compute_metrics(project)["D"].mean(),
        std=compute_metrics(project)["D"].std(),
    )
