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
        data_jogo: str
        jogadores_totais: int
        jogadores_pagantes: int
        jogadores_visitantes: int
    """
    response = (
        supabase.table(TABLE_NAME)
        .select("date_game,players_total,players_paid,players_visitors")
        .execute()
    )
    jogos_data = response.data

    # para portugues
    for jogo in jogos_data:
        jogo["data_jogo"] = jogo.pop("date_game")
        jogo["jogadores_totais"] = jogo.pop("players_total")
        jogo["jogadores_pagantes"] = jogo.pop("players_paid")
        jogo["jogadores_visitantes"] = jogo.pop("players_visitors")

    return jogos_data
