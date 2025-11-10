# schemas.py

from dataclasses import dataclass
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
    a: List[str] = []
    b: List[str] = []
    c: List[str] = []


@dataclass
class Jogo:
    data: str
    times: Times
    jogadores: List[Jogador]
