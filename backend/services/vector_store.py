"""
SERVIÇO DE VECTOR STORE
Gerencia embeddings vetoriais e busca semântica usando ChromaDB
"""

from typing import List, Dict
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class VectorStoreManager:
    """
    Gerencia o armazenamento vetorial e busca semântica

    Usa ChromaDB como banco de dados vetorial e SentenceTransformers
    para criar embeddings dos textos.
    """

    def __init__(self, collection_name: str = "documents"):
        """
        Inicializa o vector store

        Args:
            collection_name: Nome da coleção no ChromaDB
        """

        # Inicializa o ChromaDB em memória (para desenvolvimento)
        # Em produção, use persist_directory para salvar em disco
        self.client = chromadb.Client(
            Settings(anonymized_telemetry=False, allow_reset=True)
        )

        # Cria ou obtém a coleção
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Coleção de documentos para RAG"},
        )

        # Inicializa o modelo de embeddings
        # all-MiniLM-L6-v2 é um modelo leve e eficiente para embeddings
        print("🔄 Carregando modelo de embeddings...")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Modelo carregado!")

        # Contador para IDs únicos
        self.doc_counter = 0

    def add_documents(self, chunks: List[str], source: str):
        """
        Adiciona documentos ao vector store

        Args:
            chunks: Lista de chunks de texto
            source: Nome do arquivo fonte
        """

        # Cria embeddings para todos os chunks
        print(f"🔄 Criando embeddings para {len(chunks)} chunks...")
        embeddings = self.embedding_model.encode(chunks).tolist()

        # Prepara IDs e metadados
        ids = [f"doc_{self.doc_counter}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source, "chunk_id": i} for i in range(len(chunks))]

        # Adiciona ao ChromaDB
        self.collection.add(
            embeddings=embeddings, documents=chunks, metadatas=metadatas, ids=ids
        )

        self.doc_counter += 1
        print(f"✅ {len(chunks)} chunks adicionados ao vector store!")

    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Busca os chunks mais relevantes para uma query

        Args:
            query: Pergunta do usuário
            k: Número de resultados a retornar

        Returns:
            Lista de dicionários com texto, fonte e score de similaridade
        """

        # Cria embedding da query
        query_embedding = self.embedding_model.encode([query]).tolist()

        # Busca no ChromaDB
        results = self.collection.query(query_embeddings=query_embedding, n_results=k)

        # Formata os resultados
        formatted_results = []

        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append(
                    {
                        "text": doc,
                        "source": results["metadatas"][0][i]["source"],
                        "score": 1
                        - results["distances"][0][
                            i
                        ],  # Converte distância em similaridade
                    }
                )

        return formatted_results

    def get_document_count(self) -> int:
        """
        Retorna o número de chunks armazenados

        Returns:
            Número de documentos/chunks
        """
        return self.collection.count()

    def list_documents(self) -> List[str]:
        """
        Lista todos os documentos únicos no vector store

        Returns:
            Lista de nomes de arquivos
        """
        all_docs = self.collection.get()

        if not all_docs["metadatas"]:
            return []

        # Extrai fontes únicas
        sources = set([meta["source"] for meta in all_docs["metadatas"]])
        return list(sources)

    def clear(self):
        """
        Remove todos os documentos do vector store
        """
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(
            name=self.collection.name,
            metadata={"description": "Coleção de documentos para RAG"},
        )
        self.doc_counter = 0
