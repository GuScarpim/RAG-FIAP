import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import { RAGProvider } from './context/RAGContext.jsx';
import './index.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RAGProvider>
      <App />
    </RAGProvider>
  </StrictMode>
);
