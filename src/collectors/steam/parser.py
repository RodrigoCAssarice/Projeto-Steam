# src/collectors/steam/parser.py

def normalize_featured(payload: dict) -> dict:
    """
    Recebe o JSON bruto do endpoint featuredcategories e retorna uma versão
    normalizada. Por enquanto, devolve o payload original.
    """
    return payload