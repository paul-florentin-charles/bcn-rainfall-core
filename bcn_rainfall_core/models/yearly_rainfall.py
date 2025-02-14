"""
Provides a rich class to manipulate Yearly Rainfall data.
"""

import operator as opr
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from pydantic import PositiveFloat
from scipy import signal
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import bcn_rainfall_core.utils.dataframe_operations as df_ops
import bcn_rainfall_core.utils.plotly_figures as plotly_fig
import bcn_rainfall_core.utils.rainfall_metrics as rain
from bcn_rainfall_core.utils import DataFormatError, Label, Month


class YearlyRainfall:
    """
    Provides numerous functions to load, manipulate and export Yearly Rainfall data.
    """

    def __init__(
        self,
        raw_data: pd.DataFrame,
        *,
        start_year: int,
        round_precision: int,
    ):
        self.raw_data = raw_data
        self.starting_year = start_year
        self.round_precision = round_precision
        self.data = self.load_yearly_rainfall()

    def __str__(self):
        return self.data.to_string()

    def load_yearly_rainfall(self) -> pd.DataFrame:
        """
        Load Yearly Rainfall into pandas DataFrame.

        :return: A pandas DataFrame displaying rainfall data (in mm) according to year.
        """

        return self.load_rainfall(Month.JANUARY, Month.DECEMBER)

    def load_rainfall(
        self, start_month: Month, end_month: Month | None = None
    ) -> pd.DataFrame:
        """
        Generic function to load Yearly Rainfall data from raw data stored in pandas DataFrame.
        Raw data has to be shaped as rainfall values for each month according to year.

        :param start_month: A Month Enum representing the month
        to start getting our rainfall values.
        :param end_month: A Month Enum representing the month
        to end getting our rainfall values (optional).
        If not given, we load rainfall data only for given start_month.
        :return: A pandas DataFrame displaying rainfall data (in mm) according to year.
        :raise DataFormatError: If raw_data attribute of instance doesn't have exactly 13 columns.
        1 for the year; 12 for every monthly rainfall.
        """
        if not isinstance(self.raw_data, pd.DataFrame) or len(
            self.raw_data.columns
        ) != 1 + len(Month):
            raise DataFormatError(
                "[Year, Jan_rain, Feb_rain, ..., Dec_rain] (pandas DataFrame)"
            )

        return df_ops.retrieve_rainfall_data_with_constraints(
            self.raw_data,
            starting_year=self.starting_year,
            round_precision=self.round_precision,
            start_month=start_month.get_rank(),
            end_month=end_month.get_rank() if end_month else None,
        )

    def get_yearly_rainfall(self, begin_year: int, end_year: int) -> pd.DataFrame:
        """
        Retrieves Yearly Rainfall within a specific year range.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :return: A pandas DataFrame displaying rainfall data (in mm)
        for instance month according to year.
        """

        return df_ops.get_rainfall_within_year_interval(
            self.data, begin_year=begin_year, end_year=end_year
        )

    def export_as_csv(
        self,
        begin_year: int,
        end_year: int,
        *,
        path: str | Path | None = None,
    ) -> str | None:
        """
        Export the actual instance data state as a CSV.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :param path: path to csv file to save our data (optional).
        :return: CSV data as a string if no path is set.
        None otherwise.
        """

        return self.get_yearly_rainfall(begin_year, end_year).to_csv(
            path_or_buf=path, index=False
        )

    def get_average_yearly_rainfall(self, begin_year: int, end_year: int) -> float:
        """
        Computes Rainfall average for a specific year range.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :return: A float representing the average Rainfall.
        """

        return rain.get_average_rainfall(
            self.get_yearly_rainfall(begin_year, end_year),
            round_precision=self.round_precision,
        )

    def get_normal(self, begin_year: int) -> float:
        """
        Computes Rainfall average over 30 years time frame.

        :param begin_year: An integer representing the year
        to start from to compute our normal.
        :return: A float storing the normal.
        """

        return rain.get_normal(
            self.data, begin_year, round_precision=self.round_precision
        )

    def get_years_below_percentage_of_normal(
        self,
        normal_year: int,
        begin_year: int,
        end_year: int,
        *,
        percentage: PositiveFloat,
    ) -> int:
        """
        Computes the count of years within a specific year range that are below
        the percentage of a rainfall normal computed from a given normal year.

        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :param percentage: The percentage of the rainfall normal
        to compare against.

        :return: The count of years that are below the percentage of the rainfall normal.
        """

        return rain.get_years_compared_to_given_rainfall_value(
            self.get_yearly_rainfall(begin_year, end_year),
            rain.get_normal(self.data, normal_year) * percentage / 100,
            comparator=opr.lt,
        )

    def get_years_below_normal(
        self, normal_year: int, begin_year: int, end_year: int
    ) -> int:
        """
        Computes the number of years below normal for a specific year range.

        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :return: The number of years below the normal as an integer.
        """

        return self.get_years_below_percentage_of_normal(
            normal_year, begin_year, end_year, percentage=100
        )

    def get_years_above_percentage_of_normal(
        self,
        normal_year: int,
        begin_year: int,
        end_year: int,
        *,
        percentage: PositiveFloat,
    ) -> int:
        """
        Computes the count of years within a specific year range that are above
        the percentage of a rainfall normal computed from a given normal year.

        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :param percentage: The percentage of the rainfall normal
        to compare against.

        :return: The count of years that are above the percentage of the rainfall normal.
        """

        return rain.get_years_compared_to_given_rainfall_value(
            self.get_yearly_rainfall(begin_year, end_year),
            rain.get_normal(self.data, normal_year) * percentage / 100,
            comparator=opr.gt,
        )

    def get_years_above_normal(
        self, normal_year: int, begin_year: int, end_year: int
    ) -> int:
        """
        Computes the number of years above normal for a specific year range.

        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :return: The number of years above the normal as an integer.
        """

        return self.get_years_above_percentage_of_normal(
            normal_year, begin_year, end_year, percentage=100
        )

    def get_last_year(self) -> int:
        """
        Retrieves the last element of the 'Year' column from the pandas DataFrame.

        :return: The ultimate year of DataFrame.
        """

        return int(self.data[Label.YEAR].iloc[-1])

    def get_relative_distance_to_normal(
        self, normal_year: int, begin_year: int, end_year: int
    ) -> float | None:
        """
        Computes the relative distance between average rainfall within two given years
        and normal rainfall computed from a specific year.

        :param normal_year: An integer representing the year
        to start computing the 30 years normal of the rainfall.
        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :return: The relative distance as a float.
        """
        gap = end_year - begin_year + 1
        if gap <= 0:
            return None

        normal = self.get_normal(normal_year)
        average = self.get_average_yearly_rainfall(begin_year, end_year)

        return round(
            (average - normal) / normal * 100,
            self.round_precision,
        )

    def get_standard_deviation(
        self,
        begin_year: int,
        end_year: int,
        *,
        label: Label | None = Label.RAINFALL,
        weigh_by_average=False,
    ) -> float | None:
        """
        Compute the standard deviation of a column specified by its label within DataFrame
        and for an optional time range.
        By default, it uses the 'Rainfall' column.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :param label: A string corresponding to an existing column label (optional).
        :param bool weigh_by_average: whether to divide standard deviation by average or not (optional).
        Defaults to False.
        :return: The standard deviation as a float.
        Nothing if the specified column does not exist.
        """
        if label not in self.data.columns:
            return None

        data = self.get_yearly_rainfall(begin_year, end_year)[label]

        standard_deviation = data.std()
        if weigh_by_average:
            standard_deviation /= data.mean()

        return round(
            standard_deviation,
            self.round_precision,
        )

    def get_linear_regression(
        self, begin_year: int, end_year: int
    ) -> tuple[tuple[float, float], list[float]]:
        """
        Computes Linear Regression of rainfall according to year for a given time interval.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        If not given, defaults to latest year available.
        :return: a tuple containing a tuple of floats (r2 score, slope)
        and a list of rainfall values computed by the linear regression.
        """
        data = self.get_yearly_rainfall(begin_year, end_year)

        years = data[Label.YEAR.value].values.reshape(-1, 1)  # type: ignore
        rainfalls = data[Label.RAINFALL.value].values

        lin_reg = LinearRegression()
        lin_reg.fit(years, rainfalls)
        predicted_rainfalls: list[float] = [
            round(rainfall_value, self.round_precision)
            for rainfall_value in lin_reg.predict(years).tolist()
        ]

        return (
            r2_score(rainfalls, predicted_rainfalls),
            round(lin_reg.coef_[0], self.round_precision),
        ), predicted_rainfalls

    def add_percentage_of_normal(self, begin_year: int, end_year: int) -> None:
        """
        Add the percentage of rainfall compared with normal
        to our pandas DataFrame for a specific year range.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :return: None
        """
        normal = self.get_average_yearly_rainfall(begin_year, end_year)
        if normal == 0.0:
            return None

        self.data[Label.PERCENTAGE_OF_NORMAL.value] = round(
            self.data[Label.RAINFALL.value] / normal * 100.0, self.round_precision
        )

    def add_linear_regression(self) -> tuple[float, float]:
        """
        Compute and add Linear Regression of Rainfall according to Year
        to our pandas DataFrame.

        :return: a tuple containing two floats (r2 score, slope).
        """
        years = self.data[Label.YEAR.value].values.reshape(-1, 1)  # type: ignore
        rainfalls = self.data[Label.RAINFALL.value].values

        reg = LinearRegression()
        reg.fit(years, rainfalls)
        self.data[Label.LINEAR_REGRESSION.value] = reg.predict(years)
        self.data[Label.LINEAR_REGRESSION.value] = round(
            self.data[Label.LINEAR_REGRESSION.value], self.round_precision
        )

        return r2_score(
            rainfalls, self.data[Label.LINEAR_REGRESSION.value].values
        ), round(reg.coef_[0], self.round_precision)

    def add_savgol_filter(self) -> None:
        """
        Compute and add Savitzky–Golay filter to Rainfall according to Year
        to our pandas DataFrame.

        :return: None
        """
        self.data[Label.SAVITZKY_GOLAY_FILTER.value] = signal.savgol_filter(
            self.data[Label.RAINFALL.value],
            window_length=len(self.data),
            polyorder=len(self.data) // 10,
        )

        self.data[Label.SAVITZKY_GOLAY_FILTER.value] = round(
            self.data[Label.SAVITZKY_GOLAY_FILTER.value], self.round_precision
        )

    def add_kmeans(self, kmeans_clusters=4) -> int:
        """
        Compute and add K-Mean clustering of Rainfall according to Year
        to our pandas DataFrame.

        :param kmeans_clusters: The number of clusters to compute. Defaults to 4.
        :return: The number of computed clusters as an integer
        """
        fit_data: np.ndarray = self.data[
            [Label.YEAR.value, Label.RAINFALL.value]
        ].values

        kmeans = KMeans(n_init=10, n_clusters=kmeans_clusters)
        kmeans.fit(fit_data)
        self.data[Label.KMEANS.value] = kmeans.predict(fit_data)

        return kmeans.n_clusters

    def remove_column(self, label: Label) -> bool:
        """
        Remove a column for DataFrame using its label.
        Removing 'Year' or 'Rainfall' columns is prevented.

        :param label: A string corresponding to an existing column label.
        :return: A boolean set to whether the operation passed or not.
        """

        return df_ops.remove_column(self.data, label=label)

    def get_bar_figure_of_rainfall_according_to_year(
        self,
        begin_year: int,
        end_year: int,
        *,
        figure_label: str | None = None,
        trace_label: str | None = None,
        plot_average=False,
        plot_linear_regression=False,
    ) -> go.Figure | None:
        """
        Return bar figure of Rainfall data according to year.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :param figure_label: A string to label graphic data (optional).
        If not set or set to "", label value is used.
        :param trace_label: A string to label trace data (optional).
        If not set or set to "", label value is used.
        :param plot_average: Whether to plot average rainfall as a horizontal line or not.
        Defaults to False.
        :param plot_linear_regression: Whether to plot linear regression of rainfall or not.
        Defaults to False.
        :return: A plotly Figure object if data has been successfully plotted, None otherwise.
        """
        yearly_rainfall = self.get_yearly_rainfall(begin_year, end_year)

        figure = plotly_fig.get_figure_of_column_according_to_year(
            yearly_rainfall,
            label=Label.RAINFALL,
            figure_type="bar",
            figure_label=figure_label
            or f"Rainfall (mm) between {begin_year} and {end_year}",
            trace_label=trace_label,
        )
        if figure:
            if plot_average:
                average_rainfall = self.get_average_yearly_rainfall(
                    begin_year, end_year
                )

                figure.add_trace(
                    go.Scatter(
                        x=yearly_rainfall[Label.YEAR.value],
                        y=[average_rainfall] * len(yearly_rainfall),
                        name="Average rainfall",
                    )
                )

            if plot_linear_regression:
                (
                    (r2, slope),
                    linear_regression_values,
                ) = self.get_linear_regression(begin_year, end_year)

                figure.add_trace(
                    go.Scatter(
                        x=yearly_rainfall[Label.YEAR.value],
                        y=linear_regression_values,
                        name=f"{Label.LINEAR_REGRESSION.value}"
                        f"<br><i>R2 score:</i> <b>{round(r2, 2)}</b>"
                        f"<br><i>slope:</i> {slope} mm/year",
                    )
                )

            figure.update_yaxes(title_text=f"{Label.RAINFALL.value} (mm)")

        return figure

    def get_scatter_figure_of_linear_regression(
        self,
        begin_year: int,
        end_year: int,
    ) -> go.Figure | None:
        """
        Return plotly figure with scatter trace of rainfall linear regression according to year.

        :param begin_year: An integer representing the year
        to start getting our rainfall values.
        :param end_year: An integer representing the year
        to end getting our rainfall values.
        :return: A plotly Figure object if data has been successfully plotted, None otherwise.
        """
        (r2, slope), predicted_rainfalls = self.get_linear_regression(
            begin_year, end_year
        )

        yearly_rainfall = self.get_yearly_rainfall(begin_year, end_year)
        yearly_rainfall[Label.LINEAR_REGRESSION.value] = predicted_rainfalls

        figure = plotly_fig.get_figure_of_column_according_to_year(
            yearly_rainfall,
            Label.LINEAR_REGRESSION,
            figure_type="scatter",
            figure_label=f"{Label.LINEAR_REGRESSION.value}"
            f"<br><i>R2 score:</i> <b>{round(r2, 2)}</b>"
            f"<br><i>slope:</i> {slope} mm/year",
        )

        return figure

    def get_scatter_figure_of_savgol_filter(self) -> go.Figure | None:
        """
        Return plotly figure with scatter trace of Savitzky-Golay filter according to year.

        :return: A plotly Figure object if data has been successfully plotted, None otherwise.
        """

        return plotly_fig.get_figure_of_column_according_to_year(
            self.data,
            Label.SAVITZKY_GOLAY_FILTER,
            figure_type="scatter",
            figure_label=f"{Label.SAVITZKY_GOLAY_FILTER.value} (mm)",
        )

    def get_scatter_figure_of_normal(self, display_clusters=False) -> go.Figure | None:
        """
        Return plotly figure with horizontal line of normal rainfall according to year and scatter rainfall values.

        :param display_clusters: Whether to display clusters computed with k-means or not.
        Defaults to False (optional).
        :return: A plotly Figure object if data has been successfully plotted, None otherwise.
        """

        figure = go.Figure(
            go.Scatter(
                x=self.data[Label.YEAR.value],
                y=[100.0] * len(self.data),
                name="Normal rainfall (%)",
            )
        )

        if not display_clusters:
            if fig_normal := plotly_fig.get_figure_of_column_according_to_year(
                self.data, Label.PERCENTAGE_OF_NORMAL, figure_type="scatter"
            ):
                figure.add_traces(list(fig_normal.select_traces()))
            else:
                return None
        else:
            for label_value in range(rain.get_clusters_number(self.data)):
                if (
                    fig_normal_kmeans_subplot
                    := plotly_fig.get_figure_of_column_according_to_year(
                        self.data[self.data[Label.KMEANS.value] == label_value],
                        Label.PERCENTAGE_OF_NORMAL,
                        figure_type="scatter",
                    )
                ):
                    figure.add_traces(list(fig_normal_kmeans_subplot.select_traces()))
                else:
                    return None

        return figure
