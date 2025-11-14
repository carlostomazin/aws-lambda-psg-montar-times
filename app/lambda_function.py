import logging

from src.services import post_montar_times
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

    if method == "POST" and path == "/montar-times":
        status_code, response = post_montar_times(event.get("body", ""))
    elif method == "GET" and path == "/health":
        status_code, response = 200, {"status": "ok"}
    elif method == "OPTIONS":
        status_code, response = 204, {}
    else:
        status_code, response = 404, {"error": "Not Found"}

    return make_response(status_code, response)
