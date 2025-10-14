"""
SERVIÇO DE PROCESSAMENTO DE PDF
Responsável por extrair texto de PDFs e dividir em chunks para o RAG
"""

import pdfplumber
from typing import List, Tuple


class PDFProcessor:
    """
    Classe para processar arquivos PDF e extrair texto
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Inicializa o processador de PDF

        Args:
            chunk_size: Tamanho de cada chunk em caracteres
            chunk_overlap: Sobreposição entre chunks (para manter contexto)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_pdf(self, pdf_path: str) -> Tuple[List[str], int]:
        """
        Extrai texto de um PDF e divide em chunks

        Args:
            pdf_path: Caminho para o arquivo PDF

        Returns:
            Tupla contendo (lista de chunks, número de páginas)
        """

        # Extrai texto de todas as páginas
        full_text = ""
        num_pages = 0

        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)

            for page_num, page in enumerate(pdf.pages, 1):
                # Extrai texto da página
                text = page.extract_text()

                if text:
                    # Adiciona marcador de página para rastreabilidade
                    full_text += f"\n\n[Página {page_num}]\n{text}"

        # Divide o texto em chunks
        chunks = self._split_into_chunks(full_text)

        return chunks, num_pages

    def _split_into_chunks(self, text: str) -> List[str]:
        """
        Divide o texto em chunks com sobreposição

        A sobreposição é importante para manter o contexto entre chunks,
        evitando que informações importantes sejam cortadas.

        Args:
            text: Texto completo a ser dividido

        Returns:
            Lista de chunks de texto
        """
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            # Define o fim do chunk
            end = start + self.chunk_size

            # Se não é o último chunk, tenta quebrar em um espaço
            if end < text_length:
                # Procura o último espaço antes do limite
                last_space = text.rfind(" ", start, end)
                if last_space != -1:
                    end = last_space

            # Extrai o chunk
            chunk = text[start:end].strip()

            if chunk:  # Adiciona apenas chunks não vazios
                chunks.append(chunk)

            # Move o início para o próximo chunk (com sobreposição)
            start = end - self.chunk_overlap

        return chunks
