import os
import requests
import datetime as dt

def get_featured_games():
    """
    Captura categorias em destaque da Steam.
    Retorna o dicionário JSON bruto da API (payload) ou levanta um erro HTTP.
    """
    base = os.getenv("STEAM_API_BASE", "https://store.steampowered.com")
    url = f"{base}/api/featuredcategories"
    headers = {"User-Agent": "steam-data-pipeline/1.0"}
    
    # Faz a requisição HTTP
    # Se falhar, r.raise_for_status() levantará uma exceção clara.
    r = requests.get(url, timeout=30, headers=headers)
    r.raise_for_status()
    
    # Retorna o JSON puro da API para o Bronze
    return r.json()

def now_iso():
    # Mantendo a função, pois pode ser usada em outras partes
    return dt.datetime.now(dt.timezone.utc).isoformat()