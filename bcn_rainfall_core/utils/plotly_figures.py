"""
Provides useful functions for plotting rainfall data in all shapes.
"""

from typing import Union

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.basedatatypes import BaseTraceType
from pydantic import PositiveFloat

import bcn_rainfall_core.models as models
from bcn_rainfall_core.utils import Label, TimeMode

FIGURE_TYPE_TO_PLOTLY_TRACE: dict[str, type[BaseTraceType]] = {
    "bar": go.Bar,
    "scatter": go.Scatter,
}


def _get_plotly_trace_by_figure_type(figure_type: str) -> type[BaseTraceType] | None:
    return FIGURE_TYPE_TO_PLOTLY_TRACE.get(figure_type.casefold())


def update_plotly_figure_layout(
    figure: go.Figure,
    *,
    title: str,
    xaxis_title: str | None = None,
    yaxis_title: str | None = None,
    display_xaxis_range_slider=False,
):
    figure.update_layout(
        title=title,
        legend={
            "yanchor": "top",
            "y": 0.99,
            "xanchor": "left",
            "x": 0.01,
            "bgcolor": "rgba(125, 125, 125, 0.7)",
        },
        font={
            "color": "#dfd0c1",
            "family": "Khula, sans-serif",
            "size": 11,
        },
        paper_bgcolor="rgba(34, 34, 34, 0.65)",
        plot_bgcolor="rgba(123, 104, 75, 0.25)",
        margin={"t": 65, "r": 30, "b": 45, "l": 65},
        xaxis={
            "rangeslider_visible": display_xaxis_range_slider,
        },
        yaxis={
            "title_standoff": 5,
        },
        autosize=True,
    )

    if xaxis_title is not None:
        figure.update_xaxes(title_text=xaxis_title)

    if yaxis_title is not None:
        figure.update_yaxes(title_text=yaxis_title)


def get_figure_of_column_according_to_year(
    yearly_rainfall: pd.DataFrame,
    label: Label,
    *,
    figure_type="bar",
    figure_label: str | None = None,
    trace_label: str | None = None,
) -> go.Figure | None:
    """
    Return plotly figure for specified column data according to year.

    :param yearly_rainfall: A pandas DataFrame displaying rainfall data (in mm) according to year.
    :param label: A Label enum designating the column to be displayed as bars for y-values.
    :param figure_type: A case-insensitive string corresponding to a plotly BaseTraceType mapped in global dictionary;
    use private function to retrieve plotly trace class.
    :param figure_label: A string to label graphic data (optional).
    If not set or set to "", label value is used.
    :param trace_label: A string to label trace data (optional).
    If not set or set to "", label value is used.
    :return: A plotly Figure object if data has been successfully plotted, None otherwise.
    """
    if (
        Label.YEAR not in yearly_rainfall.columns
        or label not in yearly_rainfall.columns
    ):
        return None

    if plotly_trace := _get_plotly_trace_by_figure_type(figure_type):
        figure = go.Figure(
            plotly_trace(
                x=yearly_rainfall[Label.YEAR.value],
                y=yearly_rainfall[label.value],
                name=trace_label or label.value,
            )
        )

        update_plotly_figure_layout(
            figure,
            title=figure_label or label.value,
            xaxis_title=Label.YEAR.value,
            yaxis_title=label.value,
            display_xaxis_range_slider=True,
        )

        return figure

    return None


def get_bar_figure_of_rainfall_averages(
    rainfall_instance_by_label: dict[str, "models.MonthlyRainfall"]
    | dict[str, "models.SeasonalRainfall"],
    *,
    time_mode: TimeMode,
    begin_year: int,
    end_year: int,
) -> go.Figure:
    """
    Return plotly bar figure displaying average rainfall for each month or for each season passed through the dict.

    :param rainfall_instance_by_label: A dict of months respectively mapped with instances of MonthlyRainfall
    or a dict of seasons respectively mapped with instances of SeasonalRainfall.
    To be purposeful, all instances should have the same time frame in years.
    :param time_mode: A TimeMode Enum: ['monthly', 'seasonal'].
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A plotly Figure object of the rainfall averages for each month or for each season.
    """
    labels: list[str] = []
    averages: list[float] = []
    for label, rainfall_instance in rainfall_instance_by_label.items():
        labels.append(label)

        averages.append(
            rainfall_instance.get_average_yearly_rainfall(begin_year, end_year)
        )

    figure = go.Figure(go.Bar(x=labels, y=averages, name=time_mode.value.capitalize()))

    update_plotly_figure_layout(
        figure,
        title=f"Average rainfall (mm) between {begin_year} and {end_year}",
        xaxis_title=time_mode.value.capitalize()[:-2],
        yaxis_title=Label.RAINFALL.value,
    )

    return figure


