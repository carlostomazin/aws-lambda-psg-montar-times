from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, Response
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from src.services import get_recupera_jogos, post_gerar_jogo

tracer = Tracer()
logger = Logger()
app = APIGatewayHttpResolver()


@app.get("/health")
@tracer.capture_method
def get_health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


@app.get("/games")
@tracer.capture_method
def get_games():
    status_code, response = get_recupera_jogos()
    return Response(
        status_code=status_code, content_type="application/json", body=response
    )


# You can continue to use other utilities just as before
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
