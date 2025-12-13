"""Pydantic schemas for request/response models."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ChartType(str, Enum):
    """Chart type"""

    LINE = "line"
    CUMULATIVE = "cumulative"


class ExportFormat(str, Enum):
    """Export format"""

    PDF = "pdf"
    PNG = "png"
    CSV = "csv"


class SeriesData(BaseModel):
    """Data for a single series."""

    model_config = ConfigDict(frozen=False)

    name: str = Field(..., description="Series name")
    x_values: list[float] = Field(
        ..., description="X-axis values (time in days, months, hours or production in thousands, millions or billions)"
    )
    y_values: list[float | None] = Field(..., description="Y-axis values (measurements)")
    count_stat: list[bool] = Field(..., description="Whether to include in statistics")
    visible: bool = Field(True, description="Whether series is visible")


class ProcessedData(BaseModel):
    """Processed data from CSV."""

    session_id: str = Field(..., description="Unique session identifier")
    series: list[SeriesData] = Field(..., description="List of data series")
    original_filename: str = Field(..., description="Original CSV filename")


class UploadResponse(BaseModel):
    """Response after file upload."""

    session_id: str = Field(..., description="Unique session identifier")
    message: str = Field(..., description="Status message")
    series_count: int = Field(..., description="Number of series found")
    total_rows: int = Field(..., description="Total rows after processing")
    original_filename: str = Field(..., description="Original filename")


class ErrorResponse(BaseModel):
    """Error response."""

    detail: str = Field(..., description="Error message")
    error_code: str | None = Field(None, description="Error code")
