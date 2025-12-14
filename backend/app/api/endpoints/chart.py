"""Chart generation endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import DataProcessingError, SessionNotFoundError
from app.models.schemas import ChartConfig, ErrorResponse, SeriesData
from app.services.chart_generator import ChartGenerator
from app.services.session_manager import session_manager
from app.services.statistics_calculator import StatisticsCalculator

router = APIRouter()


@router.post(
    "/generate",
    response_model=dict[str, Any],
    responses={
        404: {"model": ErrorResponse, "description": "Session not found"},
        422: {"model": ErrorResponse, "description": "Invalid configuration"},
    },
)
async def generate_chart(config: ChartConfig) -> dict[str, Any]:
    """
    Generate chart with specified configuration.

    Supports multiple statistics lines simultaneously:
    - P10 (red line)
    - P50 (blue line)
    - P90 (green line)

    When any statistic is shown, data series are displayed in gray.
    Statistics are calculated row-by-row across all series.

    Args:
        config: Chart configuration

    Returns:
        Chart data in Plotly JSON format

    Raises:
        HTTPException: If session not found or configuration is invalid
    """
    try:
        session = session_manager.get_session(config.session_id)
        session_data = session["data"]

        if not session_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session data not found")

        # Reconstruct series list
        series_list = [SeriesData(**s) for s in session_data["series_list"]]

        # Apply series configuration if provided
        if config.series_config:
            series_dict = {s.name: s for s in series_list}
            for series_conf in config.series_config:
                if series_conf.name in series_dict:
                    series_dict[series_conf.name].visible = series_conf.visible
                    if series_conf.color:
                        series_dict[series_conf.name].color = series_conf.color

        # Calculate rowwise statistics if any statistic is requested
        if config.show_p10 or config.show_p50 or config.show_p90:
            calculator = StatisticsCalculator()
            all_series_data = [(s.x_values, s.y_values, s.count_stat) for s in series_list if s.visible]

            if all_series_data:
                statistics_series = calculator.calculate_rowwise_statistics(all_series_data)
            else:
                statistics_series = {
                    "p10": ([], []),
                    "p50": ([], []),
                    "p90": ([], []),
                }

        generator = ChartGenerator()

        # Calculate defined points if needed
        defined_points_data = None
        if config.show_defined_points:
            calculator = StatisticsCalculator()
            all_series_data = [(s.x_values, s.y_values, s.count_stat) for s in series_list if s.visible]
            if all_series_data:
                defined_points_data = calculator.calculate_defined_points_count(all_series_data)

        fig = generator.create_combined_chart(
            series_list=series_list,
            config=config,
            defined_points_data=defined_points_data,
            statistics_series=statistics_series,
        )

        # Export to JSON for frontend
        chart_json = generator.export_to_json(fig)

        return {
            "chart": chart_json,
            "config": config.model_dump(),
            "statistics_colors": ChartGenerator.STATISTICS_COLORS,  # for frontend
        }

    except SessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DataProcessingError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        error_detail = f"Error generating chart: {str(e)}"
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)


@router.get(
    "/preview/{session_id}",
    response_model=dict[str, Any],
    responses={
        404: {"model": ErrorResponse, "description": "Session not found"},
    },
)
async def preview_chart(session_id: str) -> dict[str, Any]:
    """
    Generate a preview chart with default settings.

    Args:
        session_id: Session identifier

    Returns:
        Chart data in Plotly JSON format
    """
    # default config
    config = ChartConfig(
        session_id=session_id,
        show_legend=True,
        show_defined_points=False,
        show_p10=False,
        show_p50=False,
        show_p90=False,
    )

    return await generate_chart(config)
