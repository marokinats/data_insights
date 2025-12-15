/**
 * UI Slice - handle UI state
 */
import { type PayloadAction, createSlice } from '@reduxjs/toolkit';

interface UiState {
  isExporting: boolean;
  exportError: string | null;
  globalError: string | null;
  sidebarCollapsed: boolean;
}

const initialState: UiState = {
  isExporting: false,
  exportError: null,
  globalError: null,
  sidebarCollapsed: false,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setIsExporting: (state, action: PayloadAction<boolean>) => {
      state.isExporting = action.payload;
    },
    setExportError: (state, action: PayloadAction<string | null>) => {
      state.exportError = action.payload;
    },
    setGlobalError: (state, action: PayloadAction<string | null>) => {
      state.globalError = action.payload;
    },
    toggleSidebar: (state) => {
      state.sidebarCollapsed = !state.sidebarCollapsed;
    },
    clearErrors: (state) => {
      state.exportError = null;
      state.globalError = null;
    },
  },
});

export const { setIsExporting, setExportError, setGlobalError, toggleSidebar, clearErrors } = uiSlice.actions;

export default uiSlice.reducer;
