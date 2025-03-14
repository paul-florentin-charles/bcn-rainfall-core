"""
Provides functions to do operations on DataFrame objects
containing rainfall data over years.
"""

import pandas as pd

from bcn_rainfall_core.utils import Label


def get_rainfall_within_year_interval(
    yearly_rainfall: pd.DataFrame,
    *,
    begin_year: int,
    end_year: int | None = None,
) -> pd.DataFrame:
    """
    Retrieves Yearly Rainfall within a specific year range.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values (optional).
    :return: A pandas DataFrame displaying rainfall data (in mm) according to year.
    """
    if end_year is not None:
        yearly_rainfall = yearly_rainfall[yearly_rainfall[Label.YEAR.value] <= end_year]

    return yearly_rainfall[yearly_rainfall[Label.YEAR.value] >= begin_year]


def remove_column(yearly_rainfall: pd.DataFrame, *, label: Label) -> bool:
    """
    Remove a column from a DataFrame using its label.
    Removing 'Year' or 'Rainfall' columns is prevented.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data
    under various shapes according to year.
    :param label: A string corresponding to an existing column label.
    :return: A boolean set to whether the operation passed or not.
    """
    if label not in yearly_rainfall.columns.drop([Label.YEAR, Label.RAINFALL]):
        return False

    yearly_rainfall.pop(label.value)

    return True


def concat_columns(data_frames: list[pd.DataFrame | pd.Series]) -> pd.DataFrame:
    """
    Concatenate pandas DataFrame objects along the column axis.

    :param data_frames: List of pandas DataFrame of same dimension along the row axis.
    :return: The concatenation result as a pandas DataFrame.
    """

    return pd.concat(data_frames, axis="columns")


def retrieve_rainfall_data_with_constraints(
    monthly_rainfall: pd.DataFrame,
    *,
    starting_year: int,
    round_precision: int,
    start_month: int,
    end_month: int | None = None,
) -> pd.DataFrame:
    """
    Apply transformations to a pandas DataFrame depicting Yearly rainfall data
    for each month of the year.

    :param monthly_rainfall: A DataFrame representing Yearly rainfall data for each month
    :param starting_year: An integer representing the year we should start get value from
    :param round_precision: A integer representing decimal precision for rainfall data
    :param start_month: An integer representing the month
    to start getting our rainfall values.
    :param end_month: An integer representing the month
    to end getting our rainfall values (optional).
    If not given, we load rainfall data only for given start_month.
    :return: A pandas DataFrame displaying rainfall data (in mm) according to year.
    """
    years = monthly_rainfall.iloc[:, :1]
    if end_month is not None and end_month < start_month:
        rainfall = concat_columns(
            [
                monthly_rainfall.iloc[:, start_month : start_month + 1],
                monthly_rainfall.iloc[:, 1 : end_month + 1],
            ]
        )
    else:
        rainfall = monthly_rainfall.iloc[
            :, start_month : (end_month or start_month) + 1
        ]

    yearly_rainfall = concat_columns([years, rainfall.sum(axis="columns")]).set_axis(
        [Label.YEAR.value, Label.RAINFALL.value], axis="columns"
    )

    yearly_rainfall = get_rainfall_within_year_interval(
        yearly_rainfall, begin_year=starting_year
    )

    yearly_rainfall[Label.RAINFALL.value] = round(
        yearly_rainfall[Label.RAINFALL.value], round_precision
    )

    return yearly_rainfall