def get_bar_figure_of_rainfall_linreg_slopes(
    rainfall_instance_by_label: dict[str, "models.MonthlyRainfall"]
    | dict[str, "models.SeasonalRainfall"],
    *,
    time_mode: TimeMode,
    begin_year: int,
    end_year: int,
) -> go.Figure:
    """
    Return plotly bar figure displaying rainfall linear regression slopes for each month or
    for each season passed through the dict.

    :param rainfall_instance_by_label: A dict of months respectively mapped with instances of MonthlyRainfall
    or a dict of seasons respectively mapped with instances of SeasonalRainfall.
    :param time_mode: A TimeMode Enum: ['monthly', 'seasonal'].
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A plotly Figure object of the rainfall LinReg slopes for each month.
    """
    labels: list[str] = []
    slopes: list[float] = []
    r2_scores: list[float] = []
    for label, rainfall_instance in rainfall_instance_by_label.items():
        labels.append(label)

        (r2_score, slope), _ = rainfall_instance.get_linear_regression(
            begin_year, end_year
        )

        slopes.append(slope)
        r2_scores.append(r2_score)

    figure = go.Figure(
        go.Bar(
            x=labels,
            y=slopes,
            name=time_mode.value.capitalize(),
        )
    )

    update_plotly_figure_layout(
        figure,
        title=f"Linear regression slope (mm/year) between {begin_year} and {end_year}",
        xaxis_title=time_mode.value.capitalize()[:-2],
        yaxis_title="Linear regression slope (mm/year)",
    )

    return figure


def get_bar_figure_of_relative_distances_to_normal(
    rainfall_instance_by_label: dict[str, "models.MonthlyRainfall"]
    | dict[str, "models.SeasonalRainfall"],
    *,
    time_mode: TimeMode,
    normal_year: int,
    begin_year: int,
    end_year: int,
) -> go.Figure:
    """
    Return plotly bar figure displaying relative distances to normal for each month or
    for each season passed through the dict.

    :param rainfall_instance_by_label: A dict of months respectively mapped with instances of MonthlyRainfall
    or a dict of seasons respectively mapped with instances of SeasonalRainfall.
    :param time_mode: A TimeMode Enum: ['monthly', 'seasonal'].
    :param normal_year: An integer representing the year
    to start computing the 30 years normal of the rainfall.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :return: A plotly Figure object of the rainfall relative distances to normal for each month or for each season.
    """
    labels: list[str] = []
    relative_distances_to_normal: list[float | None] = []
    for label, rainfall_instance in rainfall_instance_by_label.items():
        labels.append(label)
        relative_distances_to_normal.append(
            rainfall_instance.get_relative_distance_to_normal(
                normal_year, begin_year, end_year
            )
        )

    figure = go.Figure(
        go.Bar(
            x=labels,
            y=relative_distances_to_normal,
            name=time_mode.value.capitalize(),
        )
    )

    update_plotly_figure_layout(
        figure,
        title=f"Relative distance to {normal_year}-{normal_year + 29} normal between {begin_year} and {end_year} (%)",
        xaxis_title=time_mode.value.capitalize()[:-2],
        yaxis_title="Relative distance to normal (%)",
    )

    return figure


