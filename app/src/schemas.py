from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class Jogador:
    nome: str
    goleiro: bool = False
    visitante: bool = False
    quem_convidou: str = ""
    pagou: bool = False


@dataclass
class Times:
    a: List[str] = field(default_factory=list)
    b: List[str] = field(default_factory=list)
    c: List[str] = field(default_factory=list)


@dataclass
class Jogo:
    data: str
    times: Times
    jogadores: List[Jogador]
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
