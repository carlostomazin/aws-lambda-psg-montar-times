from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, Response
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.repositories.game_repository import GameRepository
from src.services.game_service import GameService

tracer = Tracer()
logger = Logger()
app = APIGatewayHttpResolver()
game_service = GameService(repository=GameRepository())


@app.get("/health")
@tracer.capture_method
def get_health():
    return {"status": "ok"}


@app.get("/games")
@tracer.capture_method
def get_games():
    status_code, response = game_service.get_all()
    return Response(
        status_code=status_code, content_type="application/json", body=response
    )


@app.get("/games/<game_id>")
@tracer.capture_method
def get_game_by_id(game_id: str):
    status_code, response = game_service.get_by_id(game_id)
    return Response(
        status_code=status_code, content_type="application/json", body=response
    )


@app.post("/games/create")
@tracer.capture_method
def post_create_game():
    body_data: dict = app.current_event.json_body
    logger.debug(f"Received payload for creating game: {body_data}")
    status_code, response = game_service.create(body_data)
    return Response(
        status_code=status_code, content_type="application/json", body=response
    )


# You can continue to use other utilities just as before
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
