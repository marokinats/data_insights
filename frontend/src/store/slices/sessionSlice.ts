/**
 * Session Slice - handle Session and Data
 */
import { type PayloadAction, createAsyncThunk, createSlice } from '@reduxjs/toolkit';

import { apiService } from '../../services/api';
import type { ProcessedData } from '../../types/api.types';

interface SessionState {
  sessionId: string | null;
  processedData: ProcessedData | null;
  isUploading: boolean;
  uploadError: string | null;
}

const initialState: SessionState = {
  sessionId: null,
  processedData: null,
  isUploading: false,
  uploadError: null,
};

export const uploadFile = createAsyncThunk('session/uploadFile', async (file: File, { rejectWithValue }) => {
  try {
    const uploadResponse = await apiService.uploadCSV(file);
    const processedData = await apiService.getProcessedData(uploadResponse.session_id);

    return {
      uploadResponse,
      processedData,
    };
  } catch (error: any) {
    return rejectWithValue(error.message || 'Failed to upload file');
  }
});

export const deleteSession = createAsyncThunk(
  'session/deleteSession',
  async (sessionId: string, { rejectWithValue }) => {
    try {
      await apiService.deleteSession(sessionId);
      return sessionId;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to delete session');
    }
  }
);

const sessionSlice = createSlice({
  name: 'session',
  initialState,
  reducers: {
    setSessionId: (state, action: PayloadAction<string | null>) => {
      state.sessionId = action.payload;
    },
    setProcessedData: (state, action: PayloadAction<ProcessedData | null>) => {
      state.processedData = action.payload;
    },
    updateSeriesVisibility: (state, action: PayloadAction<{ seriesName: string; visible: boolean }>) => {
      if (state.processedData) {
        const series = state.processedData.series.find((s) => s.name === action.payload.seriesName);
        if (series) {
          series.visible = action.payload.visible;
        }
      }
    },
    updateSeriesColor: (state, action: PayloadAction<{ seriesName: string; color: string }>) => {
      if (state.processedData) {
        const series = state.processedData.series.find((s) => s.name === action.payload.seriesName);
        if (series) {
          series.color = action.payload.color;
        }
      }
    },
    resetSession: (state) => {
      state.sessionId = null;
      state.processedData = null;
      state.uploadError = null;
    },
  },
  extraReducers: (builder) => {
    // Upload file
    builder
      .addCase(uploadFile.pending, (state) => {
        state.isUploading = true;
        state.uploadError = null;
      })
      .addCase(uploadFile.fulfilled, (state, action) => {
        state.isUploading = false;
        state.sessionId = action.payload.uploadResponse.session_id;
        state.processedData = action.payload.processedData;
        state.uploadError = null;
      })
      .addCase(uploadFile.rejected, (state, action) => {
        state.isUploading = false;
        state.uploadError = action.payload as string;
      });

    // Delete session
    builder.addCase(deleteSession.fulfilled, (state) => {
      state.sessionId = null;
      state.processedData = null;
      state.uploadError = null;
    });
  },
});

export const { setSessionId, setProcessedData, updateSeriesVisibility, updateSeriesColor, resetSession } =
  sessionSlice.actions;

export default sessionSlice.reducer;
