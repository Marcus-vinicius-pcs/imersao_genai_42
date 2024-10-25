import sys
import requests
from dewiki.parser import Parser
import re

CLEANR = re.compile('<.*?>') 
URL =  "https://pt.wikipedia.org/w/api.php"

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def search_list_of_pages(query: str):
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 1
    }
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
    
def search_page_by_title(title: str):
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",  
        "explaintext": True
    }
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

def process_response(data, parser):
    try:
        if 'query' in data:
            page_id = next(iter(data['query']['pages']))
            page_info = data['query']['pages'][page_id]
            extract = page_info.get('extract')
            extract = parser.parse_string(extract)
            extract = cleanhtml(extract)
            return extract
        else:
            print("Nenhum resultado encontrado.")
            return None
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return None

def write_file(filename: str, data: str):
    if data:
        filename = f"{filename}.wiki"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(str(data))
        print(f"Arquivo {filename} criado")

def format_filename(query: str) -> str:
    return query.replace(" ", "_")

def process_and_save_page(data, parser):
    first_title = data['query']['search'][0]['title']
    filename = format_filename(first_title)
    page_data = search_page_by_title(first_title)
    snippet = process_response(page_data, parser)
    write_file(filename, snippet)

def main():
    parser = Parser()

    if len(sys.argv) < 2:
        print("Digite o termo de busca.")
        return
    
    query = sys.argv[1].strip()
    if not query:
        print("Termo de busca não pode ser vazio")
        return

    data = search_list_of_pages(query)
    
    if data:
        suggestion = data.get('query', {}).get('searchinfo', {}).get('suggestion')
        if suggestion:
            print(f"Você quis dizer: {suggestion}")
            data = search_list_of_pages(suggestion)

        process_and_save_page(data, parser)

if __name__ == "__main__":
    main()
