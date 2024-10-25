import os
import google.generativeai as genai

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

def format_prompt(text: str) -> str:
    return f"""
        <contexto>Você é um <função>analista de sentimentos</função> e tem tarefa de <tarefa>analisar sentimentos de comentários do Github</tarefa>.</contexto>
        <instrução>Você deve classificar se o comentário reforça um sentimento NEGATIVO ou POSITIVO. Não responda nada além do sentimento</instrução> Abaixo seguem alguns exemplos sobre a classificação de sentimentos:
        <exemplo>
        Texto: "O desempenho deste sistema melhorou significativamente com a última atualização. Estou impressionado!"
        Sentimento: POSITIVO
        </exemplo>
        <exemplo>
        Texto: "Essa alteração introduziu vários erros que precisamos corrigir rapidamente. A situação está crítica."
        Sentimento: NEGATIVO
        </exemplo>
        Texto: "A equipe fez um ótimo trabalho ao resolver esse problema. A solução foi rápida e eficaz!"
        Sentimento: POSITIVO
        <exemplo>
        Texto: "Ainda não recebi resposta sobre a minha solicitação. Isso está atrasando nosso progresso."
        Sentimento: NEGATIVO
        </exemplo>
        <exemplo>
        Texto: "Adorei a nova funcionalidade! Ela realmente melhora a experiência do usuário."
        Sentimento: POSITIVO
        </exemplo>
        Aqui vai o Texto: {text}
        </instrução>
    """

def call_llm(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(text)
    return response.text

def parse_llm_response(response):
    return response.strip()


def analyze_sentiments(comments):
    for comment in comments:
        prompt = format_prompt(comment["text"])
        llm_response = call_llm(prompt)
        comment["sentiment"] = parse_llm_response(llm_response)


def main():
    github_comments = [
        {
            "text": "Ótimo trabalho na implementação desta feature! O código está limpo e bem documentado. Isso vai ajudar muito nossa produtividade.",
            "sentiment": ""
        },
        {
            "text": "Esta mudança quebrou a funcionalidade X. Por favor, reverta o commit imediatamente.",
            "sentiment": ""
        },
        {
            "text": "Podemos discutir uma abordagem alternativa para este problema? Acho que a solução atual pode causar problemas de desempenho no futuro.",
            "sentiment": ""
        },
        {
            "text": "Obrigado por relatar este bug. Vou investigar e atualizar a issue assim que tiver mais informações.",
            "sentiment": ""
        },
        {
            "text": "Este pull request não segue nossas diretrizes de estilo de código. Por favor, revise e faça as correções necessárias.",
            "sentiment": ""
        },
        {
            "text": "Excelente ideia! Isso resolve um problema que estávamos enfrentando há semanas. Mal posso esperar para ver isso implementado.",
            "sentiment": ""
        },
        {
            "text": "Esta issue está aberta há meses sem nenhum progresso. Podemos considerar fechá-la se não for mais relevante?",
            "sentiment": ""
        },
        {
            "text": "O novo recurso está causando conflitos com o módulo Y. Precisamos de uma solução urgente para isso.",
            "sentiment": ""
        },
        {
            "text": "Boa captura! Este edge case não tinha sido considerado. Vou adicionar testes para cobrir este cenário.",
            "sentiment": ""
        },
        {
            "text": "Não entendo por que estamos priorizando esta feature. Existem problemas mais críticos que deveríamos estar abordando.",
            "sentiment": ""
        }
    ]

    analyze_sentiments(github_comments)
    # Imprimir resultados
    for comment in github_comments:
        print(f"Texto: {comment['text']}")
        print(f"Sentimento: {comment['sentiment']}")
        print("-" * 50)


if __name__ == "__main__":
    main()