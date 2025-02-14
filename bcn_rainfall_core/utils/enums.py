"""
Provides various enumerations that inherit from a custom class BaseEnum.
"""

from enum import Enum


class BaseEnum(Enum):
    """
    Same as Enum but with some handy class methods.
    """

    @classmethod
    def names(cls):
        """
        Retrieve all names from an Enum.

        :return: A list made of the Enum names.
        """
        return [enum.name for enum in cls]

    @classmethod
    def values(cls):
        """
        Retrieve all values from an Enum.

        :return: A list made of the Enum values.
        """
        return [enum.value for enum in cls]


class Label(str, BaseEnum):
    """
    An Enum listing labels in DataFrame columns.
    """

    YEAR = "Year"
    RAINFALL = "Rainfall"
    PERCENTAGE_OF_NORMAL = "Percentage of normal"
    LINEAR_REGRESSION = "Linear regression"
    SAVITZKY_GOLAY_FILTER = "Savitzky–Golay filter"
    KMEANS = "K-Means"


class TimeMode(BaseEnum):
    """
    An enum listing time modes (yearly, monthly and seasonal) represented by strings.
    """

    YEARLY = "yearly"
    SEASONAL = "seasonal"
    MONTHLY = "monthly"


class Month(BaseEnum):
    """
    An Enum listing all months: 'January', 'February', ..., 'December'.
    """

    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"

    @classmethod
    def get_month_rank_dict(cls):
        return {
            cls.JANUARY: 1,
            cls.FEBRUARY: 2,
            cls.MARCH: 3,
            cls.APRIL: 4,
            cls.MAY: 5,
            cls.JUNE: 6,
            cls.JULY: 7,
            cls.AUGUST: 8,
            cls.SEPTEMBER: 9,
            cls.OCTOBER: 10,
            cls.NOVEMBER: 11,
            cls.DECEMBER: 12,
        }

    def get_rank(self) -> int:
        return self.get_month_rank_dict()[self]


class Season(BaseEnum):
    """
    An Enum listing all seasons: 'winter', 'spring', 'summer', 'fall'.
    """

    WINTER = "winter"
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"

    @classmethod
    def get_months_by_season_dict(cls):
        return {
            cls.WINTER: [Month.DECEMBER, Month.JANUARY, Month.FEBRUARY],
            cls.SPRING: [Month.MARCH, Month.APRIL, Month.MAY],
            cls.SUMMER: [Month.JUNE, Month.JULY, Month.AUGUST],
            cls.FALL: [Month.SEPTEMBER, Month.OCTOBER, Month.NOVEMBER],
        }

    def get_months(self):
        return self.get_months_by_season_dict()[self]
