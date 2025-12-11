import logging
import json
import azure.functions as func
from datetime import datetime
import os
import glob
from pathlib import Path
import sys

# CRÍTICO: Configuração do PATH para encontrar o módulo 'src'
# Assegura que o módulo 'src' seja acessível, subindo para a pasta raiz do projeto.
# Ajuste o número de 'parent.parent...' se sua estrutura de pastas for diferente.
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

# Importação do módulo de processamento Gold
try:
    from src.processing.gold.aggregator import aggregate_featured_games
    logging.info("Módulo 'aggregate_featured_games' importado com sucesso.")
except ImportError as e:
    logging.error(f"ERRO DE IMPORTAÇÃO: {e}")
    # Função dummy para evitar quebrar o programa se o import falhar
    def aggregate_featured_games(data, time): return []


# FUNÇÃO PRINCIPAL: Usa 'timer' para corresponder ao function.json
def main(timer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().isoformat()
    processing_time = utc_timestamp
    logging.info('Python timer trigger function process_gold started at %s', processing_time)

    # 1. Configuração de Caminhos
    BASE_PATH = Path(__file__).resolve().parent.parent.parent
    SILVER_PATH = BASE_PATH / "src" / "processing" / "silver"
    GOLD_PATH = BASE_PATH / "gold_output" # Usamos 'gold_output' na raiz do projeto

    # 2. Cria pasta de saída Gold se não existir
    GOLD_PATH.mkdir(parents=True, exist_ok=True)
    
    # 3. Lista arquivos Silver disponíveis
    list_of_files = glob.glob(str(SILVER_PATH / "silver_featured_*.json"))

    if not list_of_files:
        logging.warning("Nenhum arquivo Silver encontrado para processamento Gold. Pulando.")
        return

    # Pega o arquivo criado mais recentemente (latest_file)
    latest_file = max(list_of_files, key=os.path.getctime)
    logging.info('Processando arquivo Silver mais recente: %s', latest_file)

    # 4. Lê o arquivo Silver (o Silver salva uma lista plana de jogos)
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            games_list = json.load(f)
            
            # Garante que é uma lista de jogos, se for um dict, ajusta a chave
            if isinstance(games_list, dict) and "items" in games_list:
                games_list = games_list.get("items", [])
            elif not isinstance(games_list, list):
                logging.error("Arquivo Silver não é uma lista válida de jogos.")
                games_list = []
            
    except Exception as e:
        logging.error(f"Erro ao ler arquivo Silver: {e}")
        return

    # 5. Processa os dados
    gold_records = aggregate_featured_games(games_list, processing_time)

    if not gold_records:
        logging.warning("A agregação Gold não retornou registros. Pulando a escrita.")
        return

    # 6. Salva o resultado agregado
    output_filename = f"gold_featured_facts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path = GOLD_PATH / output_filename

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(gold_records, f, indent=2, ensure_ascii=False)
        
        logging.info('Pipeline Gold finalizada. Registros salvos em: %s', output_path)
        logging.info("Execução de Functions.process_gold concluída.")
        
    except Exception as e:
        logging.error(f"Erro ao salvar arquivo Gold: {e}")