import json
from typing import Dict, Any, List
from datetime import datetime

def aggregate_featured_games(silver_data: Dict[str, Any], processing_time: str) -> List[Dict[str, Any]]:
    """
    Processa os dados estruturados da camada Silver e cria uma 
    lista de registros prontos para análise (Camada Gold/Tabela Fato).
    
    A partir dos dados de 'featured_categories' da Steam, criamos
    um registro por jogo em destaque, adicionando metadados de captura.
    """
    
    gold_records = []
    
    try:
        data = silver_data.get("data", {})
        
        # O payload Silver da Steam é uma lista de categorias (specials, topsellers, etc.)
        featured_categories = data.get("featured_categories", [])
        
        # Itera sobre cada categoria (ex: 'Specials', 'Top Sellers')
        for category in featured_categories:
            category_name = category.get("name", "N/A")
            
            # Itera sobre cada jogo/item dentro da categoria
            for item in category.get("items", []):
                
                # Campos básicos do jogo
                record = {
                    "game_id": item.get("id"),
                    "game_name": item.get("name"),
                    "game_type": item.get("type"), # 0 para jogo, 1 para DLC, etc.
                    "is_discounted": item.get("discounted"),
                    "discount_percent": item.get("discount_percent", 0),
                    
                    # Preços (convertidos de centavos para moeda, se existirem)
                    # Usa get() para evitar KeyErrors e None checks
                    original_price_cents = item.get("original_price")
                    final_price_cents = item.get("final_price")
                    
                    "original_price": original_price_cents / 100 if original_price_cents is not None else None,
                    "final_price": final_price_cents / 100 if final_price_cents is not None else None,
                    
                    # Metadados de contexto
                    "category": category_name,
                    "source": silver_data.get("source"),
                    "capture_date_utc": silver_data.get("captured_at"),
                    "processing_date_utc": processing_time
                }
                gold_records.append(record)
                
    except Exception as e:
        # Em produção, você registraria o erro
        print(f"Error processing silver data for Gold layer: {e}")
        return []
        
    return gold_records

# Bloco para teste local
if __name__ == "__main__":
    # Simula um dado Silver bem formatado (estrutura simplificada)
    sample_silver = {
        "source": "steam",
        "endpoint": "featuredcategories",
        "captured_at": "2025-11-28T10:00:00+00:00",
        "data": {
            "featured_categories": [
                {
                    "name": "Specials",
                    "items": [
                        {
                            "id": 12345,
                            "type": 0,
                            "name": "Game A",
                            "discounted": True,
                            "discount_percent": 50,
                            "original_price": 4000,
                            "final_price": 2000
                        },
                        {
                            "id": 67890,
                            "type": 0,
                            "name": "Game B (Full Price)",
                            "discounted": False,
                            "discount_percent": 0,
                            "original_price": 6000,
                            "final_price": 6000
                        }
                    ]
                },
                {
                    "name": "Top Sellers",
                    "items": [
                        {
                            "id": 11223,
                            "type": 0,
                            "name": "Game C",
                            "discounted": True,
                            "discount_percent": 10,
                            "original_price": 1000,
                            "final_price": 900
                        }
                    ]
                }
            ]
        }
    }
    
    current_time = datetime.utcnow().isoformat()
    result = aggregate_featured_games(sample_silver, current_time)
    print(f"Registros Gold gerados: {len(result)}")
    print(json.dumps(result, indent=2))