import { memo, useMemo } from 'react';

function ChatMessage({ message }) {
  // TODO: Desestruturar propriedades da mensagem

  // TODO: Implementar formatação de tempo com useMemo
  const formattedTime = useMemo(() => {
    return '00:00';
  }, []);

  return (
    <div className="message user">
      <div className="message-header">
        <strong>👤 Você</strong>
        <span className="message-time">{formattedTime}</span>
      </div>

      <div className="message-content">
        {/* TODO: Mostrar conteúdo da mensagem */}
        Exemplo de mensagem
      </div>

      {/* TODO: Mostrar confiança para mensagens do bot */}

      {/* TODO: Mostrar fontes se existirem */}
    </div>
  );
}

export default memo(ChatMessage);
