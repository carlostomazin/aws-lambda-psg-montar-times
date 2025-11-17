import json
import logging
from dataclasses import asdict

from emoji import replace_emoji
from src.extrair_jogadores_json import extrair_jogadores_json
from src.montar_times import montar_times
from src.schemas import Jogador, Jogo, Times
from src.supabase_client import salvar_jogo
from src.utils import calcular_data_jogo

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def post_gerar_jogo(body_raw: str) -> tuple[int, dict]:
    """Gera um jogo com base no corpo da requisição."""
    # Limpar emojis do corpo da requisição
    try:
        body_raw = sem_emojis(body_raw or "")
    except Exception as e:
        logger.error(f"Error cleaning emojis: {e}")
        return 400, {"error": "Invalid body"}

    # Parse do corpo da requisição
    try:
        body = json.loads(body_raw)
    except Exception as e:
        logger.error(e)
        return 400, {"error": "Invalid JSON in body"}

    # Validar campos obrigatórios
    required_keys = ["jogadores_raw", "zagueiros_fixo", "habilidasos"]
    if not all(key in body for key in required_keys):
        return 400, {
            "error": 'Body must contain "jogadores_raw", "zagueiros_fixo" and "habilidasos" keys'
        }

    # Extrair variáveis do corpo da requisição
    jogadores_raw = body["jogadores_raw"]
    zagueiros_fixo = body["zagueiros_fixo"]
    habilidasos = body["habilidasos"]

    # Extrair jogadores
    try:
        jogadores: list[Jogador] = extrair_jogadores_json(jogadores_raw)
    except Exception as e:
        logger.error(f"Error extracting players: {e}")
        return 400, {"error": f"Error extracting players: {e}"}
    logger.info(f"Extracted players: {jogadores}")

    # Montar times
    try:
        times: Times = montar_times(jogadores, zagueiros_fixo, habilidasos)
    except Exception as e:
        logger.error(f"Error forming teams: {e}")
        return 400, {"error": f"Error forming teams: {e}"}
    logger.info(f"Formed teams: {times}")

    # Salvar jogo
    try:
        data_jogo = calcular_data_jogo()
        logger.info(f"Game date: {data_jogo}")
        jogo = Jogo(data=data_jogo, times=times, jogadores=jogadores)
        salvar_jogo(jogo)
    except Exception as e:
        logger.error(f"Error saving game data: {e}")
        return 500, {"error": "Error saving game data"}
    logger.info("Game data saved successfully")

    response = asdict(jogo)

    return 200, response


def sem_emojis(texto: str) -> str:
    """Remove emojis de uma string."""
    return replace_emoji(texto, replace="")
