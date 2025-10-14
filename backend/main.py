"""
BACKEND RAG - Sistema de Recuperação e Geração Aumentada
Este é o arquivo principal da API FastAPI que implementa um sistema RAG completo.

Funcionalidades:
- Upload e processamento de PDFs
- Criação de embeddings vetoriais
- Busca semântica em documentos
- Geração de respostas usando LLM com contexto
- Configurações personalizáveis de LLM (temperatura, tokens, etc.)
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from datetime import datetime

# Importações para processamento de PDF e RAG
from services.pdf_processor import PDFProcessor
from services.vector_store import VectorStoreManager
from services.llm_service import LLMService

# ============================================================================
# CONFIGURAÇÃO DA APLICAÇÃO FASTAPI
# ============================================================================

app = FastAPI(
    title="RAG API - Sistema de Perguntas e Respostas sobre PDFs",
    description="API para upload de PDFs e consultas usando RAG (Retrieval-Augmented Generation)",
    version="1.0.0",
)

# ============================================================================
# CONFIGURAÇÃO DE CORS
# Permite que o frontend React faça requisições para esta API
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique o domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# ============================================================================
# MODELOS PYDANTIC (SCHEMAS)
# Definem a estrutura dos dados que a API recebe e retorna
# ============================================================================


class QueryRequest(BaseModel):
    """
    Modelo para requisição de pergunta ao sistema RAG
    """

    question: str = Field(..., description="Pergunta do usuário sobre o documento")
    temperature: float = Field(
        0.7,
        ge=0.0,
        le=2.0,
        description="Controla a criatividade da resposta (0=determinístico, 2=muito criativo)",
    )
    max_tokens: int = Field(
        500, ge=50, le=2000, description="Número máximo de tokens na resposta"
    )
    top_k: int = Field(
        3, ge=1, le=10, description="Número de chunks relevantes a recuperar"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Qual é o tema principal do documento?",
                "temperature": 0.7,
                "max_tokens": 500,
                "top_k": 3,
            }
        }


class QueryResponse(BaseModel):
    """
    Modelo para resposta da consulta RAG
    """

    answer: str = Field(..., description="Resposta gerada pela LLM")
    sources: List[str] = Field(
        ..., description="Trechos do documento usados como contexto"
    )
    confidence: float = Field(
        ..., description="Confiança da resposta (baseada na similaridade)"
    )
    tokens_used: int = Field(..., description="Número de tokens utilizados na geração")


class DocumentInfo(BaseModel):
    """
    Modelo para informações sobre documentos processados
    """

    filename: str
    pages: int
    chunks: int
    uploaded_at: str
    size_kb: float


class HealthResponse(BaseModel):
    """
    Modelo para verificação de saúde da API
    """

    status: str
    message: str
    documents_loaded: int


# ============================================================================
# INICIALIZAÇÃO DOS SERVIÇOS
# Instancia os serviços de processamento de PDF, vector store e LLM
# ============================================================================

pdf_processor = PDFProcessor()
vector_store = VectorStoreManager()
llm_service = LLMService()

# ============================================================================
# ENDPOINTS DA API
# ============================================================================


@app.get("/", response_model=HealthResponse)
async def root():
    """
    Endpoint raiz - Verifica se a API está funcionando
    """
    return {
        "status": "online",
        "message": "RAG API está funcionando! Use /docs para ver a documentação completa.",
        "documents_loaded": vector_store.get_document_count(),
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Endpoint de health check - Verifica o status da API e quantos documentos estão carregados
    """
    return {
        "status": "healthy",
        "message": "Todos os serviços estão operacionais",
        "documents_loaded": vector_store.get_document_count(),
    }


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint para upload de PDF

    Processo:
    1. Valida se o arquivo é um PDF
    2. Salva o arquivo temporariamente
    3. Extrai o texto do PDF
    4. Divide o texto em chunks (pedaços menores)
    5. Cria embeddings vetoriais dos chunks
    6. Armazena no vector store para busca semântica

    Args:
        file: Arquivo PDF enviado pelo usuário

    Returns:
        Informações sobre o documento processado
    """

    # Validação: verifica se o arquivo é um PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")

    try:
        # Lê o conteúdo do arquivo
        contents = await file.read()
        file_size_kb = len(contents) / 1024  # Tamanho em KB

        # Salva temporariamente o arquivo
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(contents)

        # PASSO 1: Extrai texto do PDF
        print(f"📄 Processando PDF: {file.filename}")
        text_chunks, num_pages = pdf_processor.process_pdf(temp_path)

        # PASSO 2: Cria embeddings e armazena no vector store
        print(f"🔍 Criando embeddings para {len(text_chunks)} chunks...")
        vector_store.add_documents(text_chunks, file.filename)

        # Remove arquivo temporário
        os.remove(temp_path)

        # Retorna informações sobre o documento processado
        return {
            "message": "PDF processado com sucesso!",
            "document_info": {
                "filename": file.filename,
                "pages": num_pages,
                "chunks": len(text_chunks),
                "uploaded_at": datetime.now().isoformat(),
                "size_kb": round(file_size_kb, 2),
            },
        }

    except Exception as e:
        # Em caso de erro, remove o arquivo temporário se existir
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Endpoint para fazer perguntas sobre os documentos carregados

    Processo RAG (Retrieval-Augmented Generation):
    1. RETRIEVAL: Busca os chunks mais relevantes no vector store
    2. AUGMENTATION: Monta um contexto com os chunks encontrados
    3. GENERATION: Usa a LLM para gerar uma resposta baseada no contexto

    Args:
        request: Objeto contendo a pergunta e configurações da LLM

    Returns:
        Resposta gerada, fontes usadas e métricas
    """

    # Verifica se há documentos carregados
    if vector_store.get_document_count() == 0:
        raise HTTPException(
            status_code=400,
            detail="Nenhum documento carregado. Faça upload de um PDF primeiro.",
        )

    try:
        # PASSO 1: RETRIEVAL - Busca chunks relevantes
        print(f"🔍 Buscando contexto para: {request.question}")
        relevant_chunks = vector_store.search(request.question, k=request.top_k)

        if not relevant_chunks:
            raise HTTPException(
                status_code=404,
                detail="Não foram encontrados trechos relevantes para sua pergunta",
            )

        # PASSO 2: AUGMENTATION - Prepara o contexto
        context = "\n\n".join([chunk["text"] for chunk in relevant_chunks])
        sources = [
            chunk["text"][:200] + "..." for chunk in relevant_chunks
        ]  # Primeiros 200 caracteres

        # Calcula confiança média baseada nas similaridades
        avg_confidence = sum([chunk["score"] for chunk in relevant_chunks]) / len(
            relevant_chunks
        )

        # PASSO 3: GENERATION - Gera resposta com a LLM
        print(f"🤖 Gerando resposta com temperatura={request.temperature}")
        answer, tokens_used = llm_service.generate_answer(
            question=request.question,
            context=context,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return {
            "answer": answer,
            "sources": sources,
            "confidence": round(avg_confidence, 2),
            "tokens_used": tokens_used,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar consulta: {str(e)}"
        )


@app.get("/documents", response_model=List[str])
async def list_documents():
    """
    Endpoint para listar todos os documentos carregados no sistema

    Returns:
        Lista com nomes dos documentos
    """
    documents = vector_store.list_documents()
    return documents


@app.delete("/documents")
async def clear_documents():
    """
    Endpoint para limpar todos os documentos do vector store
    Útil para resetar o sistema

    Returns:
        Mensagem de confirmação
    """
    vector_store.clear()
    return {"message": "Todos os documentos foram removidos do sistema"}


# ============================================================================
# INICIALIZAÇÃO DO SERVIDOR
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    # Inicia o servidor na porta 8000
    # reload=True permite hot-reload durante desenvolvimento
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
