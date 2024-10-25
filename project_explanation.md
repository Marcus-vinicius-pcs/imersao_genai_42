# Análise de currículos com RAG

## Visão geral do sistema
Este sistema é uma aplicação de análise de currículos que utiliza técnicas de Retrieval-Augmented Generation (RAG) para processar e analisar currículos em formato PDF. O sistema permite que usuários façam upload de currículos, armazene-os em um banco de dados vetorial, e faça perguntas sobre os candidatos com base nas informações extraídas dos currículos.

## Componentes principais

1. Processador de PDF
   - Responsável por extrair texto de arquivos PDF usando a biblioteca PyMuPDF (fitz).

2. Embedding Generator
   - Utiliza o modelo SentenceTransformer para gerar embeddings a partir do texto extraído dos currículos.

3. Banco de Dados Vetorial
   - Implementado usando Chroma DB para armazenar e recuperar documentos e seus embeddings.

4. Mecanismo de Recuperação
   - Realiza consultas no banco de dados vetorial para recuperar documentos relevantes com base em uma pergunta do usuário.

5. Gerador de Respostas
   - Utiliza o modelo LLaMA 3 através da API Groq para gerar respostas às perguntas dos usuários com base nos documentos recuperados.

6. Interface de Usuário
   - Implementada usando Streamlit para permitir o upload de currículos e a interação com o sistema.

## Conceitos principais

- RAG (Retrieval-Augmented Generation): Técnica que combina a recuperação de informações relevantes com a geração de texto para produzir respostas mais precisas e contextualizadas.
- Embeddings: Representações vetoriais de texto que capturam significado semântico, usadas para comparar e recuperar documentos similares.
- Banco de Dados Vetorial: Sistema de armazenamento otimizado para busca e recuperação eficiente de vetores de alta dimensão.
- Modelo de Linguagem: Sistema de IA treinado para entender e gerar texto em linguagem natural, neste caso, o LLaMA 3.

## Fluxo de funcionamento

1. O usuário faz upload de currículos em PDF através da interface Streamlit.
2. Cada PDF é processado, extraindo seu texto e gerando embeddings.
3. Os documentos e seus embeddings são armazenados no banco de dados Chroma.
4. O usuário faz uma pergunta sobre os candidatos.
5. O sistema recupera documentos relevantes do banco de dados com base na pergunta.
6. Um prompt é gerado combinando a pergunta e os documentos recuperados.
7. O prompt é enviado ao modelo LLaMA 3 através da API Groq.
8. A resposta gerada pelo modelo é exibida ao usuário na interface Streamlit.

Este sistema permite uma análise eficiente e contextualizada de múltiplos currículos, auxiliando profissionais de RH em suas tarefas de recrutamento e seleção.