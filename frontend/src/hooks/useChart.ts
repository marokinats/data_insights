/**
 * Custom hook for chart operations with Redux
 */
import { useCallback } from 'react';

import { message } from 'antd';

import { useAppDispatch, useAppSelector } from '../store/hooks';
import { generateChart, getChartPreview } from '../store/slices/chartSlice';

export const useChart = () => {
  const dispatch = useAppDispatch();
  const { isGenerating, generateError, chartData } = useAppSelector((state) => state.chart);
  const { sessionId } = useAppSelector((state) => state.session);

  const handleGenerateChart = useCallback(async () => {
    if (!sessionId) {
      message.error('No session available. Please upload a file first.');
      return;
    }
    try {
      await dispatch(generateChart()).unwrap();
      message.success('Chart generated successfully');
    } catch (error: any) {
      message.error(error || 'Failed to generate chart');
    }
  }, [dispatch, sessionId]);

  const handleGetPreview = useCallback(
    async (sessionId: string) => {
      try {
        await dispatch(getChartPreview(sessionId)).unwrap();
        message.success('Preview loaded');
      } catch (error: any) {
        message.error(error || 'Failed to load preview');
      }
    },
    [dispatch]
  );

  return {
    generateChart: handleGenerateChart,
    getPreview: handleGetPreview,
    isGenerating,
    generateError,
    chartData,
  };
};
