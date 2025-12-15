"""Chart generation service using Plotly."""

from typing import Any

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.helpers import clean_float_values

from app.models.schemas import ChartConfig, ChartType, SeriesData


class ChartGenerator:
    """Generate charts using Plotly."""

    # Reserved colors for statistics
    STATISTICS_COLORS = {
        "p10": "#FF0000",
        "p50": "#0000FF",
        "p90": "#00FF00",
    }

    SERIES_GRAY_COLOR = "#808080"

    def __init__(self) -> None:
        """Initialize chart generator."""
        self.default_colors = [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ]

    def _get_series_color(self, series: SeriesData, index: int, statistics_shown: bool = False) -> str:
        """
        Get color for series.

        Args:
            series: Series data
            index: Series index for default color
            statistics_shown: Whether any statistics are being shown

        Returns:
            Color hex string
        """
        if statistics_shown:
            return self.SERIES_GRAY_COLOR

        if series.color:
            return series.color
        return self.default_colors[index % len(self.default_colors)]

    def _calculate_cumulative(self, y_values: list[float | None]) -> list[float]:
        """
        Calculate cumulative sum, handling None values.

        Args:
            y_values: Y-axis values

        Returns:
            Cumulative values
        """
        cumulative = []
        current_sum = 0.0

        for value in y_values:
            if value is not None:
                current_sum += value
            cumulative.append(current_sum)

        return cumulative

    def _is_any_statistic_shown(self, config: ChartConfig | None) -> bool:
        """
        Check if any statistic is enabled in config.

        Args:
            config: Chart configuration

        Returns:
            True if any statistic should be shown
        """
        if not config:
            return False

        return config.show_p10 or config.show_p50 or config.show_p90

    def create_line_chart(
        self,
        series_list: list[SeriesData],
        config: ChartConfig | None = None,
        statistics_series: dict[str, tuple[list[float], list[float | None]]] | None = None,
    ) -> go.Figure:
        """
        Create line chart.

        Args:
            series_list: List of series to plot
            config: Chart configuration
            statistics_series: Rowwise statistics data (p10, p50, p90)

        Returns:
            Plotly figure
        """
        fig = go.Figure()

        statistics_shown = self._is_any_statistic_shown(config)

        # Add series traces
        for idx, series in enumerate(series_list):
            if not series.visible:
                continue

            color = self._get_series_color(series, idx, statistics_shown)

            _series_x = []
            _series_y = []
            cleaned_series_x = clean_float_values(series.x_values)
            cleaned_series_y = clean_float_values(series.y_values)
            for x, y in zip(cleaned_series_x, cleaned_series_y):
                if y:
                    _series_x.append(x)
                    _series_y.append(y)

            fig.add_trace(
                go.Scatter(
                    x=_series_x,
                    y=_series_y,
                    mode="lines",
                    name=series.name,
                    type="scatter",
                    line=dict(color=color, width=1),
                    connectgaps=False,
                    hovertemplate=(
                        f"<b>{series.name}</b><br>" "Time: %{x:.2f} days<br>" "Value: %{y:.2f}<br>" "<extra></extra>"
                    ),
                )
            )

        # Add statistics series if provided and requested
        if statistics_series and config:
            self._add_statistics_series(fig, statistics_series, config)

        # Update layout
        self._update_layout(fig, "Line Chart", config)

        return fig

    def create_cumulative_chart(
        self,
        series_list: list[SeriesData],
        config: ChartConfig | None = None,
    ) -> go.Figure:
        """
        Create cumulative chart.

        Args:
            series_list: List of series to plot
            config: Chart configuration


        Returns:
            Plotly figure
        """
        fig = go.Figure()

        statistics_shown = self._is_any_statistic_shown(config)

        # Add cumulative series traces
        for idx, series in enumerate(series_list):
            if not series.visible:
                continue

            color = self._get_series_color(series, idx, statistics_shown)
            cumulative_y = self._calculate_cumulative(series.y_values)

            fig.add_trace(
                go.Scatter(
                    x=series.x_values,
                    y=cumulative_y,
                    mode="lines",
                    name=series.name,
                    line=dict(color=color, width=1),
                    hovertemplate=(
                        f"<b>{series.name}</b><br>"
                        "Time: %{x:.2f} days<br>"
                        "Cumulative: %{y:.2f}<br>"
                        "<extra></extra>"
                    ),
                )
            )

        # Update layout
        self._update_layout(fig, "Cumulative Chart", config)

        return fig

    def _add_statistics_series(
        self,
        fig: go.Figure,
        statistics_series: dict[str, tuple[list[float], list[float | None]]],
        config: ChartConfig,
    ) -> None:
        """
        Add statistical series to chart as separate lines.

        Args:
            fig: Plotly figure
            statistics_series: Dictionary with 'p10', 'p50', 'p90' keys
            config: Chart configuration
        """

        if config.show_p10 and "p10" in statistics_series:
            x_values, y_values = statistics_series["p10"]
            fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode="lines",
                    name="P10",
                    line=dict(color=self.STATISTICS_COLORS["p10"], width=2),
                    connectgaps=False,
                    hovertemplate=("<b>P10</b><br>" "Time: %{x:.2f} days<br>" "P10: %{y:.2f}<br>" "<extra></extra>"),
                )
            )

        if config.show_p50 and "p50" in statistics_series:
            x_values, y_values = statistics_series["p50"]
            fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode="lines",
                    name="P50 (Median)",
                    line=dict(color=self.STATISTICS_COLORS["p50"], width=2),
                    connectgaps=False,
                    hovertemplate=(
                        "<b>P50 (Median)</b><br>" "Time: %{x:.2f} days<br>" "P50: %{y:.2f}<br>" "<extra></extra>"
                    ),
                )
            )

        if config.show_p90 and "p90" in statistics_series:
            x_values, y_values = statistics_series["p90"]
            fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode="lines",
                    name="P90",
                    line=dict(color=self.STATISTICS_COLORS["p90"], width=2),
                    connectgaps=False,
                    hovertemplate=("<b>P90</b><br>" "Time: %{x:.2f} days<br>" "P90: %{y:.2f}<br>" "<extra></extra>"),
                )
            )

    def create_defined_points_chart(
        self,
        time_points: list[float],
        counts: list[int],
    ) -> go.Figure:
        """
        Create chart showing count of defined points over time.

        Args:
            time_points: Time values
            counts: Count of defined points at each time

        Returns:
            Plotly figure
        """
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=time_points,
                y=counts,
                mode="lines",
                name="Defined Points Count",
                line=dict(color="purple", width=1),
                fill="tozeroy",
                fillcolor="rgba(128, 0, 128, 0.2)",
                hovertemplate=("Time: %{x:.2f} days<br>" "Count: %{y}<br>" "<extra></extra>"),
            )
        )

        fig.update_layout(
            title="Count of Defined Data Points Over Time",
            xaxis_title="Time (days)",
            yaxis_title="Count",
            hovermode="x unified",
            template="plotly_white",
        )

        return fig

    def create_combined_chart(
        self,
        series_list: list[SeriesData],
        config: ChartConfig,
        defined_points_data: tuple[list[float], list[int]] | None = None,
        statistics_series: dict[str, tuple[list[float], list[float | None]]] | None = None,
    ) -> go.Figure:
        """
        Create combined chart with main data and optional defined points subplot.

        Args:
            series_list: List of series to plot
            config: Chart configuration
            defined_points_data: Optional tuple of (time_points, counts)
            statistics_series: Rowwise statistics data

        Returns:
            Plotly figure with subplots if needed
        """
        # if need subplots
        if config.show_defined_points and defined_points_data:
            fig = make_subplots(
                rows=2,
                cols=1,
                row_heights=[0.7, 0.3],
                subplot_titles=("Data Series", "Defined Points Count"),
                vertical_spacing=0.1,
            )

            if config.chart_type == ChartType.LINE:
                main_fig = self.create_line_chart(series_list, config, statistics_series)
            else:
                main_fig = self.create_cumulative_chart(series_list, config)

            for trace in main_fig.data:
                fig.add_trace(trace, row=1, col=1)

            # Add defined points chart
            time_points, counts = defined_points_data
            fig.add_trace(
                go.Scatter(
                    x=time_points,
                    y=counts,
                    mode="lines",
                    name="Defined Points",
                    line=dict(color="purple", width=1),
                    fill="tozeroy",
                    fillcolor="rgba(128, 0, 128, 0.2)",
                ),
                row=2,
                col=1,
            )

            fig.update_xaxes(title_text="Time (days)", row=2, col=1)
            fig.update_yaxes(title_text="Value", row=1, col=1)
            fig.update_yaxes(title_text="Count", row=2, col=1)

            fig.update_layout(
                height=800,
                showlegend=config.show_legend,
                hovermode="x unified",
                template="plotly_white",
            )

        else:
            # Single chart
            if config.chart_type == ChartType.LINE:
                fig = self.create_line_chart(series_list, config, statistics_series)
            else:
                fig = self.create_cumulative_chart(series_list, config)

        return fig

    def _update_layout(
        self,
        fig: go.Figure,
        title: str,
        config: ChartConfig | None = None,
    ) -> None:
        """
        Update figure layout.

        Args:
            fig: Plotly figure
            title: Chart title
            config: Chart configuration
        """
        show_legend = config.show_legend if config else True

        fig.update_layout(
            title=dict(text=title),
            xaxis_title=dict(text="Time (days)"),
            yaxis_title=dict(text="Value"),
            hovermode="x unified",
            template="plotly_white",
            showlegend=show_legend,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
            height=600,
            margin=dict(l=50, r=150, t=80, b=50),
        )

    def export_to_json(self, fig: go.Figure) -> Any:
        """
        Export figure to JSON format (for frontend).

        Args:
            fig: Plotly figure

        Returns:
            JSON-serializable dictionary
        """
        return fig.to_dict()

    def export_to_html(self, fig: go.Figure) -> str | Any:
        """
        Export figure to HTML.

        Args:
            fig: Plotly figure

        Returns:
            HTML string
        """
        return fig.to_html(include_plotlyjs="cdn", full_html=True)

    def export_to_image(
        self,
        fig: go.Figure,
        format: str = "png",
        width: int = 1200,
        height: int = 800,
    ) -> bytes | Any:
        """
        Export figure to static image.

        Args:
            fig: Plotly figure
            format: Image format (png, jpeg, svg)
            width: Image width in pixels
            height: Image height in pixels

        Returns:
            Image bytes
        """
        return fig.to_image(
            format=format,
            width=width,
            height=height,
            engine="kaleido",
        )

    def export_to_pdf(
        self,
        fig: go.Figure,
        width: int = 1200,
        height: int = 800,
    ) -> bytes | Any:
        """
        Export figure to PDF.

        Args:
            fig: Plotly figure
            width: PDF width in pixels
            height: PDF height in pixels

        Returns:
            PDF bytes
        """
        return fig.to_image(
            format="pdf",
            width=width,
            height=height,
            engine="kaleido",
        )
