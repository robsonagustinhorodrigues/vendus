def encontrar_posicao_multiplos(busca, lista_mlbs, max_paginas, status_callback):
    from fake_useragent import UserAgent
    import requests
    from bs4 import BeautifulSoup

    ua = UserAgent()
    # headers = {'User-Agent': ua.random}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    base_url = "https://lista.mercadolivre.com.br/{}"
    busca_formatada = busca.replace(" ", "-")
    url = base_url.format(busca_formatada)
    encontrados = {}

    print(f"Buscando url: {url}")
    
    mlbs_upper = [mlb.strip().upper() for mlb in lista_mlbs]

    # Etapa 1: coletar todos os links das páginas
    links_filtrados = []
    for pagina in range(max_paginas):
        offset = pagina * 48
        pagina_url = f"{url}_Desde_{offset}" if pagina > 0 else url
        status_callback(f"Verificando página {pagina + 1}...")
        try:
            response = requests.get(pagina_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "lxml")
            todos_links = soup.select('a[href*="mercadolivre.com.br"]')
            links_filtrados.extend([
                link.get("href", "") for link in todos_links
                if "/p/" in link.get("href", "") or "/MLB" in link.get("href", "")
            ])
        except Exception as e:
            status_callback(f"Erro ao buscar página {pagina + 1}: {e}")
            
    print(f"Total de links coletados: {links_filtrados}")
    print(f"Total de MLBs a serem verificadas: {mlbs_upper}")

    # Etapa 2: verificar posição dos mlbs na lista completa de links
    for idx, href in enumerate(links_filtrados):
        for mlb in mlbs_upper:
            if mlb not in encontrados and mlb in href.replace("-", "").upper():
                encontrados[mlb] = {
                    "pagina": (idx // 48) + 1,
                    "posicao_na_pagina": (idx % 48) + 1,
                    "posicao_total": idx + 1,
                    "url": href
                }

    return encontrados