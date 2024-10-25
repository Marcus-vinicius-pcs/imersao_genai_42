import os
import requests
from groq import Groq
import google.generativeai as genai


GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)


def format_prompt(job_description: str) -> str:
    return f"""Você é um profissional de tecnologia da informação em busca de uma vaga como Cientista de Dados.
Você receberá uma descrição de vaga e deve extrair as seguintes informações da descrição da vaga:
- Nome do cargo
- Nome da empresa
- Regime de Horário
- Modelo de Trabalho
- Local do Trabalho
- Benefícios
- Salário
- Requisitos técnicos
- Principais responsabilidade do cargo
Você não deve responder o que não sabe, e caso não consiga identificar alguma informação retorne o campo preenchido como "Não Informado".

Exemplo de descrição da vaga: (
Sobre: O Banco Itaú tem uma tradição de 100 anos encantando clientes e inovando os processos.

O Engenheiro de Software será responsável por desenvolver o app do Itaú, realizar code reviews, desenvolver na AWS, gerar testes e gerenciar infraestrutura em cloud.

Requisitos e Qualificações:
Ensino Superior Completo
Python Avançado
Terraform básico
Inglês avançado

Salário: 278k por mês
Participação nos lucros
Vale refeição alimentação
Seguro de Vida
Plano de Saúde
Gympass

Presencial em São Paulo
)
Exemplo de resposta: (
- Nome do cargo: Engenheiro de Software
- Nome da empresa: Itaú
- Regime de Horário: Não Informado
- Modelo de Trabalho: Presencial
- Local do Trabalho: São Paulo
- Benefícios: Participação nos lucros, Vale refeição alimentação, Seguro de Vida, Plano de Saúde e Gympass
- Salário: R$278000,00
- Requisitos técnicos: Ensino Superior Completo, Python Avançado, Terraform básico, Inglês avançado
- Principais responsabilidade do cargo: desenvolver o app do Itaú, realizar code reviews, desenvolver na AWS, gerar testes e gerenciar infraestrutura em cloud.
)
Segue abaixo a descrição da vaga que você deve extrair as informações:
Descrição: {job_description}"""

def get_response_from_qwen(prompt: str) -> str:
    print("Obtendo resposta do Qwen")
    headers = {
        "Content-Type": "application/json",
    }
    url = "http://localhost:11434/api/generate"
    data = {
        "prompt": prompt,
        "model": "qwen2:1.5b",
        "stream": False
    }
    resp = requests.post(url=url, json=data, headers=headers)
    
    try:
        return resp.json()['response']
    except ValueError:
        print("Erro ao decodificar a resposta JSON.")
        return {}

def get_response_from_llama(prompt: str) -> str:
    print("Obtendo resposta do Llama")
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

def get_response_from_gemini(prompt: str) -> str:
    print("Obtendo resposta do Gemini")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def query_all_models(prompt):
    resp = {}
    resp['qwen2:1.5b'] = get_response_from_qwen(prompt)
    resp['llama3-8b-8192'] = get_response_from_llama(prompt)
    resp['gemini-1.5-flash"'] = get_response_from_gemini(prompt)
    return resp

def main():
    with open("ex01/job_description.txt", "r") as file:
        job_description = file.read()

    formatted_prompt = format_prompt(job_description)
    results = query_all_models(formatted_prompt)

    for model, response in results.items():
        print(f"\nAnálise do {model}:")
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    main()