import requests
from bs4 import BeautifulSoup

class InpiService:
    BASE_URL = "https://busca.inpi.gov.br"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        })

    def buscar_marcas(self, termo, pagina=1):
        try:
            print(f"🔍 Iniciando busca por marcas: {termo} (página {pagina})")
            url = f"{self.BASE_URL}/pePI/servlet/PesquisaMarcas"
            params = {"marcas": termo, "pagina": pagina}

            print(f"🔍 Buscando marcas: {termo} (página {pagina})")
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            tabela = soup.select_one("table.tabelaResultado")
            resultados = []

            if not tabela:
                print("⚠️ Nenhuma tabela de resultados encontrada.")
                return resultados

            linhas = tabela.select("tr")[1:]  # Ignora o cabeçalho
            for tr in linhas:
                tds = tr.find_all("td")
                if len(tds) >= 5:
                    link = tr.find("a", href=True)
                    resultados.append({
                        "numeroPedido": tds[0].get_text(strip=True),
                        "marca": tds[1].get_text(strip=True),
                        "classe": tds[2].get_text(strip=True),
                        "titular": tds[3].get_text(strip=True),
                        "situacao": tds[4].get_text(strip=True),
                        "linkDetalhes": link["href"] if link else ""
                    })

            print(f"✅ {len(resultados)} resultados encontrados.")
            return resultados

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição: {e}")
            raise

        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            raise

    def detalhes_marca(self, link_relativo):
        try:
            url = f"{self.BASE_URL}{link_relativo}"
            print(f"🔍 Buscando detalhes: {url}")

            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            tabela = soup.select_one("table.detalhesMarca")
            detalhes = {}

            if not tabela:
                print("⚠️ Nenhuma tabela de detalhes encontrada.")
                return detalhes

            for tr in tabela.select("tr"):
                tds = tr.find_all("td")
                if len(tds) >= 2:
                    chave = tds[0].get_text(strip=True).rstrip(":")
                    valor = tds[1].get_text(strip=True)
                    detalhes[chave] = valor

            print(f"✅ {len(detalhes)} campos encontrados.")
            return detalhes

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição de detalhes: {e}")
            raise

        except Exception as e:
            print(f"❌ Erro inesperado nos detalhes: {e}")
            raise
