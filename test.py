import requests
import json

# Define os tokens de autenticação para cada papel
CANDIDATO_TOKEN = "candidato_token"
RECRUTADOR_TOKEN = "recrutador_token"
ADMINISTRADOR_TOKEN = "administrador_token"

# URL da API
API_URL = "http://localhost:5000"

# Função para enviar requisições POST com autenticação
def post_request(endpoint, data=None, files=None, token=CANDIDATO_TOKEN):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{API_URL}/{endpoint}', headers=headers, data=data, files=files)
    return response

# Função para enviar requisições GET com autenticação
def get_request(endpoint, params=None, token=CANDIDATO_TOKEN):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{API_URL}/{endpoint}', headers=headers, params=params)
    return response

# Função para enviar requisições DELETE com autenticação
def delete_request(endpoint, token=ADMINISTRADOR_TOKEN):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f'{API_URL}/{endpoint}', headers=headers)
    return response

# Testando upload de PDF
print("Testando upload de PDF...")
with open('./curriculo_1.pdf', 'rb') as file:
    response = post_request('upload_pdf', files={'file': file}, token=CANDIDATO_TOKEN)
print(f'Status code: {response.status_code}')
print(f'Resposta: {response.json()}')

# Testando busca semântica
print("\nTestando busca semântica...")
response = get_request('search', params={'query': 'python'}, token=RECRUTADOR_TOKEN)
print(f'Status code: {response.status_code}')
print(f'Resposta: {json.dumps(response.json(), indent=4)}')

# Testando exclusão de currículo
print("\nTestando exclusão de currículo...")
response = delete_request('curriculum/123', token=ADMINISTRADOR_TOKEN)
print(f'Status code: {response.status_code}')
print(f'Resposta: {response.json()}')

# Testando exclusão de currículo com token de candidato
print("\nTestando exclusão de currículo com token de candidato...")
response = delete_request('curriculum/123', token=CANDIDATO_TOKEN)
print(f'Status code: {response.status_code}')
print(f'Resposta: {response.json()}')
