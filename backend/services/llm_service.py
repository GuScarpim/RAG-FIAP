"""
SERVIÇO DE LLM (Large Language Model)
Gerencia a geração de respostas usando OpenAI GPT
"""

from openai import OpenAI
import os
import re
from typing import Tuple


class LLMService:
    """
    Serviço para interagir com a LLM (OpenAI GPT)

    Responsável por gerar respostas baseadas no contexto recuperado
    """

    def __init__(self):
        """
        Inicializa o serviço de LLM

        Nota: Requer a variável de ambiente OPENAI_API_KEY
        """

        # Obtém a API key do ambiente
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            print("\n" + "=" * 70)
            print("⚠️  MODO RAG SEM IA ATIVADO")
            print("=" * 70)
            print("OPENAI_API_KEY não encontrada.")
            print(
                "O sistema funcionará normalmente usando RAG (Recuperação de Contexto),"
            )
            print("mas sem geração de texto por IA.")
            print(
                "\nVocê ainda receberá respostas úteis baseadas no conteúdo dos PDFs!"
            )
            print("=" * 70 + "\n")
            self.client = None
        else:
            print("✅ OpenAI configurada - Respostas com IA ativadas")
            try:
                self.client = OpenAI(api_key=api_key)
            except Exception as e:
                print(f"❌ Erro ao inicializar OpenAI: {e}")
                print("🔄 Usando modo RAG sem IA")
                self.client = None

    def generate_answer(
        self,
        question: str,
        context: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> Tuple[str, int]:
        """
        Gera uma resposta usando a LLM com o contexto fornecido

        Args:
            question: Pergunta do usuário
            context: Contexto recuperado do vector store
            temperature: Controla a criatividade (0=determinístico, 2=criativo)
            max_tokens: Número máximo de tokens na resposta

        Returns:
            Tupla contendo (resposta, tokens_usados)
        """

        # Se não há cliente OpenAI, retorna resposta mock
        if not self.client:
            return self._generate_mock_answer(question, context), 0

        # Monta o prompt para a LLM
        system_prompt = """Você é um assistente especializado em responder perguntas baseado em documentos.

INSTRUÇÕES IMPORTANTES:
1. Use APENAS as informações fornecidas no contexto para responder
2. Se a resposta não estiver no contexto, diga "Não encontrei essa informação no documento"
3. Seja preciso e objetivo
4. Cite trechos relevantes quando apropriado
5. Não invente informações (evite alucinações)

CONFIGURAÇÕES DE ALUCINAÇÃO:
- Temperature: {temperature} (quanto menor, mais factual e determinístico)
- Sempre baseie suas respostas no contexto fornecido
- Se não tiver certeza, expresse isso claramente
"""

        user_prompt = f"""CONTEXTO DO DOCUMENTO:
{context}

PERGUNTA DO USUÁRIO:
{question}

RESPOSTA:"""

        try:
            # Chama a API da OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Modelo mais econômico
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt.format(temperature=temperature),
                    },
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9,  # Nucleus sampling para reduzir alucinações
                frequency_penalty=0.3,  # Reduz repetições
                presence_penalty=0.3,  # Incentiva novos tópicos
            )

            # Extrai a resposta
            answer = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            return answer, tokens_used

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Erro ao chamar OpenAI: {error_msg}")

            # Detecta erros específicos
            if "429" in error_msg or "quota" in error_msg.lower():
                print("💡 Cota da OpenAI excedida - Usando modo RAG sem IA")
            elif "401" in error_msg or "authentication" in error_msg.lower():
                print("💡 Erro de autenticação - Usando modo RAG sem IA")
            else:
                print("💡 Erro na API OpenAI - Usando modo RAG sem IA")

            # Retorna resposta usando apenas o contexto recuperado
            return self._generate_mock_answer(question, context), 0

    def _generate_mock_answer(self, question: str, context: str) -> str:
        """
        Gera uma resposta usando apenas o contexto recuperado (RAG sem IA)

        Args:
            question: Pergunta do usuário
            context: Contexto do documento

        Returns:
            Resposta formatada baseada no contexto
        """
        # Limpa caracteres especiais do PDF
        clean_context = self._clean_pdf_text(context)

        # Divide o contexto em parágrafos
        paragraphs = [p.strip() for p in clean_context.split("\n") if p.strip()]

        # Monta uma resposta formatada e legível
        response = f"""📄 RESPOSTA BASEADA NO DOCUMENTO (Modo RAG)

**Sua pergunta:** {question}

**Informações encontradas no documento:**

"""

        # Adiciona os parágrafos mais relevantes (até 1200 caracteres)
        char_count = 0
        max_chars = 1200

        for para in paragraphs:
            if char_count + len(para) > max_chars:
                break
            response += f"{para}\n\n"
            char_count += len(para)

        if char_count >= max_chars:
            response += "...\n\n"

        response += """---
💡 **Nota:** Esta resposta mostra diretamente o conteúdo recuperado do documento.
   Para respostas sintetizadas por IA, adicione créditos à sua conta OpenAI.
"""

        return response

    def _clean_pdf_text(self, text: str) -> str:
        """
        Limpa texto extraído de PDFs removendo caracteres especiais

        Args:
            text: Texto a ser limpo

        Returns:
            Texto limpo e formatado
        """
        if not text:
            return ""

        # Remove caracteres CID (comuns em PDFs)
        text = re.sub(r"\(cid:\d+\)", "•", text)

        # Remove múltiplos espaços
        text = re.sub(r" +", " ", text)

        # Remove múltiplas quebras de linha (mantém no máximo 2)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
