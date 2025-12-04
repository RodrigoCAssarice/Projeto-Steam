import json
from typing import Dict, Any, List
from datetime import datetime

def aggregate_featured_games(games_list: List[Dict[str, Any]], processing_time: str) -> List[Dict[str, Any]]:
    """
    Processa a lista PLANA de jogos (camada Silver) e cria uma 
    lista de registros prontos para análise (Camada Gold/Tabela Fato).
    """
    
    gold_records = []
    
    try:
        # 'games_list' é a lista PLANA de jogos
        
        for item in games_list: 
            
            if not isinstance(item, dict) or item.get("id") is None:
                continue
                
            original_price_cents = item.get("original_price")
            final_price_cents = item.get("final_price")
            category_name = item.get("category")
            
            # Cria o registro Gold (Fato)
            record = {
                "game_id": item.get("id"),
                "game_name": item.get("name"),
                "game_type": item.get("type"), 
                "is_discounted": item.get("discounted"),
                "discount_percent": item.get("discount_percent", 0),
                
                # Conversão para preço em R$ (dividir por 100)
                "original_price": original_price_cents / 100 if original_price_cents is not None else None,
                "final_price": final_price_cents / 100 if final_price_cents is not None else None,
                
                "category": category_name, 
                "source": item.get("source"),
                "capture_date_utc": item.get("captured_at"),
                "processing_date_utc": processing_time
            }
            gold_records.append(record)

    except Exception as e:
        print(f"Error processing silver data for Gold layer: {e}")
        return [] 
        
    return gold_records