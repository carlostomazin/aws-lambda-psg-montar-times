# supabse_client.py
import os
from dataclasses import asdict

from src.schemas import Jogo
from supabase import Client, create_client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def salvar_jogo(jogo: Jogo) -> None:
    """Save game data to Supabase"""
    jogo_dict = asdict(jogo)

    supabase.table("jogos").insert(jogo_dict, upsert=True).execute()


def recuperar_jogos() -> list[Jogo]:
    """Retrieve game data from Supabase"""
    response = supabase.table("jogos").select("*").execute()
    jogos_data = response.data

    jogos = [Jogo(**jogo) for jogo in jogos_data]
    return jogos
