import re
import os
import google.generativeai as genai

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

def get_response_from_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        print("Requisição bem sucedida")
        return response.text
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None

def visao_geral() -> str:
    prompt = """
    <context>Você é um assistente e deve realizar a tarefa de <task>obter informações da vida de Claude Shannon</task>.</context>
    <instruction>
    Obtenha uma visão geral da vida de Claude Shannon e retorne em formato de texto que inicie com a tag <response></response>. 
    </instruction>
    <response>
    Sua resposta vai aqui
    </response>
    """
    return get_response_from_gemini(prompt)

def principais_contribuicoes(visao_geral: str) -> str:
    prompt = f"""
    <context>Você é um assistente e vai me ajudar a obter algumas informações sobre a vida de Claude Shannon.</context>
    <instruction>
    Você receberá um texto sobre a visão geral e, com base nesse texto e no conhecimento que você possui, você deve <task>fazer uma análise sobre suas principais contribuições para a teoria da informação</task> e retorne em formato de texto que inicie com a tag <response></response>.
    <texto visão geral>{visao_geral}</texto visão geral>
    </instruction>
    <response>
    Sua resposta vai aqui
    </response>
    """
    return get_response_from_gemini(prompt)

def impacto_trabalho(contribuicao: str) -> str:
    prompt = f"""
    <context>Você é um assistente e vai me ajudar a obter algumas informações sobre a vida de Claude Shannon.</context>
    <instruction>
    Com base nas contribuições e no conhecimento que você possui, você deve <task>explorar o impacto do trabalho de Claude Shannon na computação moderna e nas tecnologias de comunicação.</task> e retorne em formato de texto que inicie com a tag <response></response>.
    <texto contribuições>{contribuicao}</texto contribuições>
    </instruction>
    <response>
    Sua resposta vai aqui
    </response>
    """
    return get_response_from_gemini(prompt)

def analise_abraangente(visao_geral: str, contribuicoes: str, impacto: str) -> str:
    prompt = f"""
    <context>Você é um assistente e deve realizar a tarefa de <task>analisar a vida e o trabalho de Claude Shannon.</task></context>
    <instruction>
    Utilize a visão geral, as principais contribuições e o impacto de seu trabalho para <task>sintetizar uma análise abrangente.</task> e retorne em formato de texto que inicie com a tag <response></response>.
    <texto visão geral>{visao_geral}</texto visão geral>
    <texto contribuições>{contribuicoes}</texto contribuições>
    <texto impacto>{impacto}</texto impacto>
    </instruction>
    <response>
    Sua resposta vai aqui
    </response>
    """
    return get_response_from_gemini(prompt)

def run_prompt_chain():
    resp_1 = visao_geral()
    visao = extract_content(resp_1, 'response')
    if visao != '':
        print("Visão Geral obtida")
    
    resp_2 = principais_contribuicoes(visao)
    contribuicoes = extract_content(resp_2, 'response')
    if visao != '':
        print("Conttribuições obtida")
    
    resp_3 = impacto_trabalho(contribuicoes)
    impacto = extract_content(resp_3, 'response')
    if visao != '':
        print("Impacto obtida")
    
    resp_4 = analise_abraangente(visao, contribuicoes, impacto)
    analise = extract_content(resp_4, 'response')
    
    print("[resultado final do encadeamento, apresentando uma análise abrangente sobre Claude Shannon]\n\n")
    print(analise)

def extract_content(text, tag):
    pattern = f"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

if __name__ == "__main__":
    run_prompt_chain()
