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
            .select("date_game,players_total,players_paid,players_visitors")
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

    def save(self, jogo: dict) -> None:
        """Save game data to Supabase"""
        self.supabase.table("games").insert(jogo, upsert=True).execute()

    def update(self, game_id: int, jogo: dict) -> None:
        """Update game data in Supabase"""
        self.supabase.table("games").update(jogo).eq("id", game_id).execute()
