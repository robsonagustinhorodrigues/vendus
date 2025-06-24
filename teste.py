import requests
from bs4 import BeautifulSoup

url = "https://lista.mercadolivre.com.br/mesa-passar"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# Mostra todos os links da página
links_filtrados = []
todos_links = soup.select('a[href*="mercadolivre.com.br"]')
links_filtrados.extend([
    link.get("href", "") for link in todos_links
    if "/p/" in link.get("href", "") or "/MLB" in link.get("href", "")
])
print("\n".join(links_filtrados[:20]))  # mostra os primeiros 20 para debug
