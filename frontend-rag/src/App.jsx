import { useEffect, useRef } from 'react';
import { useRAGContext } from './context/RAGContext';
import './App.css';
import ChatMessage from './components/ChatMessage';

function App() {
  // TODO: Adicionar estados aqui
  const { messages, isLoading } = useRAGContext();
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const stats = () => {
    // console.log('📊 [COM useMemo] Calculando stats...');
    // Este log só aparece quando 'messages' muda!
    return {
      total: 0,
      user: 0,
      bot: 0
    };
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <h1>🤖 RAG Chat - FIAP</h1>
        <p className="subtitle">
          👆 Faça upload de um PDF para começar
        </p>
      </header>

      {/* Upload Section */}
      <div className="upload-container">
        <label htmlFor="file-upload" className="upload-label">
          📄 Fazer upload de PDF
        </label>

        <input
          id="file-upload"
          type="file"
          accept=".pdf"
          className="upload-input"
        />
      </div>

      {/* Messages Container */}
      <div className="messages-container">
        <div className="empty-state">
          <h2>💬 Nenhuma conversa ainda</h2>
          <p>Faça upload de um PDF e comece a fazer perguntas!</p>
        </div>

        {/* TODO: Renderizar lista de mensagens aqui */}

        {isLoading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Processando...</p>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Stats Bar */}
      <div className="stats-bar">
        <span>📊 Total: {stats.total}</span>
        <span>👤 Você: {stats.user}</span>
        <span>🤖 Bot: {stats.bot}</span>
        <button onClick={() => {}} className="clear-button">
          🗑️ Limpar
        </button>
      </div>
      {/* TODO: Mostrar stats quando houver mensagens */}

      {/* Chat Input */}
      <form className="chat-input-form">
        <input
          type="text"
          placeholder="Digite sua pergunta..."
          className="chat-input"
        />
        <button type="submit" className="chat-button">
          📤 Enviar
        </button>
      </form>
    </div>
  );
}

export default App;
