from bcn_rainfall_core.utils import BaseEnum, Label, Month, Season, TimeMode


def test_base_enum():
    class TestEnum(BaseEnum):
        FOX = 0
        DOG = 1
        CAT = 2

    assert set(TestEnum.names()) == {"FOX", "DOG", "CAT"}
    assert set(TestEnum.values()) == {0, 1, 2}


def test_labels():
    for label in Label:
        assert isinstance(label.value, str)


def test_time_modes():
    assert len(TimeMode) == 3

    for t_mode in TimeMode.values():
        assert isinstance(t_mode, str)


class TestMonths:
    @staticmethod
    def test_months_count():
        assert len(Month) == 12

    @staticmethod
    def test_january():
        month = Month.JANUARY

        assert isinstance(month.value, str)
        assert month.value == "January"

    @staticmethod
    def test_february():
        month = Month.FEBRUARY

        assert isinstance(month.value, str)
        assert month.value == "February"

    @staticmethod
    def test_march():
        month = Month.MARCH

        assert isinstance(month.value, str)
        assert month.value == "March"

    @staticmethod
    def test_april():
        month = Month.APRIL

        assert isinstance(month.value, str)
        assert month.value == "April"

    @staticmethod
    def test_may():
        month = Month.MAY

        assert isinstance(month.value, str)
        assert month.value == "May"

    @staticmethod
    def test_june():
        month = Month.JUNE

        assert isinstance(month.value, str)
        assert month.value == "June"

    @staticmethod
    def test_july():
        month = Month.JULY

        assert isinstance(month.value, str)
        assert month.value == "July"

    @staticmethod
    def test_august():
        month = Month.AUGUST

        assert isinstance(month.value, str)
        assert month.value == "August"

    @staticmethod
    def test_september():
        month = Month.SEPTEMBER

        assert isinstance(month.value, str)
        assert month.value == "September"

    @staticmethod
    def test_october():
        month = Month.OCTOBER

        assert isinstance(month.value, str)
        assert month.value == "October"

    @staticmethod
    def test_november():
        month = Month.NOVEMBER

        assert isinstance(month.value, str)
        assert month.value == "November"

    @staticmethod
    def test_december():
        month = Month.DECEMBER

        assert isinstance(month.value, str)
        assert month.value == "December"


class TestSeasons:
    @staticmethod
    def test_seasons_count():
        assert len(Season) == 4

    @staticmethod
    def test_winter():
        season = Season.WINTER

        assert isinstance(season.value, str)
        assert season.value == "winter"

    @staticmethod
    def test_spring():
        season = Season.SPRING

        assert isinstance(season.value, str)
        assert season.value == "spring"

    @staticmethod
    def test_summer():
        season = Season.SUMMER

        assert isinstance(season.value, str)
        assert season.value == "summer"

    @staticmethod
    def test_fall():
        season = Season.FALL

        assert isinstance(season.value, str)
        assert season.value == "fall"
