# src/collectors/steam/Schemas/featured_schema.py

SCHEMA_FEATURED_GAME = {
    # GAME_ID é CRÍTICO para a desduplicação e deve ser OBRIGATÓRIO
    "game_id": {"type": int, "required": True, "description": "ID único do jogo na Steam."},
    
    # Tornando os demais campos NÃO OBRIGATÓRIOS (False) para não descartar dados
    # se a API falhar em enviar alguma informação (ex: preço)
    "game_name": {"type": str, "required": False, "description": "Nome do jogo."},
    "game_type": {"type": int, "required": False, "description": "Tipo de item (0 para jogo, 1 para DLC, etc)."},
    "is_discounted": {"type": bool, "required": False, "description": "Se o jogo está ou não com desconto."},
    "discount_percent": {"type": int, "required": False, "description": "Percentual de desconto (0-100)."},
    "original_price": {"type": float, "required": False, "description": "Preço original."},
    "final_price": {"type": float, "required": False, "description": "Preço final após desconto."},
    "category": {"type": str, "required": False, "description": "Categoria da Steam (e.g., specials, top_sellers)."},
    
    # Metadados adicionados pelo pipeline (Silver) - estes são gerados, não da API
    "source": {"type": str, "required": False},
    "endpoint": {"type": str, "required": False},
    "captured_at": {"type": str, "required": False},
    "normalized_at": {"type": str, "required": False},
}