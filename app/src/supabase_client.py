import os
from dataclasses import asdict

from dotenv import load_dotenv
from schemas import Jogo
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


def recuperar_jogos() -> list[str]:
    """Retrieve game data from Supabase"""
    response = supabase.table(TABLE_NAME).select("date_game").execute()
    jogos_data = response.data
    jogos = [jogo["date_game"] for jogo in jogos_data]

    return jogos
