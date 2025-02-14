import pandas as pd
import plotly.graph_objs as go
from pytest import raises

from bcn_rainfall_core.models import YearlyRainfall
from bcn_rainfall_core.utils import DataFormatError, Label, Month
from tst.test_config import CONFIG
from tst.test_rainfall import RAINFALL, begin_year, end_year, normal_year

YEARLY_RAINFALL = RAINFALL.yearly_rainfall


class TestYearlyRainfall:
    @staticmethod
    def test_load_yearly_rainfall():
        data = YEARLY_RAINFALL.load_yearly_rainfall()

        assert isinstance(data, pd.DataFrame)

    @staticmethod
    def test_load_rainfall():
        data = YEARLY_RAINFALL.load_rainfall(
            start_month=Month.JUNE, end_month=Month.OCTOBER
        )
        assert isinstance(data, pd.DataFrame)
        assert len(data.columns) == 2
        assert Label.YEAR in data and Label.RAINFALL in data

    @staticmethod
    def test_load_rainfall_fails_because_data_format_error():
        with raises(DataFormatError):
            YearlyRainfall(
                pd.DataFrame(),
                start_year=CONFIG.get_data_settings.start_year,
                round_precision=CONFIG.get_data_settings.rainfall_precision,
            )

    @staticmethod
    def test_get_yearly_rainfall():
        data = YEARLY_RAINFALL.get_yearly_rainfall(begin_year, end_year)

        assert isinstance(data, pd.DataFrame)
        assert len(data) == end_year - begin_year + 1

    @staticmethod
    def test_export_as_csv():
        csv_as_str = YEARLY_RAINFALL.export_as_csv(begin_year, end_year)

        assert isinstance(csv_as_str, str)

    @staticmethod
    def test_get_average_yearly_rainfall():
        avg_rainfall = YEARLY_RAINFALL.get_average_yearly_rainfall(begin_year, end_year)

        assert isinstance(avg_rainfall, float)

    @staticmethod
    def test_get_normal():
        normal = YEARLY_RAINFALL.get_normal(begin_year)

        assert isinstance(normal, float)

    @staticmethod
    def test_get_years_below_percentage_of_normal():
        n_years_below_normal_percentage = (
            YEARLY_RAINFALL.get_years_below_percentage_of_normal(
                normal_year, begin_year, end_year, percentage=75.0
            )
        )

        assert isinstance(n_years_below_normal_percentage, int)
        assert n_years_below_normal_percentage <= end_year - begin_year + 1

    @staticmethod
    def test_get_years_below_normal():
        n_years_below_avg = YEARLY_RAINFALL.get_years_below_normal(
            normal_year, begin_year, end_year
        )

        assert isinstance(n_years_below_avg, int)
        assert n_years_below_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_years_above_percentage_of_normal():
        n_years_above_normal_percentage = (
            YEARLY_RAINFALL.get_years_above_percentage_of_normal(
                normal_year, begin_year, end_year, percentage=125.0
            )
        )

        assert isinstance(n_years_above_normal_percentage, int)
        assert n_years_above_normal_percentage <= end_year - begin_year + 1

    @staticmethod
    def test_get_years_above_normal():
        n_years_above_avg = YEARLY_RAINFALL.get_years_above_normal(
            normal_year, begin_year, end_year
        )

        assert isinstance(n_years_above_avg, int)
        assert n_years_above_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_last_year():
        assert isinstance(YEARLY_RAINFALL.get_last_year(), int)

    @staticmethod
    def test_get_relative_distance_to_normal():
        relative_distance = YEARLY_RAINFALL.get_relative_distance_to_normal(
            normal_year, begin_year, end_year
        )

        assert isinstance(relative_distance, float)
        assert -100.0 <= relative_distance

    @staticmethod
    def test_get_standard_deviation():
        std = YEARLY_RAINFALL.get_standard_deviation(
            YEARLY_RAINFALL.starting_year, YEARLY_RAINFALL.get_last_year()
        )

        assert isinstance(std, float)

        YEARLY_RAINFALL.remove_column(label=Label.SAVITZKY_GOLAY_FILTER)
        std_none = YEARLY_RAINFALL.get_standard_deviation(
            YEARLY_RAINFALL.starting_year,
            YEARLY_RAINFALL.get_last_year(),
            label=Label.SAVITZKY_GOLAY_FILTER,
        )

        assert std_none is None

        std_weighted_by_avg = YEARLY_RAINFALL.get_standard_deviation(
            YEARLY_RAINFALL.starting_year,
            YEARLY_RAINFALL.get_last_year(),
            weigh_by_average=True,
        )

        assert isinstance(std_weighted_by_avg, float)

    @staticmethod
    def test_get_linear_regression():
        (
            (r2_score, slope),
            linear_regression_values,
        ) = YEARLY_RAINFALL.get_linear_regression(begin_year, end_year)

        assert isinstance(r2_score, float) and r2_score <= 1
        assert isinstance(slope, float)
        assert isinstance(linear_regression_values, list)
        assert len(linear_regression_values) == end_year - begin_year + 1

    @staticmethod
    def test_add_percentage_of_normal():
        YEARLY_RAINFALL.add_percentage_of_normal(
            YEARLY_RAINFALL.starting_year, YEARLY_RAINFALL.get_last_year()
        )

        assert Label.PERCENTAGE_OF_NORMAL in YEARLY_RAINFALL.data

        YEARLY_RAINFALL.remove_column(Label.PERCENTAGE_OF_NORMAL)

    @staticmethod
    def test_add_linear_regression():
        YEARLY_RAINFALL.add_linear_regression()

        assert Label.LINEAR_REGRESSION in YEARLY_RAINFALL.data

        YEARLY_RAINFALL.remove_column(Label.LINEAR_REGRESSION)

    @staticmethod
    def test_add_savgol_filter():
        YEARLY_RAINFALL.add_savgol_filter()

        assert Label.SAVITZKY_GOLAY_FILTER in YEARLY_RAINFALL.data

        YEARLY_RAINFALL.remove_column(Label.SAVITZKY_GOLAY_FILTER)

    @staticmethod
    def test_add_kmeans():
        kmeans_clusters = 5
        n_clusters = YEARLY_RAINFALL.add_kmeans(kmeans_clusters)

        assert n_clusters == kmeans_clusters
        assert Label.KMEANS in YEARLY_RAINFALL.data

        YEARLY_RAINFALL.remove_column(Label.KMEANS)

    @staticmethod
    def test_remove_column():
        removed = YEARLY_RAINFALL.remove_column(Label.YEAR)

        assert Label.YEAR in YEARLY_RAINFALL.data.columns
        assert not removed

        YEARLY_RAINFALL.add_savgol_filter()

        removed = YEARLY_RAINFALL.remove_column(Label.SAVITZKY_GOLAY_FILTER)

        assert Label.SAVITZKY_GOLAY_FILTER not in YEARLY_RAINFALL.data.columns
        assert removed

    @staticmethod
    def test_get_various_plotly_figures():
        bar_fig = YEARLY_RAINFALL.get_bar_figure_of_rainfall_according_to_year(
            begin_year, end_year
        )
        assert isinstance(bar_fig, go.Figure)

        scatter_fig = YEARLY_RAINFALL.get_scatter_figure_of_linear_regression(
            begin_year, end_year
        )
        assert isinstance(scatter_fig, go.Figure)

        YEARLY_RAINFALL.add_savgol_filter()

        scatter_fig = YEARLY_RAINFALL.get_scatter_figure_of_savgol_filter()
        assert isinstance(scatter_fig, go.Figure)

        YEARLY_RAINFALL.remove_column(Label.SAVITZKY_GOLAY_FILTER)

    @staticmethod
    def test_get_scatter_figure_of_normal():
        YEARLY_RAINFALL.add_percentage_of_normal(begin_year, end_year)

        figure = YEARLY_RAINFALL.get_scatter_figure_of_normal()
        assert isinstance(figure, go.Figure)

        figure = YEARLY_RAINFALL.get_scatter_figure_of_normal(display_clusters=True)
        assert isinstance(figure, go.Figure)

        YEARLY_RAINFALL.remove_column(Label.PERCENTAGE_OF_NORMAL)
