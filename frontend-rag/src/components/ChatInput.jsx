import { memo, useCallback, useState } from 'react';
// import { useRAGContext } from '../context/RAGContext';
// import { useRAG } from '../hooks/useRAG';

function ChatInput() {
  // TODO: Obter estados do Context

  // TODO: Criar estado local para o input
  const [input, setInput] = useState('');

  // TODO: Implementar handleSubmit com useCallback
  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();

    console.log('Submit:', input);
  }, [input]);

  // TODO: Implementar handleKeyDown com useCallback
  const handleKeyDown = useCallback((e) => {
  }, [handleSubmit]);

  return (
    <form onSubmit={handleSubmit} className="chat-input-form">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Digite sua pergunta..."
        className="chat-input"
      />

      <button
        type="submit"
        disabled={!input.trim()}
        className="chat-button"
      >
        📤 Enviar
      </button>
    </form>
  );
}

export default memo(ChatInput);
