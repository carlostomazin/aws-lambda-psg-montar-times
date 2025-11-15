from src.schemas import Jogo
from src.supabase_client import recuperar_jogos


def get_recupera_jogos() -> list[Jogo]:
    """Retrieve games from Supabase"""
    try:
        jogos = recuperar_jogos()
    except Exception as e:
        return 500, {"error": f"Error retrieving games: {e}"}

    return 200, {"jogos": jogos}
