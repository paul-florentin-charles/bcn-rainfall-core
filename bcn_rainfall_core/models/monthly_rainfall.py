"""
Provides a rich class to manipulate Monthly rainfall data.
"""

import pandas as pd
import plotly.graph_objs as go

from bcn_rainfall_core.models.yearly_rainfall import YearlyRainfall
from bcn_rainfall_core.utils import Month


class MonthlyRainfall(YearlyRainfall):
    """
    Provides numerous functions to load, manipulate and export Monthly rainfall data.
    """

    def __init__(
        self,
        raw_data: pd.DataFrame,
        month: Month,
        *,
        start_year: int,
        round_precision: int,
    ):
        self.month = month
        super().__init__(
            raw_data, start_year=start_year, round_precision=round_precision
        )

    def load_yearly_rainfall(self) -> pd.DataFrame:
        """
        Load Yearly Rainfall for instance month variable into pandas DataFrame.

        :return: A pandas DataFrame displaying rainfall data (in mm)
        for instance month according to year.
        """

        return self.load_rainfall(self.month)

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
        Overrides parent method by customizing figure and trace labels.
        """
        return super().get_bar_figure_of_rainfall_according_to_year(
            begin_year,
            end_year,
            figure_label=figure_label
            or f"Rainfall (mm) for {self.month.value} between {begin_year} and {end_year}",
            trace_label=f"{self.month.value} rainfall",
            plot_average=plot_average,
            plot_linear_regression=plot_linear_regression,
        )
