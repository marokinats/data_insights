"""Export endpoints."""

from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import Response, StreamingResponse

from app.core.exceptions import SessionNotFoundError
from app.models.schemas import (
    ChartConfig,
    ChartType,
    ErrorResponse,
    ExportFormat,
    SeriesData,
)
from app.services.chart_generator import ChartGenerator
from app.services.export_service import ExportService
from app.services.session_manager import session_manager

router = APIRouter()


@router.get(
    "/csv/{session_id}",
    response_class=StreamingResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Session not found"},
    },
)
async def export_csv(session_id: str) -> StreamingResponse:
    """
    Export processed data as CSV file.

    The exported CSV includes:
    - All processed series data
    - Count_Stat column for each series

    Args:
        session_id: Unique session identifier

    Returns:
        CSV file as streaming response

    Raises:
        HTTPException: If session is not found
    """
    try:
        session = session_manager.get_session(session_id)
        session_data = session["data"]

        if not session_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session data not found")

        # Reconstruct data
        series_list = [SeriesData(**s) for s in session_data["series_list"]]

        # Export to CSV
        export_service = ExportService()
        csv_content = export_service.export_to_csv(
            series_list=series_list,
            original_filename=session["filename"],
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data_insights_{timestamp}.csv"

        return StreamingResponse(
            iter([csv_content]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except SessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error exporting CSV: {str(e)}")


@router.get(
    "/{session_id}",
    response_class=Response,
    responses={
        404: {"model": ErrorResponse, "description": "Session not found"},
        400: {"model": ErrorResponse, "description": "Invalid format"},
    },
)
async def export_data(
    session_id: str,
    format: ExportFormat = Query(..., description="Export format (png, pdf, csv)"),
    width: int = Query(1200, ge=400, le=3000, description="Image width (for png/pdf)"),
    height: int = Query(800, ge=300, le=2000, description="Image height (for png/pdf)"),
) -> Response:
    """
    Universal export endpoint supporting PNG, PDF, and CSV formats.

    Args:
        session_id: Unique session identifier
        format: Export format (png, pdf, or csv)
        width: Image width in pixels (for png/pdf)
        height: Image height in pixels (for png/pdf)

    Returns:
        File in requested format

    Raises:
        HTTPException: If session not found or format is invalid
    """
    try:
        session = session_manager.get_session(session_id)
        session_data = session["data"]

        if not session_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session data not found")

        # Reconstruct data
        series_list = [SeriesData(**s) for s in session_data["series_list"]]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == ExportFormat.CSV:
            export_service = ExportService()
            csv_content = export_service.export_to_csv(
                series_list=series_list,
                original_filename=session["filename"],
            )

            filename = f"data_insights_{timestamp}.csv"
            return Response(
                content=csv_content,
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename={filename}"},
            )

        # Generate chart with default config
        config = ChartConfig(
            session_id=session_id,
            chart_type=ChartType.LINE,
            show_legend=True,
        )

        generator = ChartGenerator()
        fig = generator.create_combined_chart(
            series_list=series_list,
            config=config,
        )

        if format == ExportFormat.PDF:
            content = generator.export_to_pdf(fig, width=width, height=height)
            media_type = "application/pdf"
            filename = f"chart_{timestamp}.pdf"
        elif format == ExportFormat.JPEG:
            content = generator.export_to_image(fig, format="jpeg", width=width, height=height)
            media_type = "image/jpeg"
            filename = f"chart_{timestamp}.jpg"
        else:  # PNG
            content = generator.export_to_image(fig, format="png", width=width, height=height)
            media_type = "image/png"
            filename = f"chart_{timestamp}.png"

        return Response(
            content=content, media_type=media_type, headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except SessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error exporting: {str(e)}")


@router.get(
    "/html/{session_id}",
    response_class=Response,
    responses={
        404: {"model": ErrorResponse, "description": "Session not found"},
    },
)
async def export_html(session_id: str) -> Response:
    """
    Export chart as interactive HTML file.

    Args:
        session_id: Unique session identifier

    Returns:
        HTML file
    """
    try:
        session = session_manager.get_session(session_id)
        session_data = session["data"]

        if not session_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session data not found")

        # Reconstruct data
        series_list = [SeriesData(**s) for s in session_data["series_list"]]

        # Generate chart
        config = ChartConfig(
            session_id=session_id,
            chart_type=ChartType.LINE,
            show_legend=True,
        )

        generator = ChartGenerator()
        fig = generator.create_combined_chart(
            series_list=series_list,
            config=config,
        )

        html_content = generator.export_to_html(fig)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chart_{timestamp}.html"

        return Response(
            content=html_content,
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except SessionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
