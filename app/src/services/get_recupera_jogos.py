from dataclasses import asdict

from src.schemas import Jogo
from src.supabase_client import recuperar_jogos


def get_recupera_jogos() -> list[dict]:
    """Recuperar jogos armazenados"""
    try:
        jogos: list[Jogo] = recuperar_jogos()
        jogos = [asdict(jogo) for jogo in jogos]

    except Exception as e:
        return 500, {"error": f"Error retrieving games: {e}"}

    return 200, {"jogos": jogos}
