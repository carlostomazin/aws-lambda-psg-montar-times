from dataclasses import asdict

from src.schemas import Jogo
from src.supabase_client import recuperar_jogos


def get_recupera_jogos() -> list[dict]:
    """Recuperar jogos armazenados"""
    try:
        jogos: list[dict] = recuperar_jogos()

    except Exception as e:
        return 500, {"error": f"Error retrieving games: {e}"}

    return 200, {"jogos": jogos}
