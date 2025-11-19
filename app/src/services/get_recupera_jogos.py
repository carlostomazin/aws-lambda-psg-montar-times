from src.supabase_client import recuperar_jogos


def get_recupera_jogos(date: str = None) -> list[dict]:
    """Recuperar jogos armazenados"""
    try:
        if date:
            jogos = recuperar_jogos(data=date)
        else:
            jogos = recuperar_jogos()

    except Exception as e:
        return 500, {"error": f"Error retrieving games: {e}"}

    return 200, {"jogos": jogos}
