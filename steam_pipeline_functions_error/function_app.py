import azure.functions as func
import logging
import os
import json
from datetime import datetime

app = func.FunctionApp()

# Função Bronze: captura diária
@app.function_name(name="capture_daily")
@app.timer_trigger(schedule="0 0 12 * * *", arg_name="timer", run_on_startup=False, use_monitor=True)
def capture_daily(timer: func.TimerRequest) -> None:
    logging.info("capture_daily disparada às 12h")

    # Exemplo de captura de dados brutos (mock)
    raw_data = {
        "source": "steam_api",
        "endpoint": "featured",
        "captured_at": datetime.utcnow().isoformat(),
        "payload": {"games": ["game1", "game2", "game3"]}
    }

    # Salva na camada bronze
    bronze_dir = os.path.join("src", "processing", "bronze")
    os.makedirs(bronze_dir, exist_ok=True)

    filename = f"raw_featured_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(bronze_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    logging.info(f"[capture_daily] wrote {filepath}")


# Função Silver: processa bronze em silver
@app.function_name(name="process_silver")
@app.timer_trigger(schedule="0 */5 * * * *", arg_name="timer", run_on_startup=False, use_monitor=True)
def process_silver(timer: func.TimerRequest) -> None:
    logging.info("process_silver disparada a cada 5 minutos")

    bronze_dir = os.path.join("src", "processing", "bronze")
    silver_dir = os.path.join("src", "processing", "silver")
    os.makedirs(silver_dir, exist_ok=True)

    # Procura arquivos bronze
    bronze_files = [f for f in os.listdir(bronze_dir) if f.endswith(".json")]
    if not bronze_files:
        logging.info("[process_silver] no bronze files found")
        return

    # Carrega o mais recente
    latest_file = max(bronze_files, key=lambda f: os.path.getctime(os.path.join(bronze_dir, f)))
    latest_path = os.path.join(bronze_dir, latest_file)

    with open(latest_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # Transforma em silver (exemplo simples)
    silver_data = {
        "source": raw_data.get("source", "unknown"),
        "endpoint": raw_data.get("endpoint", "unknown"),
        "captured_at": raw_data.get("captured_at", datetime.utcnow().isoformat()),
        "games": raw_data.get("payload", {}).get("games", [])
    }

    filename = f"silver_featured_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(silver_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(silver_data, f, ensure_ascii=False, indent=2)

    logging.info(f"[process_silver] wrote {filepath}")