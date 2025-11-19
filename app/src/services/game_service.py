from aws_lambda_powertools import Logger

logger = Logger()


class GameService:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        games = self.repository.find_all()
        return 200, {"games": games}

    def get_by_id(self, game_id):
        game = self.repository.find_by_id(game_id)
        if game:
            return 200, game
        else:
            return 404, {"error": "Game not found"}

    def create(self, payload):
        try:
            # Assume body_data is already validated and processed
            # new_game = Game.from_dict(body_data)
            game = self.repository.save(payload)
            return 201, game
        except Exception as e:
            logger.error(f"Error creating game: {e}")
            return 500, {"error": "Error creating game"}

    def update(self, game_id, body_data):
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
