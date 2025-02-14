"""
Provides functions to compute interesting and reusable generic metrics
over DataFrame containing rainfall data over years.
"""

from typing import Callable

import pandas as pd

from bcn_rainfall_core.utils import Label
from bcn_rainfall_core.utils import dataframe_operations as df_ops


def get_average_rainfall(yearly_rainfall: pd.DataFrame, *, round_precision=1) -> float:
    """
    Computes Rainfall average.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param round_precision: A float representing the rainfall precision (optional). Defaults to 2.
    :return: A float representing the average Rainfall.
    """
    return yearly_rainfall[Label.RAINFALL.value].mean().round(round_precision)


def get_years_compared_to_given_rainfall_value(
    yearly_rainfall: pd.DataFrame,
    rainfall_value: float,
    *,
    comparator: Callable[[float, float], bool],
) -> int:
    """
    Computes the number of years that conform specified comparison
    to the given rainfall value.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param rainfall_value: A float representing the rainfall value.
    :param comparator: A comparator function that takes exactly two parameters and return a boolean.
    :return: The number of years compared to the given rainfall value as an integer.
    """
    yearly_rainfall = yearly_rainfall[
        comparator(yearly_rainfall[Label.RAINFALL.value], rainfall_value)
    ]

    return int(yearly_rainfall[Label.YEAR.value].count())


def get_clusters_number(yearly_rainfall: pd.DataFrame) -> int:
    """
    Computes the number of clusters.

    :param yearly_rainfall: A pandas DataFrame displaying clusters label according to year.
    :return: The number of clusters as an integer.
    """
    if Label.KMEANS not in yearly_rainfall.columns:
        return 0

    return yearly_rainfall[Label.KMEANS.value].max() + 1


def get_normal(
    yearly_rainfall: pd.DataFrame, begin_year, *, round_precision=1
) -> float:
    """
    Computes average rainfall over 30 years time frame.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param begin_year: A year to start the time frame.
    :param round_precision: A float representing the rainfall precision (optional). Defaults to 2.
    :return: A float storing the normal.
    """

    return get_average_rainfall(
        df_ops.get_rainfall_within_year_interval(
            yearly_rainfall, begin_year=begin_year, end_year=begin_year + 29
        ),
        round_precision=round_precision,
    )
