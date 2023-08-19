"""
Короткие метрики:
- среднее расстояние и дисперсия

Уточненные метрики:
- проблемные модули (расстояние и дисперсия больше чем опр. число: зона бесполезности,
зона боли)

Подробные метрики:
- таблица метрик по компонентам
"""
import pandas as pd
from src.application.project import PythonProject


def compute_metrics(project: PythonProject):
    pass


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
