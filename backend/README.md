# Data Insights Backend

FastAPI backend for data processing and visualization.

## Setup

```bash
# Install Poetry if not installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies and activate virtual environment
poetry install
poetry shell
```

## Running

```bash
# Development mode with auto-reload
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
poetry run python -m app.main
```

## Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_main.py -v
```

## Code Quality

```bash
# Format and lint code
poetry run ruff format

# Type checking
poetry run mypy app
```

## API Documentation

Once running, visit:

Swagger UI: http://localhost:8000/api/docs\
ReDoc: http://localhost:8000/api/redoc\
OpenAPI JSON: http://localhost:8000/api/openapi.json
