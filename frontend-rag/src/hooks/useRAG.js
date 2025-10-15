import { useCallback } from 'react';
// import { useRAGContext } from '../context/RAGContext';

const API_URL = 'http://localhost:8000';

export function useRAG() {
  // TODO: Obter estados do Context

  // TODO: Implementar função de upload
  const uploadFile = useCallback(async (file) => {

    console.log('Upload file:', file);
    return { success: false };
  }, []);

  // TODO: Implementar função de enviar pergunta
  const sendQuery = useCallback(async (question) => {

    console.log('Send query:', question);
    return { success: false };
  }, []);

  // TODO: Implementar função de limpar mensagens
  const clearMessages = useCallback(() => {
    console.log('Clear messages');
  }, []);

  return {
    uploadFile,
    sendQuery,
    clearMessages,
  };
}
