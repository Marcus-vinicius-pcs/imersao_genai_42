import sys
import requests
from bs4 import BeautifulSoup
import re

URL = "https://en.wikipedia.org/wiki/"

def make_request(query):
    try:
        response = requests.get(URL + query)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error: {e}. Unable to continue.")
        sys.exit(1)

def is_valid_link(link):
    """Verifica se o link é válido para seguimento."""
    if link.find_parent(['table']):
        return False
    if link.find_parent(['i', 'em', 'sup', 'small']):
        return False
    if link.find(['i', 'em', 'sup', 'small']):
        return False
    pattern = r'^\(.*\)$'  # (link), não considera (texto link)
    if re.match(pattern, link.text):
        return False

    href = link['href']
    return href.startswith('/wiki/') and not any(x in href for x in [':', '#'])

def get_first_valid_link(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    title = soup.title.string.replace(" - Wikipedia", "") if soup.title else "Título não encontrado"
    print(title)
    
    content_div = soup.find('div', id='mw-content-text')
    if not content_div:
        return None
    
    for hatnote in content_div.find_all(class_='hatnote'):
        hatnote.decompose()

    paragraphs = content_div.find_all('p')
    found_link = False
    
    for paragraph in paragraphs:
        links = paragraph.find_all('a', href=True)
        if links:
            found_link = True
            for link in links:
                if is_valid_link(link):
                    return link['href']
    
    if not found_link:
        all_elements = content_div.find_all(True)
        for element in all_elements:
            links = element.find_all('a', href=True)
            for link in links:
                if is_valid_link(link):
                    return link['href']
    
    return None

def fetch_and_follow_links(query):
    current_query = query
    visited = set()
    roads_count = 0 

    while True:
        html_content = make_request(current_query)
        first_valid_link = get_first_valid_link(html_content)
        roads_count += 1

        if first_valid_link:
            full_link = f"https://en.wikipedia.org{first_valid_link}"
            if "Philosophy" in full_link:
                print(f"{roads_count} roads from {query} to philosophy!")
                return full_link
            
            next_query = first_valid_link.replace('/wiki/', '')
            
            if next_query in visited:
                print("It leads to an infinite loop!")
                break
            
            visited.add(next_query)
            current_query = next_query
            
        else:
            print("It leads to a dead end!")
            break

def main():
    if len(sys.argv) < 2:
        print("Digite o termo de busca.")
        return
    
    query = sys.argv[1].strip()
    if not query:
        print("Termo de busca não pode ser vazio")
        return
    fetch_and_follow_links(query)

if __name__ == "__main__":
    main()
