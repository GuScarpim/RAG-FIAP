import { memo, useMemo } from 'react';

function ChatMessage({ message }) {
  // TODO: Desestruturar propriedades da mensagem
  const { type, isError } = message;

  // TODO: Implementar formatação de tempo com useMemo
  const formattedTime = useMemo(() => {
    return '00:00';
  }, []);

  return (
    <div className={`message ${type} ${isError ? 'error' : ''}`}>
      <div className="message-header">
        <strong>👤 Você</strong>
        <span className="message-time">{formattedTime}</span>
      </div>

      <div className="message-content">
        {/* TODO: Mostrar conteúdo da mensagem */}
        Exemplo de mensagem
      </div>

      {/* TODO: Mostrar confiança para mensagens do bot */}
      <div className="message-confidence">
        Confiança: 100%
      </div>
      {/* TODO: Mostrar fontes se existirem */}
      <details className="message-sources">
        <summary>📚 Ver fontes (0)</summary>
        <div className="sources-list">
          <div className="source-item">
            <strong>Trecho:</strong>
            <p>Teste</p>
          </div>
        </div>
      </details>
    </div>
  );
}

export default memo(ChatMessage);
