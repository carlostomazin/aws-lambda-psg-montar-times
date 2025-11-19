from aws_lambda_powertools import Logger

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
        try:
            game = self.repository.save(payload)
            return 201, game
        except Exception as e:
            logger.error(f"Error creating game: {e}")
            return 500, {"error": "Error creating game"}

    def update(self, game_id, body_data) -> tuple[int, dict]:
        try:
            game = self.repository.find_by_id(game_id)
            if not game:
                return 404, {"error": "Game not found"}
            game.update_from_dict(body_data)
            self.repository.save(game)
            return 200, game.to_dict()
        except Exception as e:
            logger.error(f"Error updating game: {e}")
            return 500, {"error": "Error updating game"}
