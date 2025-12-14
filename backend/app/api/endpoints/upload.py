"""File upload endpoints."""

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.core.exceptions import DataProcessingError, FileValidationError
from app.models.schemas import ErrorResponse, SeriesData, UploadResponse
from app.services.data_processor import DataProcessor
from app.services.session_manager import session_manager
from app.services.statistics_calculator import StatisticsCalculator

router = APIRouter()


@router.post(
    "/",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file"},
        413: {"model": ErrorResponse, "description": "File too large"},
        422: {"model": ErrorResponse, "description": "Processing error"},
    },
)
async def upload_csv(file: UploadFile = File(...)) -> UploadResponse:
    """
    Upload and process CSV file.

    The CSV file should contain paired columns (X, Y) representing time series data.
    - X columns: Month values (will be converted to days)
    - Y columns: Measurement values

    Args:
        file: CSV file to upload

    Returns:
        Upload response with session ID and basic statistics

    Raises:
        HTTPException: If file validation or processing fails
    """

    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename is required")

    file_ext = "." + file.filename.split(".")[-1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}",
        )

    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error reading file: {str(e)}")

    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB",
        )

    # Process data
    try:
        processor = DataProcessor()
        calculator = StatisticsCalculator()
        df = processor.read_csv(content)

        # Process DataFrame
        processed_df, series_names = processor.process_raw_dataframe(df)

        # Extract series data
        all_series_data = []
        series_list: list[SeriesData] = []
        for series_name in series_names:
            x_values, y_values, count_stat = processor.get_series_data(processed_df, series_name)

            all_series_data.append((x_values, y_values, count_stat))
            series_list.append(
                SeriesData(
                    name=series_name,
                    x_values=x_values,
                    y_values=y_values,
                    count_stat=count_stat,
                    visible=True,
                )
            )
        # Calculate statistics
        stats = calculator.calculate_rowwise_statistics(all_series_data)

        session_id = session_manager.create_session(file.filename)
        session_data = {
            "processed_df": processed_df.to_dict(),
            "series_names": series_names,
            "series_list": [s.model_dump() for s in series_list],
            "statistics": stats,
        }
        session_manager.update_session_data(session_id, session_data)

        return UploadResponse(
            session_id=session_id,
            message="File processed successfully",
            series_count=len(series_names),
            total_rows=len(processed_df),
            original_filename=file.filename,
        )

    except FileValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DataProcessingError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")
