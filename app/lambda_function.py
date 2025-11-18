import logging

from src.services import get_recupera_jogos, post_gerar_jogo
from src.utils import make_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")

    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", event.get("httpMethod", ""))
    )

    path = (
        event.get("requestContext", {})
        .get("http", {})
        .get("path", event.get("path", ""))
    )

    match method:
        case "GET":
            match path:
                case "/health":
                    status_code, response = 200, {"status": "ok"}
                case "/jogos":
                    status_code, response = get_recupera_jogos()
                case "/jogos/{data}":
                    status_code, response = get_recupera_jogos(
                        data=event.get("pathParameters", {}).get("data", "")
                    )
                case _:
                    status_code, response = 404, {"error": "Not Found"}

        case "POST":
            match path:
                case "/jogos/gerar":
                    status_code, response = post_gerar_jogo(event.get("body", ""))
                case _:
                    status_code, response = 404, {"error": "Not Found"}

        case _:
            status_code, response = 405, {"error": "Method Not Allowed"}

    return make_response(status_code, response)
