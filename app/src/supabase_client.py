import os
from dataclasses import asdict

from dotenv import load_dotenv
from src.schemas import Jogo
from supabase import Client, create_client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

TABLE_NAME = "games"


def salvar_jogo(jogo: Jogo) -> None:
    """Save game data to Supabase"""
    jogo_dict = asdict(jogo)

    supabase.table(TABLE_NAME).insert(jogo_dict, upsert=True).execute()


def recuperar_jogos() -> list[dict]:
    """
    Retrieve game data from Supabase

    Returns:
    list[dict]: List of games
        date_game: str
        players_total: int
        players_paid: int
        players_visitors: int
    """
    response = (
        supabase.table(TABLE_NAME)
        .select("date_game,players_total,players_paid,players_visitors")
        .execute()
    )
    jogos_data = response.data

    return jogos_data


def recuperar_jogos_by_id(game_id: int) -> dict:
    """
    Retrieve a specific game data from Supabase by game ID

    Args:
        game_id (int): ID of the game to retrieve.
    Returns:
    dict: Game data
        date_game: str
        players: list[dict]
        teams: list[dict]
        players_total: int
        players_paid: int
        players_visitors: int
    """
    response = supabase.table(TABLE_NAME).select("*").eq("id", game_id).execute()
    jogo_data = response.data
    if jogo_data:
        return jogo_data[0]
    return {}
