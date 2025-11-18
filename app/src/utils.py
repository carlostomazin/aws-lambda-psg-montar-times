import json
from datetime import datetime, timedelta, timezone


def calcular_data_jogo() -> str:
    """Calcula a data do jogo: próxima segunda; se hoje for segunda, mantém a data."""
    hoje = datetime.now(timezone(timedelta(hours=-3)))
    dias_ate_segunda = (7 - hoje.weekday()) % 7  # 0=segunda
    proxima_segunda = hoje + timedelta(days=dias_ate_segunda)
    return proxima_segunda.strftime("%Y-%m-%d")


def make_response(status_code: int, body: dict):
    """Função helper pra sempre devolver com CORS"""
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
    }
