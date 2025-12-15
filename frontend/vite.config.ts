import react from '@vitejs/plugin-react';
import path from 'path';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
        modifyVars: {
          // Ant Design theme variables
          '@primary-color': '#1890ff',
          '@link-color': '#1890ff',
          '@success-color': '#52c41a',
          '@warning-color': '#faad14',
          '@error-color': '#f5222d',
          '@font-size-base': '14px',
          '@heading-color': 'rgba(0, 0, 0, 0.85)',
          '@text-color': 'rgba(0, 0, 0, 0.65)',
          '@text-color-secondary': 'rgba(0, 0, 0, 0.45)',
          '@disabled-color': 'rgba(0, 0, 0, 0.25)',
          '@border-radius-base': '6px',
          '@border-color-base': '#d9d9d9',
          '@box-shadow-base': '0 2px 8px rgba(0, 0, 0, 0.15)',
        },
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
