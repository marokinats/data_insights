/**
 * Chart-specific types
 */
import type { ChartType, SeriesData } from './api.types';

export interface SeriesDisplayConfig extends SeriesData {
  id: string;
}

export interface ChartSettings {
  showLegend: boolean;
  showDefinedPoints: boolean;
  showP10: boolean;
  showP50: boolean;
  showP90: boolean;
  chartType: ChartType;
}
