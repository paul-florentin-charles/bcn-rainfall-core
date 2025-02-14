import pandas as pd
import plotly.graph_objs as go
from pytest import raises

from bcn_rainfall_core.models import SeasonalRainfall
from bcn_rainfall_core.utils import DataFormatError, Label, Month, Season
from tst.test_config import CONFIG
from tst.test_rainfall import RAINFALL, begin_year, end_year, normal_year

SEASONAL_RAINFALL = RAINFALL.seasonal_rainfalls[Season.FALL.value]


class TestMonthlyRainfall:
    @staticmethod
    def test_load_yearly_rainfall():
        data = SEASONAL_RAINFALL.load_yearly_rainfall()

        assert isinstance(data, pd.DataFrame)

    @staticmethod
    def test_load_rainfall():
        data = SEASONAL_RAINFALL.load_rainfall(
            start_month=Month.JUNE, end_month=Month.OCTOBER
        )
        assert isinstance(data, pd.DataFrame)
        assert len(data.columns) == 2
        assert Label.YEAR in data and Label.RAINFALL in data

    @staticmethod
    def test_load_rainfall_fails_because_data_format_error():
        with raises(DataFormatError):
            SeasonalRainfall(
                pd.DataFrame(),
                Season.FALL,
                start_year=CONFIG.get_data_settings.start_year,
                round_precision=CONFIG.get_data_settings.rainfall_precision,
            )

    @staticmethod
    def test_get_yearly_rainfall():
        data = SEASONAL_RAINFALL.get_yearly_rainfall(begin_year, end_year)

        assert isinstance(data, pd.DataFrame)
        assert len(data) == end_year - begin_year + 1

    @staticmethod
    def test_export_as_csv():
        csv_as_str = SEASONAL_RAINFALL.export_as_csv(begin_year, end_year)

        assert isinstance(csv_as_str, str)

    @staticmethod
    def test_get_average_yearly_rainfall():
        avg_rainfall = SEASONAL_RAINFALL.get_average_yearly_rainfall(
            begin_year, end_year
        )

        assert isinstance(avg_rainfall, float)

    @staticmethod
    def test_get_normal():
        normal = SEASONAL_RAINFALL.get_normal(begin_year)

        assert isinstance(normal, float)

    @staticmethod
    def test_get_years_below_average():
        n_years_below_avg = SEASONAL_RAINFALL.get_years_below_normal(
            normal_year, begin_year, end_year
        )

        assert isinstance(n_years_below_avg, int)
        assert n_years_below_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_years_above_average():
        n_years_above_avg = SEASONAL_RAINFALL.get_years_above_normal(
            normal_year, begin_year, end_year
        )

        assert isinstance(n_years_above_avg, int)
        assert n_years_above_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_last_year():
        assert isinstance(SEASONAL_RAINFALL.get_last_year(), int)

    @staticmethod
    def test_get_relative_distance_to_normal():
        relative_distance = SEASONAL_RAINFALL.get_relative_distance_to_normal(
            normal_year, begin_year, end_year
        )

        assert isinstance(relative_distance, float)
        assert -100.0 <= relative_distance

    @staticmethod
    def test_get_standard_deviation():
        std = SEASONAL_RAINFALL.get_standard_deviation(
            SEASONAL_RAINFALL.starting_year, SEASONAL_RAINFALL.get_last_year()
        )

        assert isinstance(std, float)

        SEASONAL_RAINFALL.remove_column(label=Label.SAVITZKY_GOLAY_FILTER)
        std_none = SEASONAL_RAINFALL.get_standard_deviation(
            SEASONAL_RAINFALL.starting_year,
            SEASONAL_RAINFALL.get_last_year(),
            label=Label.SAVITZKY_GOLAY_FILTER,
        )

        assert std_none is None

        std_weighted_by_avg = SEASONAL_RAINFALL.get_standard_deviation(
            SEASONAL_RAINFALL.starting_year,
            SEASONAL_RAINFALL.get_last_year(),
            weigh_by_average=True,
        )

        assert isinstance(std_weighted_by_avg, float)

    @staticmethod
    def test_get_linear_regression():
        (
            (r2_score, slope),
            linear_regression_values,
        ) = SEASONAL_RAINFALL.get_linear_regression(begin_year, end_year)

        assert isinstance(r2_score, float) and r2_score <= 1
        assert isinstance(slope, float)
        assert isinstance(linear_regression_values, list)
        assert len(linear_regression_values) == end_year - begin_year + 1

    @staticmethod
    def test_add_percentage_of_normal():
        SEASONAL_RAINFALL.add_percentage_of_normal(
            SEASONAL_RAINFALL.starting_year, SEASONAL_RAINFALL.get_last_year()
        )

        assert Label.PERCENTAGE_OF_NORMAL in SEASONAL_RAINFALL.data

    @staticmethod
    def test_add_linear_regression():
        SEASONAL_RAINFALL.add_linear_regression()

        assert Label.LINEAR_REGRESSION in SEASONAL_RAINFALL.data

    @staticmethod
    def test_add_savgol_filter():
        SEASONAL_RAINFALL.add_savgol_filter()

        assert Label.SAVITZKY_GOLAY_FILTER in SEASONAL_RAINFALL.data

    @staticmethod
    def test_add_kmeans():
        kmeans_clusters = 5
        n_clusters = SEASONAL_RAINFALL.add_kmeans(kmeans_clusters)

        assert n_clusters == kmeans_clusters
        assert Label.KMEANS in SEASONAL_RAINFALL.data

    @staticmethod
    def test_remove_column():
        removed = SEASONAL_RAINFALL.remove_column(Label.YEAR)

        assert Label.YEAR in SEASONAL_RAINFALL.data.columns
        assert not removed

        removed = SEASONAL_RAINFALL.remove_column(Label.SAVITZKY_GOLAY_FILTER)

        assert Label.SAVITZKY_GOLAY_FILTER not in SEASONAL_RAINFALL.data.columns
        assert removed

        SEASONAL_RAINFALL.add_savgol_filter()

    @staticmethod
    def test_get_various_plotly_figures():
        bar_fig = SEASONAL_RAINFALL.get_bar_figure_of_rainfall_according_to_year(
            begin_year, end_year
        )
        assert isinstance(bar_fig, go.Figure)

        scatter_fig = SEASONAL_RAINFALL.get_scatter_figure_of_linear_regression(
            begin_year, end_year
        )
        assert isinstance(scatter_fig, go.Figure)

        scatter_fig = SEASONAL_RAINFALL.get_scatter_figure_of_savgol_filter()
        assert isinstance(scatter_fig, go.Figure)

    @staticmethod
    def test_get_scatter_figure_of_normal():
        figure = SEASONAL_RAINFALL.get_scatter_figure_of_normal()
        assert isinstance(figure, go.Figure)

        figure = SEASONAL_RAINFALL.get_scatter_figure_of_normal(display_clusters=True)
        assert isinstance(figure, go.Figure)
