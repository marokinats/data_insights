"""Export service for data and charts."""

from io import StringIO
from typing import Any

import pandas as pd

from app.models.schemas import ProcessedData, SeriesData


class ExportService:
    """Handle data export operations."""

    def export_to_csv(
        self,
        series_list: list[SeriesData],
        original_filename: str,
    ) -> str:
        """
        Export processed data to CSV format.

        Args:
            series_list: List of series data
            original_filename: Original filename

        Returns:
            CSV string
        """
        output = StringIO()

        output.write("# Data Insights Export\n")
        output.write(f"# Original file: {original_filename}\n")
        output.write(f"# Number of series: {len(series_list)}\n")
        output.write("#\n")

        data_dict: dict[str, list[Any]] = {}
        max_length = 0

        for series in series_list:
            data_dict[f"{series.name}_X"] = series.x_values
            data_dict[f"{series.name}_Y"] = series.y_values
            data_dict[f"{series.name}_Count_Stat"] = series.count_stat
            max_length = max(max_length, len(series.x_values))

        # Pad shorter series with empty values
        for key in data_dict:
            current_length = len(data_dict[key])
            if current_length < max_length:
                if key.endswith("_Count_Stat"):
                    data_dict[key].extend([False] * (max_length - current_length))
                else:
                    data_dict[key].extend([None] * (max_length - current_length))

        df = pd.DataFrame(data_dict)
        df.to_csv(output, index=False)

        return output.getvalue()

    def export_processed_data_to_dataframe(
        self,
        processed_data: ProcessedData,
    ) -> pd.DataFrame:
        """
        Convert processed data to pandas DataFrame.

        Args:
            processed_data: Processed data object

        Returns:
            DataFrame
        """
        data_dict: dict[str, list[Any]] = {}

        for series in processed_data.series:
            data_dict[f"{series.name}_X"] = series.x_values
            data_dict[f"{series.name}_Y"] = series.y_values
            data_dict[f"{series.name}_Count_Stat"] = series.count_stat

        return pd.DataFrame(data_dict)
