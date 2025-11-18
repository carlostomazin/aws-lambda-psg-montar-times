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
    """Retrieve game data from Supabase"""
    response = (
        supabase.table(TABLE_NAME)
        .select("date_game,players_total,players_paid,players_visitors")
        .execute()
    )
    jogos_data = response.data

    return jogos_data
