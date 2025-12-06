# Data Insights

A web-based application for processing time-series data from CSV files, performing statistical analysis, and generating interactive visualizations.

## Features

- CSV file upload and processing
- Time-series data analysis
- Statistical calculations (P10, P50, P90, Mean)
- Interactive charts (line and cumulative)
- Customizable visualizations
- Export to PDF, PNG, and CSV

## Project Structure
```bash
data_insights/
├── backend/ # Python FastAPI backend
├── frontend/ # React TypeScript frontend
├── docs/ # Documentation
├── .github/ # GitHub Actions workflows
└── docker-compose.yml
```

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- Pandas & NumPy
- Plotly

### Frontend
- React 18+ with TypeScript
- Vite
- Plotly.js
- Ant Design

## Prerequisites

- Python 3.11+
- Node.js 18+
- Poetry
- Docker

## Quick Start

### Backend

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

API will be available at http://localhost:8000\
API docs at http://localhost:8000/api/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:5173

## Testing

### Backend

```bash
cd backend
poetry run pytest
poetry run pytest --cov=app
```

### Frontend

```bash
cd frontend
npm test
```

## Documentation

See docs/ for detailed documentation.

## License

MIT

## Authors

Tania Marokina  💅
