import json
from typing import Dict, Any, List
from datetime import datetime
import logging 

# Importações de bibliotecas pesadas (como pandas) foram removidas para evitar
# o 'ImportError' que estava ativando a função dummy no __init__.py.

def aggregate_featured_games(games_list: List[Dict[str, Any]], processing_time: str) -> List[Dict[str, Any]]:
    """
    Processa a lista PLANA de jogos (camada Silver) e cria uma 
    lista de registros prontos para análise (Camada Gold/Tabela Fato).
    """
    
    gold_records = []
    
    if not games_list:
        logging.warning("Lista de jogos Silver vazia para agregação Gold.")
        return []

    try:
        for item in games_list: 
            
            # 1. Garante que o registro é válido (tem o ID obrigatório)
            game_id = item.get("game_id")
            if not isinstance(item, dict) or game_id is None:
                continue
                
            # 2. Cria o registro Gold (Fato): 
            record = {
                "fact_id": f"{game_id}_{processing_time}", # Chave única do registro de fato
                "game_id": game_id,
                
                # Mapeamento de campos (usa o nome EXATO do Silver)
                "game_name": item.get("game_name"), 
                "game_type": item.get("game_type"), 
                
                # Métricas
                "is_discounted": item.get("is_discounted"),
                "discount_percent": item.get("discount_percent", 0),
                "original_price": item.get("original_price"), 
                "final_price": item.get("final_price"), 
                
                # Dimensões e Metadados
                "category": item.get("category"), 
                "source": item.get("source"),
                "capture_date_utc": item.get("captured_at"),
                "processing_date_utc": processing_time
            }
            
            gold_records.append(record)

    except Exception as e:
        # Se houver uma falha crítica, loga o erro.
        logging.error(f"Error CRÍTICO no Gold ao processar um registro: {e}")
        return [] 
        
    logging.info(f"Gold Aggregation: {len(gold_records)} registros de fato gerados.")
    return gold_records