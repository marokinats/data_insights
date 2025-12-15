import React, { useCallback } from 'react';

import { CheckCircleOutlined, FileTextOutlined, InboxOutlined, ReloadOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { Button, Upload, message } from 'antd';

import { useSession } from '../../hooks/useSession';
import { useAppSelector } from '../../store/hooks';
import './styles.less';

const { Dragger } = Upload;

export const FileUploader: React.FC = () => {
  const { uploadFile, resetSession } = useSession();
  const { isUploading, processedData, uploadError } = useAppSelector((state) => state.session);

  const handleUpload: UploadProps['customRequest'] = useCallback(
    async (options) => {
      const { file, onSuccess, onError } = options;

      try {
        await uploadFile(file as File);
        onSuccess?.('ok');
      } catch (error) {
        onError?.(error as Error);
      }
    },
    [uploadFile]
  );

  const beforeUpload = (file: File) => {
    const isCSV = file.type === 'text/csv' || file.name.endsWith('.csv');
    if (!isCSV) {
      message.error('You can only upload CSV files!');
      return false;
    }

    const isLt50M = file.size / 1024 / 1024 < 50;
    if (!isLt50M) {
      message.error('File must be smaller than 50MB!');
      return false;
    }

    return true;
  };

  if (processedData) {
    return (
      <div className="file-uploader">
        <div className="file-uploader__status">
          <div className="file-uploader__status-info">
            <CheckCircleOutlined />
            <div className="file-uploader__status-text">
              <div className="file-uploader__status-text-title">
                <FileTextOutlined /> {processedData.original_filename}
              </div>
              <div className="file-uploader__status-text-details">{processedData.series.length} series</div>
            </div>
          </div>
          <Button icon={<ReloadOutlined />} onClick={resetSession} disabled={isUploading}>
            Upload New File
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="file-uploader">
      <div className="file-uploader__dragger">
        <Dragger
          name="file"
          multiple={false}
          accept=".csv"
          customRequest={handleUpload}
          beforeUpload={beforeUpload}
          showUploadList={false}
          disabled={isUploading}
        >
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">Click or drag CSV file to this area to upload</p>
          <p className="ant-upload-hint">Support for a single CSV file upload. Maximum file size: 50MB</p>
        </Dragger>
      </div>

      <div className="file-uploader__info">
        <div className="file-uploader__info-title">CSV File Requirements:</div>
        <ul className="file-uploader__info-list">
          <li>File must contain paired columns (X-axis, Y-axis)</li>
          <li>X-axis columns: Month values (will be converted to days)</li>
          <li>Y-axis columns: Measurement values</li>
          <li>Each pair represents one data series</li>
          <li>All values should be numeric</li>
        </ul>
      </div>

      {uploadError && (
        <div className="file-uploader__error">
          <strong>Error:</strong> {uploadError}
        </div>
      )}
    </div>
  );
};
