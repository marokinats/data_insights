/**
 * API Types for Data Insights application
 */

export enum ChartType {
  LINE = 'line',
  CUMULATIVE = 'cumulative',
}

export enum ExportFormat {
  PNG = 'png',
  PDF = 'pdf',
  CSV = 'csv',
  JPEG = 'jpeg',
}

export interface SeriesData {
  name: string;
  x_values: number[];
  y_values: (number | null)[];
  count_stat: boolean[];
  color?: string;
  visible: boolean;
}

export interface StatisticsData {
  p10: number[];
  p50: number[];
  p90: number[];
}

export interface ProcessedData {
  session_id: string;
  series: SeriesData[];
  statistics: StatisticsData;
  original_filename: string;
  created_at: string;
}

export interface SeriesConfig {
  name: string;
  visible: boolean;
  color?: string;
}

export interface ChartConfig {
  session_id: string;
  chart_type: ChartType;
  show_legend: boolean;
  show_defined_points: boolean;
  show_p10: boolean;
  show_p50: boolean;
  show_p90: boolean;
  series_config?: SeriesConfig[];
}

export interface UploadResponse {
  session_id: string;
  message: string;
  series_count: number;
  total_rows: number;
  original_filename: string;
}

export interface ChartResponse {
  chart: any; // Plotly chart data
  config: ChartConfig;
  statistics_colors: {
    p10: string;
    p50: string;
    p90: string;
  };
}

export interface ErrorResponse {
  detail: string;
  error_code?: string;
  timestamp?: string;
}
