import React from 'react';

import { FileTextOutlined } from '@ant-design/icons';
import { Layout, Space, Typography } from 'antd';

import { ChartViewer } from './components/Chart/ChartViewer';
import { Toolbar } from './components/Toolbar/Toolbar';
import { FileUploader } from './components/Upload/FileUploader';
import { useAppSelector } from './store/hooks';

const { Header, Content, Sider } = Layout;
const { Title } = Typography;

const App: React.FC = () => {
  const { processedData } = useAppSelector((state) => state.session);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header>
        <Space>
          <FileTextOutlined style={{ fontSize: '24px', color: '#1890ff' }} />
          <Title level={3} style={{ margin: 0, color: '#1890ff' }}>
            Data Insights
          </Title>
        </Space>
      </Header>

      <Layout>
        {processedData && (
          <Sider width={320} theme="light" style={{ padding: '24px 16px' }}>
            <Toolbar />
          </Sider>
        )}

        <Content style={{ padding: '24px' }}>
          <Space orientation="vertical" size="large" style={{ width: '100%' }}>
            {!processedData && <FileUploader />}
            {processedData && (
              <>
                <FileUploader />
                <ChartViewer />
              </>
            )}
          </Space>
        </Content>
      </Layout>
    </Layout>
  );
};

export default App;
