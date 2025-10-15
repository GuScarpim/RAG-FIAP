import './App.css';

function App() {
  // TODO: Adicionar estados aqui

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
      </div>

      {/* Stats Bar */}
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
