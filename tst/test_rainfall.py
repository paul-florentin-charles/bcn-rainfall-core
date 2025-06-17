from pathlib import Path
from shutil import rmtree

from bcn_rainfall_core import Rainfall
from bcn_rainfall_core.models import MonthlyRainfall, SeasonalRainfall, YearlyRainfall
from bcn_rainfall_core.utils import Label, Month, Season, TimeMode

RAINFALL = Rainfall.from_config(from_file=True)

normal_year = 1971
begin_year = 1991
end_year = 2020

month = Month.MAY
season = Season.SPRING


class TestRainfall:
    @staticmethod
    def test_export_all_data_to_csv():
        folder_path = ""
        try:
            folder_path = RAINFALL.export_all_data_to_csv(begin_year, end_year)

            assert isinstance(folder_path, str)
            assert Path(folder_path).exists()
        finally:
            if folder_path:
                rmtree(folder_path, ignore_errors=True)

    @staticmethod
    def test_export_as_csv():
        csv_str = RAINFALL.export_as_csv(
            TimeMode.YEARLY, begin_year=begin_year, end_year=end_year
        )

        assert isinstance(csv_str, str)
        lines: list[str] = csv_str.splitlines()
        assert len(lines) == end_year - begin_year + 2  # With header
        assert set(lines[0].split(",")) == {
            f"{Label.YEAR.value}",
            f"{Label.RAINFALL.value}",
        }

        csv_str = RAINFALL.export_as_csv(
            TimeMode.MONTHLY, begin_year=begin_year, end_year=end_year, month=month
        )
        assert isinstance(csv_str, str)

        csv_str = RAINFALL.export_as_csv(
            TimeMode.SEASONAL, begin_year=begin_year, end_year=end_year, season=season
        )
        assert isinstance(csv_str, str)

    @staticmethod
    def test_get_average_rainfall():
        for t_mode in TimeMode:
            avg_rainfall = RAINFALL.get_rainfall_average(
                t_mode,
                begin_year=begin_year,
                end_year=end_year,
                month=month,
                season=season,
            )

            assert isinstance(avg_rainfall, float)

    @staticmethod
    def test_get_normal():
        for t_mode in TimeMode:
            normal = RAINFALL.get_normal(
                t_mode, begin_year=begin_year, month=month, season=season
            )

            assert isinstance(normal, float)

    @staticmethod
    def test_get_years_below_normal():
        for t_mode in TimeMode:
            n_years_below_avg = RAINFALL.get_years_below_normal(
                t_mode,
                normal_year=normal_year,
                begin_year=begin_year,
                end_year=end_year,
                month=month,
                season=season,
            )

            assert isinstance(n_years_below_avg, int)
            assert n_years_below_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_years_above_normal():
        for t_mode in TimeMode:
            n_years_above_avg = RAINFALL.get_years_above_normal(
                t_mode,
                normal_year=normal_year,
                begin_year=begin_year,
                end_year=end_year,
                month=month,
                season=season,
            )

            assert isinstance(n_years_above_avg, int)
            assert n_years_above_avg <= end_year - begin_year + 1

    @staticmethod
    def test_get_last_year():
        assert isinstance(RAINFALL.get_last_year(), int)

    @staticmethod
    def test_get_relative_distance_to_normal():
        for t_mode in TimeMode:
            relative_distance = RAINFALL.get_relative_distance_to_normal(
                t_mode,
                normal_year=normal_year,
                begin_year=begin_year,
                end_year=end_year,
                month=month,
                season=season,
            )

            assert isinstance(relative_distance, float)
            assert -100.0 <= relative_distance

    @staticmethod
    def test_get_standard_deviation():
        for t_mode in TimeMode:
            std = RAINFALL.get_rainfall_standard_deviation(
                t_mode,
                begin_year=begin_year,
                end_year=end_year,
                month=month,
                season=season,
            )

            assert isinstance(std, float)

    @staticmethod
    def test_get_entity_for_time_mode():
        assert isinstance(
            RAINFALL.get_entity_for_time_mode(TimeMode.YEARLY), YearlyRainfall
        )
        assert isinstance(
            RAINFALL.get_entity_for_time_mode(TimeMode.SEASONAL, season=season),
            SeasonalRainfall,
        )
        assert isinstance(
            RAINFALL.get_entity_for_time_mode(TimeMode.MONTHLY, month=month),
            MonthlyRainfall,
        )
        assert RAINFALL.get_entity_for_time_mode("unknown_time_mode") is None
