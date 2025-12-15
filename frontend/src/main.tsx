import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';

import { ConfigProvider } from 'antd';

import App from './App';
import { store } from './store';
import './styles/index.less';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: '#1890ff',
            borderRadius: 6,
            colorSuccess: '#52c41a',
            colorWarning: '#faad14',
            colorError: '#f5222d',
          },
        }}
      >
        <App />
      </ConfigProvider>
    </Provider>
  </React.StrictMode>
);
