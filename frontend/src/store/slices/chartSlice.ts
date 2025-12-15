/**
 * Chart Slice - handle Charts
 */
import { type PayloadAction, createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import type { PlotType } from 'plotly.js';

import { apiService } from '../../services/api';
import { type ChartConfig, ChartType } from '../../types/api.types';
import type { RootState } from '../index';
import { uploadFile } from './sessionSlice';

interface ChartSettings {
  showLegend: boolean;
  showDefinedPoints: boolean;
  showP10: boolean;
  showP50: boolean;
  showP90: boolean;
  chartType: ChartType;
}
interface ChartData {
  line: Record<string, string | number>;
  name: string;
  mode: string;
  type: PlotType;
  x: number[];
  y: number[];
}

interface ChartLayout {
  height: number;
  width: number;
  hovermode: false | 'x' | 'y' | 'closest' | 'x unified' | 'y unified' | undefined;
  title: Record<string, string>;
  xaxis: Record<string, string>;
  yaxis: Record<string, string>;
}

interface ChartAllData {
  data: ChartData[];
  layout: ChartLayout;
}
interface ChartState {
  chartData: ChartAllData | null;
  chartConfig: ChartConfig | null;
  settings: ChartSettings;
  statisticsColors: {
    p10: string;
    p50: string;
    p90: string;
  } | null;
  isGenerating: boolean;
  generateError: string | null;
}

const initialState: ChartState = {
  chartData: null,
  chartConfig: null,
  settings: {
    showLegend: true,
    showDefinedPoints: false,
    showP10: false,
    showP50: false,
    showP90: false,
    chartType: ChartType.LINE,
  },
  statisticsColors: null,
  isGenerating: false,
  generateError: null,
};

export const generateChart = createAsyncThunk('chart/generateChart', async (_, { getState, rejectWithValue }) => {
  const state = getState() as RootState;
  const { sessionId, processedData } = state.session;
  const { settings } = state.chart;

  if (!sessionId || !processedData) {
    return rejectWithValue('No session data available');
  }

  try {
    const config: ChartConfig = {
      session_id: sessionId,
      chart_type: settings.chartType,
      show_legend: settings.showLegend,
      show_defined_points: settings.showDefinedPoints,
      show_p10: settings.showP10,
      show_p50: settings.showP50,
      show_p90: settings.showP90,
      series_config: processedData.series.map((s) => ({
        name: s.name,
        visible: s.visible,
        color: s.color,
      })),
    };

    const response = await apiService.generateChart(config);

    return {
      chartData: response.chart,
      chartConfig: config,
      statisticsColors: response.statistics_colors,
    };
  } catch (error: any) {
    return rejectWithValue(error.message || 'Failed to generate chart');
  }
});

export const getChartPreview = createAsyncThunk(
  'chart/getChartPreview',
  async (sessionId: string, { rejectWithValue }) => {
    try {
      const response = await apiService.getChartPreview(sessionId);
      return {
        chartData: response.chart,
        chartConfig: response.config,
        statisticsColors: response.statistics_colors,
      };
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to get chart preview');
    }
  }
);

const chartSlice = createSlice({
  name: 'chart',
  initialState,
  reducers: {
    updateSettings: (state, action: PayloadAction<Partial<ChartSettings>>) => {
      state.settings = { ...state.settings, ...action.payload };
    },
    setChartType: (state, action: PayloadAction<ChartType>) => {
      state.settings.chartType = action.payload;
    },
    toggleLegend: (state) => {
      state.settings.showLegend = !state.settings.showLegend;
    },
    toggleDefinedPoints: (state) => {
      state.settings.showDefinedPoints = !state.settings.showDefinedPoints;
    },
    toggleP10: (state) => {
      state.settings.showP10 = !state.settings.showP10;
    },
    toggleP50: (state) => {
      state.settings.showP50 = !state.settings.showP50;
    },
    toggleP90: (state) => {
      state.settings.showP90 = !state.settings.showP90;
    },
    resetChart: (state) => {
      state.chartData = null;
      state.chartConfig = null;
      state.generateError = null;
    },
  },
  extraReducers: (builder) => {
    // Generate chart
    builder
      .addCase(generateChart.pending, (state) => {
        state.isGenerating = true;
        state.generateError = null;
      })
      .addCase(generateChart.fulfilled, (state, action) => {
        state.isGenerating = false;
        state.chartData = action.payload.chartData;
        state.chartConfig = action.payload.chartConfig;
        state.statisticsColors = action.payload.statisticsColors;
        state.generateError = null;
      })
      .addCase(generateChart.rejected, (state, action) => {
        state.isGenerating = false;
        state.generateError = action.payload as string;
      });

    // Get chart preview
    builder
      .addCase(getChartPreview.pending, (state) => {
        state.isGenerating = true;
        state.generateError = null;
      })
      .addCase(getChartPreview.fulfilled, (state, action) => {
        state.isGenerating = false;
        state.chartData = action.payload.chartData;
        state.chartConfig = action.payload.chartConfig;
        state.statisticsColors = action.payload.statisticsColors;
        state.generateError = null;
      })
      .addCase(getChartPreview.rejected, (state, action) => {
        state.isGenerating = false;
        state.generateError = action.payload as string;
      });
    builder.addCase(uploadFile.fulfilled, (state) => {
      state.chartData = null;
      state.chartConfig = null;
      state.generateError = null;
      state.isGenerating = false;
    });
  },
});

export const {
  updateSettings,
  setChartType,
  toggleLegend,
  toggleDefinedPoints,
  toggleP10,
  toggleP50,
  toggleP90,
  resetChart,
} = chartSlice.actions;

export default chartSlice.reducer;
