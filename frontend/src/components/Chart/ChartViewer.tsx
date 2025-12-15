import React, { useEffect, useMemo, useRef } from 'react';
import Plot from 'react-plotly.js';

import { BarChartOutlined, ExclamationCircleOutlined, LineChartOutlined } from '@ant-design/icons';
import { Alert, Spin } from 'antd';

import { useChart } from '../../hooks/useChart';
import { useAppSelector } from '../../store/hooks';
import './styles.less';

export const ChartViewer: React.FC = () => {
  const { chartData, isGenerating, generateError } = useAppSelector((state) => state.chart);
  const { processedData, sessionId } = useAppSelector((state) => state.session);
  const { generateChart } = useChart();
  const lastGeneratedSessionRef = useRef<string | null>(null);

  // Auto-generate chart when data is loaded
  useEffect(() => {
    if (processedData && !chartData && !isGenerating && sessionId && lastGeneratedSessionRef.current !== sessionId) {
      lastGeneratedSessionRef.current = sessionId;
      generateChart();
    }
  }, [processedData, chartData, isGenerating, generateChart, sessionId]);

  const chartInfo = useMemo(() => {
    if (!chartData || !processedData) return null;

    const visibleSeries = processedData.series.filter((s) => s.visible).length;

    return {
      visibleSeries,
      totalSeries: processedData.series.length,
    };
  }, [chartData, processedData]);

  // Loading state
  if (isGenerating) {
    return (
      <div className="chart-viewer">
        <div className="chart-viewer__container">
          <div className="chart-viewer__loading">
            <Spin size="large" />
            <div className="chart-viewer__loading-text">Generating chart...</div>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (generateError) {
    return (
      <div className="chart-viewer">
        <div className="chart-viewer__container">
          <div className="chart-viewer__error">
            <ExclamationCircleOutlined />
            <div className="chart-viewer__error-text">{generateError}</div>
            <Alert
              message="Chart Generation Failed"
              description="Please try adjusting your settings or upload a different file."
              type="error"
              showIcon
            />
          </div>
        </div>
      </div>
    );
  }

  // Empty state
  if (!chartData) {
    return (
      <div className="chart-viewer">
        <div className="chart-viewer__container">
          <div className="chart-viewer__empty">
            <LineChartOutlined />
            <div className="chart-viewer__empty-text">No Chart Data</div>
            <div className="chart-viewer__empty-hint">
              {processedData ? 'Click "Generate Chart" to visualize your data' : 'Upload a CSV file to get started'}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chart-viewer">
      <div className="chart-viewer__container">
        <div className="chart-viewer__plot">
          <Plot
            data={chartData.data.map((item) => {
              return {
                x: item.x,
                y: item.y,
                type: item.type,
                mode: item.mode,
                name: item.name,
                line: { ...item.line },
              };
            })}
            layout={{
              width: chartData.layout.width,
              height: chartData.layout.height,
              title: { ...chartData.layout.title },
              xaxis: { ...chartData.layout.xaxis },
              yaxis: { ...chartData.layout.yaxis },
              autosize: true,
              margin: { l: 60, r: 150, t: 80, b: 60 },
            }}
            config={{
              responsive: true,
              displayModeBar: true,
              displaylogo: false,
              modeBarButtonsToRemove: ['lasso2d', 'select2d'],
              toImageButtonOptions: {
                format: 'png',
                filename: 'data_insights_chart',
                height: 800,
                width: 1200,
                scale: 2,
              },
            }}
            useResizeHandler={true}
            style={{ width: '100%', height: '100%' }}
          />
        </div>
      </div>

      {chartInfo && (
        <div className="chart-viewer__info">
          <div className="chart-viewer__info-item">
            <BarChartOutlined />
            <span className="chart-viewer__info-item-label">Visible Series:</span>
            <span className="chart-viewer__info-item-value">
              {chartInfo.visibleSeries} / {chartInfo.totalSeries}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};
