"""Statistics calculation service."""

from typing import Any

import numpy as np

from app.core.exceptions import DataProcessingError


class StatisticsCalculator:
    """Calculate statistical metrics for data series."""

    def calculate_percentiles(self, values: list[float], count_stat: list[bool]) -> dict[str, float]:
        """
        Calculate percentiles (P10, P50, P90) and mean.
        Only includes values where count_stat is True.

        Args:
            values: Y-axis values
            count_stat: Boolean flags indicating which values to include

        Returns:
            Dictionary with p10, p50, p90, mean, and count

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
            "mean": float(np.mean(arr)),
            "count": len(valid_values),
        }

    def calculate_combined_statistics(
        self, all_series_data: list[tuple[list[float], list[float | None], list[bool]]]
    ) -> dict[str, Any]:
        """
        Calculate statistics across all series combined.

        Args:
            all_series_data: List of tuples (x_values, y_values, count_stat) for each series

        Returns:
            Dictionary with combined statistics
        """
        # Combine all valid values from all series
        all_valid_values = []
        total_points = 0

        for _x_values, y_values, count_stat in all_series_data:
            total_points += len([v for v in y_values if v is not None])

            valid_values = [v for v, include in zip(y_values, count_stat) if include and v is not None]
            all_valid_values.extend(valid_values)

        if len(all_valid_values) == 0:
            raise DataProcessingError("No valid data points across all series")

        arr = np.array(all_valid_values, dtype=float)

        return {
            "p10": float(np.percentile(arr, 10)),
            "p50": float(np.percentile(arr, 50)),
            "p90": float(np.percentile(arr, 90)),
            "mean": float(np.mean(arr)),
            "count": len(all_valid_values),
            "total_points": total_points,
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
