from enum import Enum
from typing import NamedTuple


class XColUnit(str, Enum):
    """X Axis unit"""

    DAYS = "d"
    HOURS = "hr"
    MONTHS = "mo"
    MMSCF = "MMscf"
    MSCF = "Mscf"
    KSCF = "kscf"
    BCF = "Bcf"


class SeriesPair(NamedTuple):
    x_col: str
    y_col: str
    x_col_unit: XColUnit
    y_col_unit: str


ProcessedDataType = int | float | bool | str | None
