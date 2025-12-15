/**
 * Custom hook for export operations
 */
import { useCallback } from 'react';

import { message } from 'antd';

import { apiService } from '../services/api';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { setExportError, setIsExporting } from '../store/slices/uiSlice';
import { ExportFormat } from '../types/api.types';

export const useExport = () => {
  const dispatch = useAppDispatch();
  const { sessionId } = useAppSelector((state) => state.session);
  const { isExporting } = useAppSelector((state) => state.ui);

  const exportData = useCallback(
    async (format: ExportFormat, width?: number, height?: number) => {
      if (!sessionId) {
        message.error('No session available');
        return;
      }

      dispatch(setIsExporting(true));
      dispatch(setExportError(null));

      try {
        const blob = await apiService.exportData(sessionId, format, width, height);

        const extension = format.toLowerCase();
        const filename = `data_insights_${Date.now()}.${extension}`;

        apiService.downloadFile(blob, filename);
        message.success(`Exported as ${format.toUpperCase()}`);
      } catch (error: any) {
        const errorMessage = error.message || 'Failed to export';
        dispatch(setExportError(errorMessage));
        message.error(errorMessage);
      } finally {
        dispatch(setIsExporting(false));
      }
    },
    [dispatch, sessionId]
  );

  const exportCSV = useCallback(async () => {
    if (!sessionId) {
      message.error('No session available');
      return;
    }

    dispatch(setIsExporting(true));

    try {
      const blob = await apiService.exportCSV(sessionId);
      const filename = `data_insights_${Date.now()}.csv`;
      apiService.downloadFile(blob, filename);
      message.success('Exported as CSV');
    } catch (error: any) {
      message.error(error.message || 'Failed to export CSV');
    } finally {
      dispatch(setIsExporting(false));
    }
  }, [dispatch, sessionId]);

  const exportHTML = useCallback(async () => {
    if (!sessionId) {
      message.error('No session available');
      return;
    }

    dispatch(setIsExporting(true));

    try {
      const blob = await apiService.exportHTML(sessionId);
      const filename = `chart_${Date.now()}.html`;
      apiService.downloadFile(blob, filename);
      message.success('Exported as HTML');
    } catch (error: any) {
      message.error(error.message || 'Failed to export HTML');
    } finally {
      dispatch(setIsExporting(false));
    }
  }, [dispatch, sessionId]);

  return {
    exportData,
    exportCSV,
    exportHTML,
    isExporting,
  };
};
