import React from 'react';

import {
  AreaChartOutlined,
  BarChartOutlined,
  EyeOutlined,
  LineChartOutlined,
  ThunderboltOutlined,
} from '@ant-design/icons';
import { Button, Divider, Radio, Switch, Tooltip } from 'antd';

import { useChart } from '../../hooks/useChart';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import {
  setChartType,
  toggleDefinedPoints,
  toggleLegend,
  toggleP10,
  toggleP50,
  toggleP90,
} from '../../store/slices/chartSlice';
import { ChartType } from '../../types/api.types';
import './styles.less';

export const Toolbar: React.FC = () => {
  const dispatch = useAppDispatch();
  const { settings, isGenerating } = useAppSelector((state) => state.chart);
  const { processedData } = useAppSelector((state) => state.session);
  const { generateChart } = useChart();

  const handleChartTypeChange = (e: any) => {
    dispatch(setChartType(e.target.value));
  };

  const isDisabled = !processedData || isGenerating;

  return (
    <div className="toolbar">
      <div className="toolbar__section">
        <div className="toolbar__section-title">
          <BarChartOutlined />
          Chart Type
        </div>
        <Radio.Group
          value={settings.chartType}
          onChange={handleChartTypeChange}
          disabled={isDisabled}
          className="toolbar__chart-type"
          buttonStyle="solid"
        >
          <Radio.Button value={ChartType.LINE}>
            <LineChartOutlined /> Line
          </Radio.Button>
          <Radio.Button value={ChartType.CUMULATIVE}>
            <AreaChartOutlined /> Cumulative
          </Radio.Button>
        </Radio.Group>
      </div>

      <Divider className="toolbar__section-divider" />

      <div className="toolbar__section">
        <div className="toolbar__section-title">
          <EyeOutlined />
          Display Options
        </div>
        <div className="toolbar__controls">
          <div className="toolbar__control-item">
            <span className="toolbar__control-item-label">Show Legend</span>
            <Switch checked={settings.showLegend} onChange={() => dispatch(toggleLegend())} disabled={isDisabled} />
          </div>
          <div className="toolbar__control-item">
            <Tooltip title="Show count of defined data points over time">
              <span className="toolbar__control-item-label">Defined Points Count</span>
            </Tooltip>
            <Switch
              checked={settings.showDefinedPoints}
              onChange={() => dispatch(toggleDefinedPoints())}
              disabled={isDisabled}
            />
          </div>
        </div>
      </div>

      <Divider className="toolbar__section-divider" />

      <div className="toolbar__section">
        <div className="toolbar__section-title">
          <ThunderboltOutlined />
          Statistics
        </div>
        <div className="toolbar__statistics">
          <div className="toolbar__statistics-item">
            <div className="toolbar__statistics-item-label">
              <span className="toolbar__statistics-item-label-icon toolbar__statistics-item-label-icon--p10" />
              <span className="toolbar__statistics-item-label-text">P10 (10th Percentile)</span>
            </div>
            <Switch checked={settings.showP10} onChange={() => dispatch(toggleP10())} disabled={isDisabled} />
          </div>

          <div className="toolbar__statistics-item">
            <div className="toolbar__statistics-item-label">
              <span className="toolbar__statistics-item-label-icon toolbar__statistics-item-label-icon--p50" />
              <span className="toolbar__statistics-item-label-text">P50 (Median)</span>
            </div>
            <Switch checked={settings.showP50} onChange={() => dispatch(toggleP50())} disabled={isDisabled} />
          </div>

          <div className="toolbar__statistics-item">
            <div className="toolbar__statistics-item-label">
              <span className="toolbar__statistics-item-label-icon toolbar__statistics-item-label-icon--p90" />
              <span className="toolbar__statistics-item-label-text">P90 (90th Percentile)</span>
            </div>
            <Switch checked={settings.showP90} onChange={() => dispatch(toggleP90())} disabled={isDisabled} />
          </div>
        </div>
      </div>

      <div className="toolbar__actions">
        <Button
          type="primary"
          icon={<ThunderboltOutlined />}
          onClick={generateChart}
          loading={isGenerating}
          disabled={isDisabled}
          block
        >
          Generate Chart
        </Button>
      </div>
    </div>
  );
};
