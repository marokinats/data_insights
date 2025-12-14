"""Pydantic schemas for request/response models."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChartType(str, Enum):
    """Chart type"""

    LINE = "line"
    CUMULATIVE = "cumulative"


class ExportFormat(str, Enum):
    """Export format"""

    PDF = "pdf"
    PNG = "png"
    JPEG = "jpeg"
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
    visible: bool = Field(default=True, description="Whether series is visible")
    color: str | None = Field(default=None, description="Series color (hex format, e.g., #FF5733)")

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str | None) -> str | None:
        """Validate hex color format."""
        if v is not None and not v.startswith("#"):
            raise ValueError("Color must be in hex format (e.g., #FF5733)")
        return v


class StatisticsData(BaseModel):
    """Statistical calculations."""

    p10: tuple[list[float], list[float | None]] = Field(..., description="10th percentile")
    p50: tuple[list[float], list[float | None]] = Field(..., description="50th percentile (median)")
    p90: tuple[list[float], list[float | None]] = Field(..., description="90th percentile")


class ProcessedData(BaseModel):
    """Processed data from CSV."""

    session_id: str = Field(..., description="Unique session identifier")
    series: list[SeriesData] = Field(..., description="List of data series")
    original_filename: str = Field(..., description="Original CSV filename")
    statistics: StatisticsData = Field(..., description="Calculated statistics")


class SeriesConfig(BaseModel):
    """Configuration for a single series."""

    name: str = Field(..., description="Series name")
    visible: bool = Field(default=True, description="Whether series is visible")
    color: str | None = Field(default=None, description="Series color (hex)")


class ChartConfig(BaseModel):
    """Chart configuration."""

    session_id: str = Field(..., description="Session identifier")
    chart_type: ChartType = Field(default=ChartType.LINE, description="Type of chart (line or cumulative)")
    show_legend: bool = Field(default=True, description="Show legend")
    show_defined_points: bool = Field(default=False, description="Show defined points count graph")
    show_p10: bool = Field(default=False, description="Show P10 line")
    show_p50: bool = Field(default=False, description="Show P50 line (median)")
    show_p90: bool = Field(default=False, description="Show P90 line")
    show_mean: bool = Field(default=False, description="Show mean line")
    series_config: list[SeriesConfig] | None = Field(
        default=None, description="Per-series configuration (visibility, color)"
    )


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
    error_code: str | None = Field(default=None, description="Error code")
