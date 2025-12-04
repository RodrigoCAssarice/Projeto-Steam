# src/collectors/steam/client.py

# A importação relativa expõe a função de api.py, permitindo que
# o __init__.py a acesse através do alias 'client'.
from .api import get_featured_games

# Este arquivo não precisa de mais nada, apenas garantir que a função 
# principal da API esteja acessível.