class GameService:
    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        games = self.repository.find_all()
        games_list = [game.to_dict() for game in games]
        return 200, {"games": games_list}

    def get_by_id(self, game_id):
        game = self.repository.find_by_id(game_id)
        if game:
            return 200, game.to_dict()
        else:
            return 404, {"error": "Game not found"}

    def create(self, body_data):
        try:
            # Assume body_data is already validated and processed
            new_game = Game.from_dict(body_data)
            self.repository.save(new_game)
            return 201, new_game.to_dict()
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
