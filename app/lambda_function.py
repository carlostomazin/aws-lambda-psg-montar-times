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
    event["body"] = sem_emojis(event["body"])

    try:
        body = json.loads(event["body"])
    except Exception as e:
        logger.error(e)
        return {"statusCode": 400, "body": json.dumps("Invalid JSON in request body")}

    required_keys = ["jogadores_raw", "zagueiros_fixo", "habilidasos"]
    if not all(key in body for key in required_keys):
        return {
            "statusCode": 400,
            "body": json.dumps(
                'Body must contain "jogadores_raw", "zagueiros_fixo" and "habilidasos" keys'
            ),
        }

    jogadores_raw = body["jogadores_raw"]
    zagueiros_fixo = body["zagueiros_fixo"]
    habilidasos = body["habilidasos"]

    # Extrair jogadores
    try:
        jogadores: list[Jogador] = extrair_jogadores_json(jogadores_raw)
    except Exception as e:
        logger.error(f"Error extracting players: {e}")
        return {"statusCode": 400, "body": json.dumps(f"Error extracting players: {e}")}
    logger.info(f"Extracted players: {jogadores}")

    # Montar times
    try:
        times: Times = montar_times(jogadores, zagueiros_fixo, habilidasos)
    except Exception as e:
        logger.error(f"Error forming teams: {e}")
        return {"statusCode": 400, "body": json.dumps(f"Error forming teams: {e}")}
    logger.info(f"Formed teams: {times}")

    # Salvar jogo
    try:
        data_jogo = calcular_data_jogo()
        logger.info(f"Game date: {data_jogo}")
        salvar_jogo(Jogo(data=data_jogo, times=times, jogadores=jogadores))
    except Exception as e:
        logger.error(f"Error saving game data: {e}")
        return {"statusCode": 500, "body": json.dumps(f"Error saving game data: {e}")}
    logger.info("Game data saved successfully")

    response = {
        "times": {
            "a": times.a,
            "b": times.b,
            "c": times.c,
        }
    }

    # Retonar resposta
    return {"statusCode": 200, "body": json.dumps(response)}
