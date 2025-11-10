from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def calcular_data_jogo() -> str:
    """Calcula a data do jogo: próxima segunda; se hoje for segunda, mantém a data."""
    hoje = datetime.now()
    dias_ate_segunda = (7 - hoje.weekday()) % 7  # 0=segunda
    proxima_segunda = hoje + timedelta(days=dias_ate_segunda)
    return proxima_segunda.strftime("%Y-%m-%d")
