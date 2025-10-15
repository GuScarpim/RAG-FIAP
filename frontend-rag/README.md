# Frontend RAG - Template para Aula

## 🎯 O que é este projeto?

Este é um **template base** para ensinar React na prática.

- ✅ **CSS Completo** - Todo o design está pronto
- ✅ **Estrutura HTML** - Todos os componentes têm o layout
- 🔨 **Funcionalidades** - Código comentado com `// TODO:` para você implementar

## 📚 Leia Primeiro

👉 **[GUIA_AULA.md](./GUIA_AULA.md)** ← GUIA COMPLETO DA AULA

## 🚀 Quick Start

```bash
# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev
```

## 📁 Arquivos para Implementar

Durante a aula, você vai implementar:

1. **Context API** (`src/context/RAGContext.jsx`)
   - Gerenciamento de estado global

2. **Hook Customizado** (`src/hooks/useRAG.js`)
   - Lógica de comunicação com API

3. **Componentes**
   - `FileUpload.jsx` - Upload de PDF
   - `ChatMessage.jsx` - Mensagens do chat
   - `ChatInput.jsx` - Input de perguntas

4. **App Principal** (`src/App.jsx`)
   - Integração de tudo

## 🎓 Conceitos que você vai aprender

- Context API
- Hooks (useState, useCallback, useMemo, useRef, useEffect)
- Fetch API
- Controlled Inputs
- React Patterns
- Performance (memo, lazy loading)

## 📖 Estrutura

```
frontend-rag/
├── src/
│   ├── App.jsx              ✅ HTML pronto
│   ├── App.css              ✅ CSS completo
│   ├── main.jsx             ✅ Setup básico
│   ├── context/
│   │   └── RAGContext.jsx   🔨 Implementar
│   ├── hooks/
│   │   └── useRAG.js        🔨 Implementar
│   └── components/
│       ├── FileUpload.jsx   🔨 Implementar
│       ├── ChatMessage.jsx  🔨 Implementar
│       └── ChatInput.jsx    🔨 Implementar
└── GUIA_AULA.md            📚 Roteiro completo
```

## 🔗 Backend Necessário

Este frontend se conecta ao backend RAG em:
```
http://localhost:8000
```

**Endpoints usados:**
- `POST /upload` - Upload de PDF
- `POST /query` - Fazer perguntas

## 💡 Dica

Cada parte tem comentários `// TODO:` indicando o que fazer.

## 🎉 Objetivo

Ao final, você terá uma aplicação RAG completa funcionando, e terá aprendido:
- Como estruturar uma aplicação React
- Como usar Context API
- Como criar hooks customizados
- Como integrar com backend
- Boas práticas de performance

**Boa aula! 🚀**
