import pandas as pd
import plotly.graph_objs as go

from bcn_rainfall_core.utils import (
    Label,
    Month,
    Season,
    TimeMode,
)
from bcn_rainfall_core.utils import (
    plotly_figures as plotly_fig,
)
from tst.models.test_yearly_rainfall import YEARLY_RAINFALL
from tst.test_rainfall import RAINFALL, begin_year, end_year, normal_year


class TestPlotting:
    @staticmethod
    def test_get_figure_of_column_according_to_year():
        bar_fig = plotly_fig.get_figure_of_column_according_to_year(
            YEARLY_RAINFALL.data, Label.RAINFALL
        )

        assert isinstance(bar_fig, go.Figure)

        bar_fig = plotly_fig.get_figure_of_column_according_to_year(
            pd.DataFrame(), Label.RAINFALL
        )

        assert bar_fig is None

        scatter_fig = plotly_fig.get_figure_of_column_according_to_year(
            YEARLY_RAINFALL.data, Label.RAINFALL, figure_type="scatter"
        )

        assert isinstance(scatter_fig, go.Figure)

    @staticmethod
    def test_get_bar_figure_of_rainfall_averages():
        figure = plotly_fig.get_bar_figure_of_rainfall_averages(
            RAINFALL.monthly_rainfalls,
            time_mode=TimeMode.MONTHLY,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

        figure = plotly_fig.get_bar_figure_of_rainfall_averages(
            RAINFALL.seasonal_rainfalls,
            time_mode=TimeMode.SEASONAL,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

    @staticmethod
    def test_get_bar_figure_of_rainfall_linreg_slopes():
        figure = plotly_fig.get_bar_figure_of_rainfall_linreg_slopes(
            RAINFALL.monthly_rainfalls,
            time_mode=TimeMode.MONTHLY,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

        figure = plotly_fig.get_bar_figure_of_rainfall_linreg_slopes(
            RAINFALL.seasonal_rainfalls,
            time_mode=TimeMode.SEASONAL,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

    @staticmethod
    def test_get_bar_figure_of_relative_distances_to_normal():
        figure = plotly_fig.get_bar_figure_of_relative_distances_to_normal(
            RAINFALL.monthly_rainfalls,
            time_mode=TimeMode.MONTHLY,
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

        figure = plotly_fig.get_bar_figure_of_relative_distances_to_normal(
            RAINFALL.seasonal_rainfalls,
            time_mode=TimeMode.SEASONAL,
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

    @staticmethod
    def test_get_bar_figure_of_standard_deviations():
        figure = plotly_fig.get_bar_figure_of_standard_deviations(
            RAINFALL.monthly_rainfalls,
            time_mode=TimeMode.MONTHLY,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

        figure = plotly_fig.get_bar_figure_of_standard_deviations(
            RAINFALL.seasonal_rainfalls,
            time_mode=TimeMode.SEASONAL,
            begin_year=begin_year,
            end_year=end_year,
            weigh_by_average=True,
        )

        assert isinstance(figure, go.Figure)

    @staticmethod
    def test_get_pie_figure_of_years_above_and_below_normal():
        figure = plotly_fig.get_pie_figure_of_years_above_and_below_normal(
            RAINFALL.monthly_rainfalls[Month.SEPTEMBER.value],
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)

        figure = plotly_fig.get_pie_figure_of_years_above_and_below_normal(
            RAINFALL.seasonal_rainfalls[Season.WINTER.value],
            normal_year=normal_year,
            begin_year=begin_year,
            end_year=end_year,
        )

        assert isinstance(figure, go.Figure)
