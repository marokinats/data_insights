/**
 * Custom hook for session operations with Redux
 */
import { useCallback } from 'react';

import { message } from 'antd';

import { useAppDispatch, useAppSelector } from '../store/hooks';
import { resetChart } from '../store/slices/chartSlice';
import { deleteSession, resetSession, uploadFile } from '../store/slices/sessionSlice';

export const useSession = () => {
  const dispatch = useAppDispatch();
  const { sessionId, isUploading, uploadError, processedData } = useAppSelector((state) => state.session);

  const handleUploadFile = useCallback(
    async (file: File) => {
      try {
        const result = await dispatch(uploadFile(file)).unwrap();
        message.success(`File uploaded: ${result.uploadResponse.original_filename}`);

        return result;
      } catch (error: any) {
        message.error(error || 'Failed to upload file');
        throw error;
      }
    },
    [dispatch]
  );

  const handleDeleteSession = useCallback(async () => {
    if (!sessionId) {
      message.warning('No active session to delete');
      return;
    }

    try {
      await dispatch(deleteSession(sessionId)).unwrap();
      dispatch(resetChart());
      message.success('Session reset successfully');
    } catch (error: any) {
      message.error(error || 'Failed to reset session');
    }
  }, [dispatch, sessionId]);

  const handleResetSession = useCallback(() => {
    dispatch(resetSession());
    dispatch(resetChart());
    message.info('Session cleared');
  }, [dispatch]);

  return {
    uploadFile: handleUploadFile,
    deleteSession: handleDeleteSession,
    resetSession: handleResetSession,
    sessionId,
    isUploading,
    uploadError,
    processedData,
  };
};