def get_bar_figure_of_standard_deviations(
    rainfall_instance_by_label: dict[str, "models.MonthlyRainfall"]
    | dict[str, "models.SeasonalRainfall"],
    *,
    time_mode: TimeMode,
    begin_year: int,
    end_year: int,
    weigh_by_average=False,
) -> go.Figure:
    """
    Return plotly bar figure displaying standard deviations for each month or for each season passed through the dict.

    :param rainfall_instance_by_label: A dict of months respectively mapped with instances of MonthlyRainfall
    or a dict of seasons respectively mapped with instances of SeasonalRainfall.
    :param time_mode: A TimeMode Enum: ['monthly', 'seasonal'].
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :param bool weigh_by_average: Whether to divide standard deviation by average or not (optional).
    Defaults to False.
    :return: A plotly Figure object of the rainfall standard deviations for each month or for each season.
    """
    labels: list[str] = []
    standard_deviations: list[float | None] = []
    for label, rainfall_instance in rainfall_instance_by_label.items():
        labels.append(label)

        standard_deviation = rainfall_instance.get_rainfall_standard_deviation(
            begin_year, end_year, weigh_by_average=weigh_by_average
        )
        if weigh_by_average:
            standard_deviation *= 100

        standard_deviations.append(standard_deviation)

    figure = go.Figure(
        go.Bar(
            x=labels,
            y=standard_deviations,
            name=time_mode.value.capitalize(),
        )
    )

    title_suffix = "weighted by average (%)" if weigh_by_average else "(mm)"
    update_plotly_figure_layout(
        figure,
        title=f"Standard deviations between {begin_year} and {end_year} {title_suffix}",
        xaxis_title=time_mode.value.capitalize()[:-2],
        yaxis_title=f"Standard deviation {title_suffix}",
    )

    return figure


def get_pie_figure_of_years_above_and_below_normal(
    rainfall_instance: Union[
        "models.YearlyRainfall", "models.MonthlyRainfall", "models.SeasonalRainfall"
    ],
    *,
    normal_year: int,
    begin_year: int,
    end_year: int,
    percentages_of_normal: tuple[PositiveFloat, ...] = (
        0,
        80,
        120,
        float("inf"),
    ),
) -> go.Figure | None:
    """
    Return plotly pie figure displaying the percentage of years above and below normal for the given time mode,
    between the given years, and for the normal computed from the given year.

    :param rainfall_instance: An instance of one these 3 classes: [YearlyRainfall, MonthlyRainfall, SeasonalRainfall].
    :param normal_year: An integer representing the year
    to start computing the 30 years normal of the rainfall.
    :param begin_year: An integer representing the year
    to start getting our rainfall values.
    :param end_year: An integer representing the year
    to end getting our rainfall values.
    :param percentages_of_normal: A tuple of floats greater than 0 to decide which slices of normal's percentages
    we display. E.g., if (0, 50, 100, 150, float("inf")) is given, we display years whose rainfall is:
    1. Below 50 % of normal rainfall.
    2. Between 50 and 100 % of normal rainfall.
    3. Between 100 and 150 of normal rainfall.
    4. Above 150 % of normal rainfall.
    Defaults to (0, 80, 120, float("inf")).
    :return: A plotly Figure object of the percentage of years above and below normal as a pie chart.
    None if percentages_of_normal tuple has less than 2 values;
    """
    if len(percentages_of_normal) < 2:
        return None

    sorted_percentages_of_normal = sorted(percentages_of_normal)

    values: list[float] = []
    labels: list[str] = []
    for idx in range(len(sorted_percentages_of_normal) - 1):
        percentage_1 = sorted_percentages_of_normal[idx]
        percentage_2 = sorted_percentages_of_normal[idx + 1]

        values.append(
            rainfall_instance.get_years_between_two_percentages_of_normal(
                normal_year,
                begin_year,
                end_year,
                percentages=(
                    percentage_1,
                    percentage_2,
                ),
            )
        )

        if percentage_1 == 0 and percentage_2 < float("inf"):
            label = f"Years below {percentage_2}% of normal"
        elif percentage_1 > 0 and percentage_2 == float("inf"):
            label = f"Years above {percentage_1}% of normal"
        else:
            label = f"Years between {percentage_1}% and {percentage_2}% of normal"

        labels.append(label)

    figure_title = f"Years compared to {normal_year}-{normal_year + 29} normal between {begin_year} and {end_year}"
    figure_label = "Percentage of years compared to normal"
    if isinstance(rainfall_instance, models.MonthlyRainfall):
        figure_title = f"{figure_title} for {rainfall_instance.month.value}"
        figure_label = f"{figure_label} for {rainfall_instance.month.value}"
    elif isinstance(rainfall_instance, models.SeasonalRainfall):
        figure_title = f"{figure_title} for {rainfall_instance.season.value}"
        figure_label = f"{figure_label} for {rainfall_instance.season.value}"

    figure = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            name=figure_label,
            marker={
                "colors": px.colors.sequential.Blues[::2]
                if len(values) <= 6
                else px.colors.sequential.Blues
            },
            scalegroup="one",
            sort=False,
        ),
    )

    update_plotly_figure_layout(
        figure,
        title=figure_title,
    )

    return figure
