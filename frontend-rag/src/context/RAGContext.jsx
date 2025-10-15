import { createContext, useContext, useState } from 'react';

// Cria o Context
const RAGContext = createContext(null);


// TODO: Criar o Provider
export function RAGProvider({ children }) {
  // TODO: Adicionar estados aqui
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // TODO: Criar o value com os estados
  const value = {
    messages,
    setMessages,
    isLoading,
    setIsLoading,
  };
  return (
    <>
      <RAGContext.Provider value={value}>
        {children}
      </RAGContext.Provider>
    </>
  );
}

// TODO: Criar hook customizado para acessar o Context
export function useRAGContext() {
  const context = useContext(RAGContext);
  if (!context) {
    throw new Error('useRAGContext deve ser usado dentro de RAGProvider');
  }
  return context;
}
