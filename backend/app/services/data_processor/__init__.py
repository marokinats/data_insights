"""Data processing service for CSV files."""

from collections.abc import Sequence
from io import StringIO

import pandas as pd

from app.core.config import settings
from app.core.exceptions import DataProcessingError, FileValidationError
from app.services.data_processor.converters import convert_units
from app.services.data_processor.dto import ProcessedDataType, SeriesPair, XColUnit


class DataProcessor:
    """Process CSV data according to business rules."""

    def __init__(self) -> None:
        """Initialize data processor."""
        self.months_to_days = settings.MONTHS_TO_DAYS_MULTIPLIER
        self.hours_to_days = settings.HOURS_TO_DAYS_DENOMINATOR
        self.kilo_unit = settings.KILO_UNIT
        self.ten_unit = settings.TEN_UNIT

    def validate_csv_structure(self, df: pd.DataFrame) -> None:
        """
        Validate CSV structure.

        Args:
            df: DataFrame to validate

        Raises:
            FileValidationError: If structure is invalid
        """
        if df.empty:
            raise FileValidationError("CSV file is empty")

        # Check if even number of columns (pairs)
        if len(df.columns) % 2 != 0:
            raise FileValidationError("CSV must contain paired columns (X, Y). " f"Found {len(df.columns)} columns.")

        # Check if all columns contain numeric data
        for col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                except Exception:
                    raise FileValidationError(f"Column '{col}' contains non-numeric data")

    def read_csv(self, file: bytes) -> pd.DataFrame:
        """
        Read CSV file.

        Args:
            file_content: CSV file content as bytes

        Returns:
            DataFrame with CSV data

        Raises:
            FileValidationError: If file cannot be read
        """
        try:
            for encoding in ["utf-8", "latin-1", "iso-8859-1"]:
                try:
                    content_str = file.decode(encoding)
                    df = pd.read_csv(StringIO(content_str), header=[0, 1])
                    self.validate_csv_structure(df)
                    return df
                except UnicodeDecodeError:
                    continue

            raise FileValidationError("Unable to decode file with supported encodings")

        except pd.errors.EmptyDataError:
            raise FileValidationError("CSV file is empty")
        except pd.errors.ParserError as e:
            raise FileValidationError(f"CSV parsing error: {str(e)}")
        except Exception as e:
            raise FileValidationError(f"Error reading CSV: {str(e)}")

    def extract_series_pairs_with_units(self, df: pd.DataFrame) -> list[SeriesPair]:
        """
        Extract column pairs (X, Y) from DataFrame.

        Args:
            df: Input DataFrame

        Returns:
            List of tuples (x_col_name, y_col_name, x_col_unit, y_col_unit)
        """
        columns = df.columns.tolist()
        pairs: list[SeriesPair] = []

        for i in range(0, len(columns), 2):
            x_col = columns[i][0]
            y_col = columns[i + 1][0]
            y_col_unit = columns[i + 1][1]

            try:
                x_col_unit = XColUnit(columns[i][1])
            except ValueError:
                raise DataProcessingError(f"Unknown measure: {columns[i][1]}")

            pairs.append(SeriesPair(x_col, y_col, x_col_unit, y_col_unit))

        return pairs

    def process_series(
        self, x_values: pd.Series, y_values: pd.Series, unit: int | None
    ) -> tuple[list[int | None], list[float | None], list[bool]]:
        """
        Process a single series according to business rules:
        1. Remove duplicate rows (same X in nearest row pairs)
        2. Insert empty rows where rows X difference > 1
        3. Mark rows with Count_Stat flag

        Args:
            x_values: X-axis values (time or production volume)
            y_values: Y-axis values (measurements)
            unit: ten_unit counter

        Returns:
            Tuple of (processed_x, processed_y, count_stat)
        """

        x_list = x_values.tolist()
        y_list = y_values.tolist()

        if len(x_list) == 0:
            return [], [], []

        result_x: list[int | None] = []
        result_y: list[float | None] = []
        result_count_stat: list[bool] = []

        i = 0
        while i < len(x_list):
            current_x = x_list[i]
            current_y = y_list[i]

            # Add current row
            result_x.append(current_x)
            result_y.append(current_y)
            if not current_y:
                result_count_stat.append(False)
            else:
                result_count_stat.append(True)

            # Find the next index with a different X (skip duplicates)
            j = i + 1
            while j < len(x_list) and x_list[j] == current_x:
                j += 1

            # Handle gaps between current_x and next_x
            if j < len(x_list):
                next_x = x_list[j]

                x_diff = next_x - current_x if not unit else int((next_x - current_x) / unit)

                if x_diff > 1:
                    # Insert empty rows
                    num_empty_rows = x_diff - 1
                    for k in range(1, num_empty_rows + 1):
                        next_x_value = current_x + k if not unit else current_x + k * unit
                        result_x.append(next_x_value)
                        result_y.append(None)
                        result_count_stat.append(False)

            i = j

        return result_x, result_y, result_count_stat

    def process_raw_dataframe(self, df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
        """
        Process entire DataFrame with all series.

        Args:
            df: Input DataFrame

        Returns:
            Tuple of (processed_df, series_names)
        """
        series_pairs = self.extract_series_pairs_with_units(df)

        # Dictionary to store processed series
        processed_data: dict[str, Sequence[ProcessedDataType] | str] = {}
        series_names = []

        for x_col, y_col, x_col_unit, y_col_unit in series_pairs:
            # Extract series name
            series_name, x_axis_name = x_col.split(" - ")
            axis_name = x_axis_name.removesuffix("X Axis")
            series_names.append(series_name)

            # Get original values
            x_values = df[x_col][x_col_unit]
            y_values = df[y_col][y_col_unit]
            min_len = min(len(x_values), len(y_values))
            x_values = x_values.iloc[:min_len]
            y_values = y_values.iloc[:min_len]

            # Convert
            x_values_converted = convert_units(self, x_values, x_col_unit)
            # Process series
            unit = self.ten_unit if x_col_unit in (XColUnit.MMSCF, XColUnit.MSCF, XColUnit.KSCF, XColUnit.BCF) else None
            proc_x, proc_y, count_stat = self.process_series(x_values_converted, y_values, unit)

            processed_data[f"{series_name}_X"] = proc_x
            processed_data[f"{series_name}_Y"] = proc_y
            processed_data[f"{series_name}_Count_Stat"] = count_stat
            processed_data[f"{series_name}_Axis_Name"] = axis_name

        # Create new DataFrame
        max_len = max(len(v) for v in processed_data.values())
        # Pad all series to same length
        for key in processed_data:
            current_len = len(processed_data[key])
            if current_len < max_len:
                if key.endswith("_X"):
                    additional_x = [0] * (max_len - current_len)
                    processed_data[key] = [*processed_data[key], *additional_x]
                elif key.endswith("_Count_Stat"):
                    additional_stat = [False] * (max_len - current_len)
                    processed_data[key] = [*processed_data[key], *additional_stat]
                else:
                    additional_y = [None] * (max_len - current_len)
                    processed_data[key] = [*processed_data[key], *additional_y]

        processed_df = pd.DataFrame(processed_data)

        return processed_df, series_names

    def get_series_data(self, df: pd.DataFrame, series_name: str) -> tuple[list[float], list[float | None], list[bool]]:
        """
        Extract data for a specific series from processed DataFrame.

        Args:
            df: Processed DataFrame
            series_name: Name of the series

        Returns:
            Tuple of (x_values, y_values, count_stat)
        """
        x_col = f"{series_name}_X"
        y_col = f"{series_name}_Y"
        count_stat_col = f"{series_name}_Count_Stat"

        x_values = df[x_col].tolist()
        y_values = df[y_col].tolist()
        count_stat = df[count_stat_col].tolist()

        # Trim to match x_values length
        y_values = y_values[: len(x_values)]
        count_stat = count_stat[: len(x_values)]

        return x_values, y_values, count_stat
