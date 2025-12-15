"""Statistics calculation service."""

import numpy as np

from app.core.exceptions import DataProcessingError


class StatisticsCalculator:
    """Calculate statistical metrics for data series."""

    def calculate_percentiles(self, values: list[float | None], count_stat: list[bool]) -> dict[str, float]:
        """
        Calculate percentiles (P10, P50, P90).
        Only includes values where count_stat is True.

        Args:
            values: Y-axis values
            count_stat: Boolean flags indicating which values to include

        Returns:
            Dictionary with p10, p50, p90 and count

        Raises:
            DataProcessingError: If no valid data points
        """
        # Filter values where count_stat is True and value is not None
        valid_values = [v for v, include in zip(values, count_stat) if include and v is not None]

        if len(valid_values) == 0:
            raise DataProcessingError("No valid data points for statistics calculation")

        arr = np.array(valid_values, dtype=float)

        return {
            "p10": float(np.percentile(arr, 10)),
            "p50": float(np.percentile(arr, 50)),  # median
            "p90": float(np.percentile(arr, 90)),
            "count": len(valid_values),
        }

    def calculate_rowwise_statistics(
        self, all_series_data: list[tuple[list[float], list[float | None], list[bool]]]
    ) -> dict[str, tuple[list[float], list[float | None]]]:
        """
        Calculate statistics row-by-row across all series.

        For each time point (row), calculate P10, P50, P90 across all series
        where count_stat is True.

        Args:
            all_series_data: List of tuples (x_values, y_values, count_stat) for each series

        Returns:
            Dictionary with keys 'p10', 'p50', 'p90', each containing tuple of
            (x_values, y_values) for that statistic line
        """
        if not all_series_data:
            return {
                "p10": ([], []),
                "p50": ([], []),
                "p90": ([], []),
            }

        # Collect all unique X values
        all_x_values = set()
        for x_values, _, _ in all_series_data:
            all_x_values.update(x_values)

        sorted_x_values = sorted(all_x_values)

        # For each X value, collect Y values from all series
        p10_values: list[float | None] = []
        p50_values: list[float | None] = []
        p90_values: list[float | None] = []

        for x in sorted_x_values:
            y_values_at_x = []

            for x_values, y_values, count_stat in all_series_data:
                # Find if this series has data at this X
                try:
                    idx = x_values.index(x)
                    y_val = y_values[idx]
                    count_stat_val = count_stat[idx]

                    if count_stat_val and y_val is not None:
                        y_values_at_x.append(y_val)
                except (ValueError, IndexError):
                    continue

            # Calculate statistics
            if len(y_values_at_x) >= 1:
                y_array = np.array(y_values_at_x, dtype=float)
                p10_values.append(float(np.percentile(y_array, 10)))
                p50_values.append(float(np.percentile(y_array, 50)))
                p90_values.append(float(np.percentile(y_array, 90)))
            else:
                p10_values.append(None)
                p50_values.append(None)
                p90_values.append(None)

        return {
            "p10": (sorted_x_values, p10_values),
            "p50": (sorted_x_values, p50_values),
            "p90": (sorted_x_values, p90_values),
        }

    def calculate_defined_points_count(
        self, all_series_data: list[tuple[list[float], list[float | None], list[bool]]]
    ) -> tuple[list[float], list[int]]:
        """
        Calculate count of defined points (Count_Stat=True) at each time point.

        Args:
            all_series_data: List of tuples (x_values, y_values, count_stat) for each series

        Returns:
            Tuple of (time_points, counts)
        """
        # Collect all time points
        time_point_counts: dict[float, int] = {}

        for x_values, y_values, count_stat in all_series_data:
            for x, y, include in zip(x_values, y_values, count_stat):
                if include and y is not None:
                    time_point_counts[x] = time_point_counts.get(x, 0) + 1

        # Sort by time
        sorted_points = sorted(time_point_counts.items())
        time_points = [x for x, _ in sorted_points]
        counts = [count for _, count in sorted_points]

        return time_points, counts
