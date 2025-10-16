import { memo, useMemo } from 'react';

function ChatMessage({ message }) {
  // TODO: Desestruturar propriedades da mensagem
  const { type, content, timestamp, sources, confidence, isError } = message;

  // TODO: Implementar formatação de tempo com useMemo
  const formattedTime = useMemo(() => {

    if (!(timestamp instanceof Date)) return '';
    return timestamp.toLocaleTimeString('pt-BR', {
      hour: '2-digit',
      minute: '2-digit'
    });
  }, [timestamp]);

  return (
    <div className={`message ${type} ${isError ? 'error' : ''}`}>
      <div className="message-header">
        <strong>{type === 'user' ? '👤 Você' : '🤖 Assistente'}</strong>
        <span className="message-time">{formattedTime}</span>
      </div>

      <div className="message-content">
        {content}
      </div>

      {/* TODO: Mostrar confiança para mensagens do bot */}
      {type === 'bot' && confidence !== undefined && (
        <div className="message-confidence">
          Confiança: {Math.round(confidence * 100)}%
        </div>
      )}

      {/* TODO: Mostrar fontes se existirem */}
      {sources && sources.length > 0 && (
        <details className="message-sources">
          <summary>📚 Ver fontes ({sources.length})</summary>
          <div className="sources-list">
            {sources.map((source, index) => (
              <div className="source-item" key={index}>
                <strong>Trecho: {index + 1}</strong>
                <p>{source}</p>
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
}

export default memo(ChatMessage);
