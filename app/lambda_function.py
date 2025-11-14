import json
import logging

from emoji import replace_emoji
from src.extrair_jogadores_json import extrair_jogadores_json
from src.montar_times import montar_times
from src.schemas import Jogador, Jogo, Times
from src.supabase_client import salvar_jogo
from src.utils import calcular_data_jogo

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def sem_emojis(texto: str) -> str:
    """Remove emojis de uma string."""
    return replace_emoji(texto, replace="")


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")

    # 🔹 Headers de CORS (ajusta o Origin se quiser travar por domínio)
    headers = {
        "Access-Control-Allow-Origin": "*",  # ou "*" se quiser liberar geral
        "Access-Control-Allow-Methods": "OPTIONS,POST",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    # 🔹 Tratamento do preflight (OPTIONS)
    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", event.get("httpMethod", ""))
    )

    if method == "OPTIONS":
        # Preflight não precisa de body
        return {
            "statusCode": 204,
            "headers": headers,
            "body": "",
        }

    # 🔹 Função helper pra sempre devolver com CORS
    def make_response(status_code: int, body: dict):
        return {
            "statusCode": status_code,
            "headers": headers,
            "body": json.dumps(body),
        }

    body_raw = event.get("body", "")

    try:
        body_raw = sem_emojis(body_raw or "")
    except Exception as e:
        logger.error(f"Error cleaning emojis: {e}")
        return make_response(400, {"error": "Invalid body"})

    try:
        body = json.loads(body_raw)
    except Exception as e:
        logger.error(e)
        return make_response(400, {"error": "Invalid JSON in body"})

    required_keys = ["jogadores_raw", "zagueiros_fixo", "habilidasos"]
    if not all(key in body for key in required_keys):
        return make_response(
            400,
            {
                "error": 'Body must contain "jogadores_raw", "zagueiros_fixo" and "habilidasos" keys'
            },
        )

    jogadores_raw = body["jogadores_raw"]
    zagueiros_fixo = body["zagueiros_fixo"]
    habilidasos = body["habilidasos"]

    # Extrair jogadores
    try:
        jogadores: list[Jogador] = extrair_jogadores_json(jogadores_raw)
    except Exception as e:
        logger.error(f"Error extracting players: {e}")
        return make_response(400, {"error": f"Error extracting players: {e}"})
    logger.info(f"Extracted players: {jogadores}")

    # Montar times
    try:
        times: Times = montar_times(jogadores, zagueiros_fixo, habilidasos)
    except Exception as e:
        logger.error(f"Error forming teams: {e}")
        return make_response(400, {"error": f"Error forming teams: {e}"})
    logger.info(f"Formed teams: {times}")

    # Salvar jogo
    try:
        data_jogo = calcular_data_jogo()
        logger.info(f"Game date: {data_jogo}")
        salvar_jogo(Jogo(data=data_jogo, times=times, jogadores=jogadores))
    except Exception as e:
        logger.error(f"Error saving game data: {e}")
        return make_response(500, {"error": "Error saving game data"})
    logger.info("Game data saved successfully")

    response = {
        "times": {
            "a": times.a,
            "b": times.b,
            "c": times.c,
        }
    }

    return make_response(200, response)
