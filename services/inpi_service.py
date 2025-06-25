import requests

class InpiService:
    BASE = "https://busca.inpi.gov.br/Marca/servlet"

    def buscar_marca(self, termo, ncl=None, tipo='R', pagina=1):
        params = {"marca": termo, "pagina": pagina, "tipo": tipo}
        if ncl:
            params["ncl"] = ncl

        resp = requests.get(f"{self.BASE}/Pesquisa_classe_basica.jsp", params=params)
        resp.raise_for_status()

        # Tenta interpretar como JSON, mas faz fallback para texto
        content_type = resp.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return resp.json()
        else:
            return {"html": resp.text}  # ou usar BeautifulSoup se necessário
