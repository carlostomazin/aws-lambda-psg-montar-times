from dataclasses import asdict

from aws_lambda_powertools import Logger
from emoji import replace_emoji
from postgrest import APIError
from src.extrair_jogadores_json import extrair_jogadores_json
from src.montar_times import montar_times
from src.schemas import Game, Times
from src.utils import calcular_data_jogo

logger = Logger()


class GameService:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self) -> tuple[int, dict]:
        try:
            games = self.repository.find_all()
            return 200, {"games": games}
        except Exception as e:
            logger.error(f"Error retrieving games: {e}")
            return 500, {"error": "Error retrieving games"}

    def get_by_id(self, game_id: str) -> tuple[int, dict]:
        try:
            game = self.repository.find_by_id(game_id)
            if game:
                return 200, game
            else:
                return 404, {"error": "Game not found"}
        except Exception as e:
            logger.error(f"Error retrieving game by id {game_id}: {e}")
            return 500, {"error": "Error retrieving game"}

    def create(self, payload: dict) -> tuple[int, dict]:
        payload["jogadores_raw"] = replace_emoji(payload["jogadores_raw"], replace="")

        jogadores = extrair_jogadores_json(payload["jogadores_raw"])
        zagueiros_fixo = payload.get("zagueiros_fixos")
        habilidosos = payload.get("habilidosos")

        times: Times = montar_times(jogadores, zagueiros_fixo, habilidosos)
        data_jogo = calcular_data_jogo()

        game_payload = Game(data_jogo, times, jogadores)
        game_payload_dict = asdict(game_payload)
        try:
            game_response = self.repository.save(game_payload_dict)
            return 201, game_response
        except APIError as e:
            if (
                e.message
                == 'duplicate key value violates unique constraint "game_date_key"'
                and e.code == 23505
            ):
                game_id = self.repository.find_by_date_game(data_jogo)["id"]
                try:
                    self.update(game_id, game_payload_dict)
                except Exception as e:
                    logger.error(f"Error creating game: {e}")
                    return 500, {"error": "Error creating game"}
        except Exception as e:
            logger.error(f"Error creating game: {e}")
            return 500, {"error": "Error creating game"}

    def update(self, game_id, body_data) -> tuple[int, dict]:
        try:
            game_response = self.repository(game_id, body_data)
            return 200, game_response
        except Exception as e:
            logger.error(f"Error updating game: {e}")
            return 500, {"error": "Error updating game"}
