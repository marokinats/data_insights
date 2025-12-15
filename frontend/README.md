# Data Insights Frontend

Frontend of the Data Insights project.\
This is a modern React application built with TypeScript and Vite, designed for visualizing and analyzing time series data from CSV files.

## Features

- **Fast CSV Upload**: Convenient drag-and-drop interface for file uploads.
- **Interactive Charts**: Data visualization using Plotly.js with zoom, pan, and hover details.
- **Flexible Configuration**: Control panel for switching chart types (line, cumulative), displaying statistics, and managing series visibility.
- **Statistics Visualization**: Display P10, P50 (median), and P90 as separate series on the chart for detailed analysis.
- **Data Export**: Export charts (PNG, PDF) and processed data (CSV).
- **Responsive Design**: Proper display across various devices.
- **Modern State Management**: Centralized state management using Redux Toolkit.

## Tech Stack

- **Framework**: [React 18](https://reactjs.org/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **State Management**: [Redux Toolkit](https://redux-toolkit.js.org/)
- **UI Library**: [Ant Design](https://ant.design/)
- **Charts**: [Plotly.js](https://plotly.com/javascript/) & [react-plotly.js](https://github.com/plotly/react-plotly.js)
- **Styling**: [LESS](https://lesscss.org/) with BEM methodology
- **HTTP Client**: [Axios](https://axios-http.com/)
- **Code Quality**: [ESLint](https://eslint.org/) & [Prettier](https://prettier.io/)

## Getting Started

### Prerequisites

1. Installed [Node.js](https://nodejs.org/) (recommended version v20+).
2. Installed package manager `npm` or `yarn`.
3. **Running backend server**. The frontend sends requests to `http://localhost:8000/api`.

### Installation

```bash
# Navigate to the frontend directory
cd frontend
# Install all dependencies
npm install
```

### Development Mode

Ensure the backend server is running.

```bash
# Start the frontend dev server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Available Scripts

| Command                | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| `npm run dev`          | Starts the dev server with hot-reload.                         |
| `npm run build`        | Builds the application for production to the `dist` directory. |
| `npm run preview`      | Starts a local server to preview the production build.         |
| `npm run lint`         | Checks code with ESLint for compliance with standards.         |
| `npm run lint:fix`     | Automatically fixes errors found by ESLint.                    |
| `npm run format`       | Formats all code using Prettier.                               |
| `npm run format:check` | Checks formatting without making changes.                      |
| `npm run type-check`   | Checks TypeScript types without compilation.                   |

## State Management (Redux)

Application state is managed using **Redux Toolkit**. Logic is divided into three main "slices":

- **`sessionSlice.ts`**: Manages session state, including `sessionId`, loaded and processed data (`processedData`), and loading statuses.
- **`chartSlice.ts`**: Manages chart state, including Plotly data (`chartData`), current configuration (`chartConfig`), and settings (`settings`).
- **`uiSlice.ts`**: Manages UI state, such as export statuses, global errors, and other UI elements.

To interact with the Redux store, use typed hooks from `src/store/hooks.ts`:

- `useAppSelector`: For retrieving data from the store.
- `useAppDispatch`: For dispatching actions and thunks.

## Styling (LESS)

Project styling is implemented using the **LESS** preprocessor.

## Code Quality

- **ESLint** is used for static code analysis and problem detection.
- **Prettier** handles automatic code formatting to ensure a consistent style.
- **Pre-commit Hooks** automatically run `prettier`, `eslint`, and `tsc` before each commit to guarantee high code quality in the repository.

## API Integration

The frontend communicates with the backend through a set of RESTful endpoints. All API calls are handled by the `ApiService` class in `src/services/api.ts`.

## Testing

```bash
npm test
```

---

For more detailed information about the backend, deployment, or overall architecture, please refer to the backend documentation and main project documentation.
