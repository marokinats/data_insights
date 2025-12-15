/**
 * API Service for Data Insights
 */
import axios, { AxiosError, type AxiosInstance } from 'axios';

import type {
  ChartConfig,
  ChartResponse,
  ErrorResponse,
  ExportFormat,
  ProcessedData,
  UploadResponse,
} from '../types/api.types';
import { API_BASE_URL, API_ENDPOINTS } from './config';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    // Response error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ErrorResponse>) => {
        if (error.response) {
          const errorMessage = error.response.data?.detail || 'An error occurred';
          console.error('API Error:', errorMessage);
          throw new Error(errorMessage);
        } else if (error.request) {
          console.error('Network Error:', error.message);
          throw new Error('Network error. Please check your connection.');
        } else {
          console.error('Error:', error.message);
          throw new Error(error.message);
        }
      }
    );
  }

  /**
   * Upload CSV file
   */
  async uploadCSV(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.client.post<UploadResponse>(API_ENDPOINTS.UPLOAD, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  /**
   * Get processed data for a session
   */
  async getProcessedData(sessionId: string): Promise<ProcessedData> {
    const response = await this.client.get<ProcessedData>(API_ENDPOINTS.DATA(sessionId));
    return response.data;
  }

  /**
   * Generate chart with configuration
   */
  async generateChart(config: ChartConfig): Promise<ChartResponse> {
    const response = await this.client.post<ChartResponse>(API_ENDPOINTS.CHART_GENERATE, config);
    return response.data;
  }

  /**
   * Get chart preview (default settings)
   */
  async getChartPreview(sessionId: string): Promise<ChartResponse> {
    const response = await this.client.get<ChartResponse>(API_ENDPOINTS.CHART_PREVIEW(sessionId));
    return response.data;
  }

  /**
   * Export data/chart
   */
  async exportData(sessionId: string, format: ExportFormat, width?: number, height?: number): Promise<Blob> {
    const params = new URLSearchParams();
    params.append('format', format);
    if (width) params.append('width', width.toString());
    if (height) params.append('height', height.toString());

    const response = await this.client.get(`${API_ENDPOINTS.EXPORT(sessionId)}?${params.toString()}`, {
      responseType: 'blob',
    });

    return response.data;
  }

  /**
   * Export as CSV
   */
  async exportCSV(sessionId: string): Promise<Blob> {
    const response = await this.client.get(API_ENDPOINTS.EXPORT_CSV(sessionId), {
      responseType: 'blob',
    });
    return response.data;
  }

  /**
   * Export as HTML
   */
  async exportHTML(sessionId: string): Promise<Blob> {
    const response = await this.client.get(API_ENDPOINTS.EXPORT_HTML(sessionId), {
      responseType: 'blob',
    });
    return response.data;
  }

  /**
   * Delete session
   */
  async deleteSession(sessionId: string): Promise<void> {
    await this.client.delete(API_ENDPOINTS.SESSION_DELETE(sessionId));
  }

  /**
   * Get session status
   */
  async getSessionStatus(sessionId: string): Promise<any> {
    const response = await this.client.get(API_ENDPOINTS.SESSION_STATUS(sessionId));
    return response.data;
  }

  /**
   * Download file helper
   */
  downloadFile(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }
}

export const apiService = new ApiService();
