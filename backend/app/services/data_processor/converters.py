from typing import TYPE_CHECKING

import pandas as pd

from app.services.data_processor.dto import XColUnit

if TYPE_CHECKING:
    from app.services.data_processor import DataProcessor

TRUNC_SHIFT = 0.00001


def convert_to_int(values: pd.Series) -> "pd.Series[int]":
    """
    Convert numeric days to integer type days.

    Args:
        days: Series with days values

    Returns:
        Series with integer type day values
    """
    return (values + TRUNC_SHIFT).round().astype(int)


def convert_hours_to_int_days(handler: "DataProcessor", hours: pd.Series) -> pd.Series:
    """
    Convert hours to integer type days.

    Args:
        handler:  class DataProcessor
        hours: Series with hours values

    Returns:
        Series with integer type day values
    """
    return hours / handler.hours_to_days


def convert_months_to_int_days(handler: "DataProcessor", months: pd.Series) -> pd.Series:
    """
    Convert months to integer type days.

    Args:
        handler:  class DataProcessor
        months: Series with month values

    Returns:
        Series with integer type day values
    """
    return months * handler.months_to_days


def convert_to_ten_units(handler: "DataProcessor", values: pd.Series) -> "pd.Series[int]":
    """
    Convert numeric values to integer type units.

    Args:
        handler:  class DataProcessor
        values: Series with numeric values

    Returns:
        Series with integer type 10 based units
    """
    return ((values / handler.ten_unit).round() * handler.ten_unit).astype(int)


def convert_thousands_to_millions(handler: "DataProcessor", values: pd.Series) -> "pd.Series[float]":
    """
    Convert values in the thousands to values in the millions

    Args:
        handler:  class DataProcessor
        values: Series with numeric values in the thousands

    Returns:
        Series with numeric values in the millions
    """
    return values / handler.kilo_unit


def convert_billions_to_millions(handler: "DataProcessor", values: pd.Series) -> "pd.Series[float]":
    """
    Convert values in the billions to values in the millions

    Args:
        handler:  class DataProcessor
        values: Series with numeric values in the billions

    Returns:
        Series with numeric values in the millions
    """
    return values * handler.kilo_unit


def convert_units(handler: "DataProcessor", values: pd.Series, current_series_unit: XColUnit) -> "pd.Series[int]":
    match current_series_unit:
        case XColUnit.DAYS:
            return convert_to_int(values)
        case XColUnit.HOURS:
            return convert_to_int(convert_hours_to_int_days(handler, values))
        case XColUnit.MONTHS:
            return convert_to_int(convert_months_to_int_days(handler, values))
        case XColUnit.MMSCF:
            return convert_to_ten_units(handler, values)
        case XColUnit.MSCF:
            return convert_to_ten_units(handler, convert_thousands_to_millions(handler, values))
        case XColUnit.KSCF:
            return convert_to_ten_units(handler, convert_thousands_to_millions(handler, values))
        case XColUnit.BCF:
            return convert_to_ten_units(handler, convert_billions_to_millions(handler, values))
        case _:
            return convert_to_int(values)
