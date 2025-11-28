# src/collectors/steam/parser.py

def normalize_featured(payload: dict) -> dict:
    """
    Recebe o JSON bruto do endpoint featuredcategories e retorna uma versão
    normalizada. Por enquanto, devolve o payload original.
    """
    return payload

def parse_featured(data: dict) -> dict:
    """
    Normaliza o payload de 'featuredcategories' da Steam.
    Ajuste conforme a estrutura real do JSON.
    """
    # Exemplo simples: pega só os nomes das categorias
    categories = []
    for cat in data.get("featured_categories", []):
        categories.append({
            "id": cat.get("id"),
            "name": cat.get("name"),
            "items": cat.get("items", [])
        })
    return {"categories": categories}