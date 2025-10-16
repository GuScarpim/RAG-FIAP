import { useCallback } from 'react';
import { useRAGContext } from '../context/RAGContext';

const API_URL = 'http://localhost:8000';

export function useRAG() {
  // TODO: Obter estados do Context
  const {
    messages,
    setMessages,
    setIsLoading,
    setUploadedFile
  } = useRAGContext();

  // TODO: Implementar função de upload
  const uploadFile = useCallback(async (file) => {
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      setUploadedFile(data);
      return { success: true, data }
    } catch (error) {
      console.error(error);
      return { success: false, error: error.message }
    } finally {
      setIsLoading(false);
    }
  }, [setIsLoading, setUploadedFile]);

  // TODO: Implementar função de enviar pergunta
  // Enviar pergunta
  const sendQuery = useCallback(async (question) => {
    // Adiciona mensagem do usuário
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: question,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);

    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();

      // Adiciona resposta do bot
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: data.answer,
        sources: data.sources || [],
        confidence: data.confidence,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botMessage]);

      localStorage.setItem('messages', JSON.stringify(messages));

      return { success: true, data };
    } catch (error) {
      console.error('Erro ao enviar pergunta:', error);

      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Erro ao processar sua pergunta. Tente novamente.',
        isError: true,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);

      return { success: false, error: error.message };
    } finally {
      setIsLoading(false);
    }
  }, [setMessages, setIsLoading]);

  // TODO: Implementar função de limpar mensagens
  const clearMessages = useCallback(() => {
    setMessages([])
    localStorage.removeItem('messages')
  }, [setMessages]);

  return {
    messages,
    uploadFile,
    sendQuery,
    clearMessages,
  };
}

