import os
import google.generativeai as genai

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

def create_prompt(role: str, task: str, topic: str, specific_question: str) -> str:
    return f"""<contexto>Você é um <função>{role}</função> e tem tarefa de <tarefa>{task}</tarefa>.</contexto>
    <instrução>Sobre o tópico <tópico>{topic}</tópico> responda à pergunta <questão>{specific_question}</questão> no formato abaixo:
    - 1. Explicação básica do conceito:
    - 2. Analogia do cotidiano:
    - 3. Solução passo a passo da pergunta:
    - 4. Exemplo detalhado:
    - 5. Dica prática para iniciantes:</instrução>
    """

def send_to_gemini(prompt: str) -> str:
    print("Obtendo resposta do Gemini")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def main():
    role = "especialista em filosofia e história da ciência"
    task = "explicar o pensamento de Descartes e sua influência para iniciantes em filosofia"
    topic = "René Descartes e o Método Cartesiano"
    specific_question = "Quem foi René Descartes e qual é o significado da frase 'Penso, logo existo'?"
    prompt = create_prompt(role, task, topic, specific_question)
    response = send_to_gemini(prompt)
    print("\nResposta do Gemini 1.5 Flash:")
    print(response)

    role = "assistente especializado em ensinar programação Python para iniciantes"
    task = "explicar conceitos básicos de Python e fornecer exemplos simples e práticos"
    topic = "list comprehensions em Python"
    specific_question = "O que é uma list comprehension e como posso usá-la para criar uma lista de números pares de 0 a 10?"
    prompt = create_prompt(role, task, topic, specific_question)
    response = send_to_gemini(prompt)
    print("\nResposta do Gemini 1.5 Flash:")
    print(response)

    role = "especialista em métodos de educação inovadores em tecnologia"
    task = "explicar o conceito e a abordagem única da École 42 para interessados em educação em tecnologia"
    topic = "École 42 e seu método de ensino"
    specific_question = "O que é a École 42 e como seu método de ensino difere das faculdades tradicionais de computação?"
    prompt = create_prompt(role, task, topic, specific_question)
    response = send_to_gemini(prompt)
    print("\nResposta do Gemini 1.5 Flash:")
    print(response)

    role = "historiador da ciência da computação e teoria da informação"
    task = "explicar a importância de Claude Shannon e suas contribuições para iniciantes em ciência da computação"
    topic = "Claude Shannon e a Teoria da Informação"
    specific_question = "Quem foi Claude Shannon e qual foi sua principal contribuição para a ciência da computação e comunicação?"
    prompt = create_prompt(role, task, topic, specific_question)
    response = send_to_gemini(prompt)
    print("\nResposta do Gemini 1.5 Flash:")
    print(response)


if __name__ == "__main__":
    main()