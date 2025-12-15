/**
 * Redux Store Configuration
 */
import { configureStore } from '@reduxjs/toolkit';

import chartReducer from './slices/chartSlice';
import sessionReducer from './slices/sessionSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    session: sessionReducer,
    chart: chartReducer,
    ui: uiReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['chart/generateChart/fulfilled'],
        ignoredPaths: ['chart.chartData'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
