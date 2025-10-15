import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './index.css';

// TODO: Adicionar RAGProvider aqui
// import { RAGProvider } from './context/RAGContext.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* TODO: Envolver App com RAGProvider */}
    <App />
  </StrictMode>
);
