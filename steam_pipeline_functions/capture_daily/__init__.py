import os
import json
import datetime as dt
import azure.functions as func
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv(dotenv_path=Path("config/dev/.env"))

def _now_iso():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def _capture_steam_featured():
    base = os.getenv("STEAM_API_BASE", "https://store.steampowered.com")
    url = f"{base}/api/featuredcategories"
    headers = {"User-Agent": "steam-data-pipeline/1.0"}
    r = requests.get(url, timeout=30, headers=headers)
    r.raise_for_status()
    payload = r.json()
    return {
        "source": "steam",
        "endpoint": "featuredcategories",
        "captured_at": _now_iso(),
        "data": payload
    }

def main(timer: func.TimerRequest) -> None:
    # Decide alvos de captura
    targets = os.getenv("CAPTURE_TARGETS", "steam").split(",")

    results = []
    if "steam" in [t.strip() for t in targets]:
        try:
            results.append(_capture_steam_featured())
        except Exception as e:
            results.append({
                "source": "steam",
                "error": str(e),
                "captured_at": _now_iso()
            })

    # Persistência inicial em arquivo local (bronze/raw local)
    #out_dir = Path("src/processing/bronze")
    out_dir = Path(__file__).resolve().parents[2] / "src" / "processing" / "bronze"
    out_dir.mkdir(parents=True, exist_ok=True)
    outfile = out_dir / f"raw_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with outfile.open("w", encoding="utf-8") as f:
        json.dump({"items": results}, f, ensure_ascii=False, indent=2)

    print(f"[capture_daily] wrote {outfile}")