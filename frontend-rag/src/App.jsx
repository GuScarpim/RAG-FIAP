import { lazy, Suspense, useEffect, useMemo, useRef } from 'react';
import { useRAGContext } from './context/RAGContext';
import './App.css';


const FileUpload = lazy(() => import('./components/FileUpload'));
const ChatMessage = lazy(() => import('./components/ChatMessage'));
const ChatInput = lazy(() => import('./components/ChatInput'));
// import ChatInput from './components/ChatInput';
// import FileUpload from './components/FileUpload';
// import ChatMessage from './components/ChatMessage';
import { useRAG } from './hooks/useRAG';

function App() {
  // TODO: Adicionar estados aqui
  const { messages, uploadedFile, isLoading } = useRAGContext();
  const { clearMessages } = useRAG();
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const stats = useMemo(() => {
    // Este log só aparece quando 'messages' muda!
    return {
      total: messages.length,
      user: messages.filter(mes => mes.type === 'user').length,
      bot: messages.filter(mes => mes.type === 'bot').length
    };
  }, [messages]);

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <h1>🤖 RAG Chat - FIAP</h1>
        <p className="subtitle">
          {uploadedFile ? uploadedFile.filename : '👆 Faça upload de um PDF para começar'}
        </p>
      </header>

      {/* Upload Section */}
      <Suspense fallback={<div className="loading">Carregando...</div>}>
        <FileUpload />
      </Suspense>

      {/* TODO: Renderizar lista de mensagens aqui */}
      {/* Messages Container */}
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <h2>💬 Nenhuma conversa ainda</h2>
            <p>Faça upload de um PDF e comece a fazer perguntas!</p>
          </div>) : (
          <Suspense fallback={<div className="loading">Carregando mensagens...</div>}>
            {messages.map((message) => (
              <ChatMessage message={message} />
            ))}
          </Suspense>
        )}

        {isLoading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Processando...</p>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Stats Bar */}
      {messages.length > 0 && (
        <div className="stats-bar">
          <span>📊 Total: {stats.total}</span>
          <span>👤 Você: {stats.user}</span>
          <span>🤖 Bot: {stats.bot}</span>
          <button onClick={clearMessages} className="clear-button">
            🗑️ Limpar
          </button>
        </div>
      )}
      {/* TODO: Mostrar stats quando houver mensagens */}

      {/* Chat Input */}
      <Suspense fallback={<div className="loading">Carregando input...</div>}>
        <ChatInput />
      </Suspense>
    </div>
  );
}

export default App;
