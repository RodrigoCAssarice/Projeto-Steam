# src/collectors/steam/schemas.py

def validate_envelope(obj: dict) -> None:
    """
    Valida o envelope de saída: source, endpoint, captured_at, data.
    Lança ValueError se algo essencial estiver faltando.
    """
    required = ["source", "endpoint", "captured_at", "data"]
    missing = [k for k in required if k not in obj or obj[k] is None]
    if missing:
        raise ValueError(f"Envelope inválido, faltando campos: {', '.join(missing)}")