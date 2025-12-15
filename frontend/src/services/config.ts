/**
 * API Configuration
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const API_VERSION = '/api/v1';

export const API_ENDPOINTS = {
  UPLOAD: `${API_VERSION}/upload/`,
  DATA: (sessionId: string) => `${API_VERSION}/data/${sessionId}`,
  CHART_GENERATE: `${API_VERSION}/chart/generate`,
  CHART_PREVIEW: (sessionId: string) => `${API_VERSION}/chart/preview/${sessionId}`,
  EXPORT: (sessionId: string) => `${API_VERSION}/export/${sessionId}`,
  EXPORT_CSV: (sessionId: string) => `${API_VERSION}/export/csv/${sessionId}`,
  EXPORT_HTML: (sessionId: string) => `${API_VERSION}/export/html/${sessionId}`,
  SESSION_DELETE: (sessionId: string) => `${API_VERSION}/session/${sessionId}`,
  SESSION_STATUS: (sessionId: string) => `${API_VERSION}/session/${sessionId}/status`,
} as const;
