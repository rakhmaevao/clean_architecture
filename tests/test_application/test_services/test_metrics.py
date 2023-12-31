import pandas as pd
from src.application.services.metrics import (
    ShortMetrics,
    compute_metrics,
    compute_short_metrics,
)
from tests.test_application.const import MOCK_PROJECT
from pandas.testing import assert_frame_equal


def test_compute_metrics():
    assert_frame_equal(
        compute_metrics(MOCK_PROJECT),
        pd.DataFrame.from_dict(
            {
                "component": [
                    "main",
                    "src.app",
                    "src.config",
                    "src.application.parser",
                    "src.application.message",
                    "src.presentation.api",
                ],
                "I": [0.0, 0.3333333333333333, 1.0, 0.5, 1.0, 0.5],
                "A": [0.0, 0.0, 0.0, 0.0, 0.5, 0.0],
                "D": [1.0, 0.6666666666666667, 0.0, 0.5, 0.5, 0.5],
            }
        ),
    )


def test_compute_short_metrics():
    assert compute_short_metrics(MOCK_PROJECT) == ShortMetrics(
        mean=0.5277777777777778, std=0.3234650361779919
    )
