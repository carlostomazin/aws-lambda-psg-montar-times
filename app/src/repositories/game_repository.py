import os

from supabase import Client, create_client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")


class GameRepository:
    def __init__(self):
        self.supabase: Client = create_client(url, key)

    def find_all(self):
        response = (
            self.supabase.table("games")
            .select("id,date_game,players_total,players_paid,players_visitors")
            .execute()
        )
        jogos_data = response.data
        return jogos_data

    def find_by_id(self, game_id: int):
        response = self.supabase.table("games").select("*").eq("id", game_id).execute()
        jogo_data = response.data
        if jogo_data:
            return jogo_data[0]
        return None

    def find_by_date_game(self, game_date: str):
        response = (
            self.supabase.table("games")
            .select("*")
            .eq("date_game", game_date)
            .execute()
        )
        jogo_data = response.data
        if jogo_data:
            return jogo_data[0]
        return None

    def save(self, jogo: dict) -> dict:
        """Save game data to Supabase"""
        response = self.supabase.table("games").insert(jogo).execute()
        return response.data

    def update(self, game_id: int, jogo: dict) -> dict:
        """Update game data in Supabase"""
        response = self.supabase.table("games").update(jogo).eq("id", game_id).execute()
        return response.data
