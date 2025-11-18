from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import List


@dataclass
class Jogador:
    name: str
    gk: bool = False
    visitor: bool = False
    invited_by: str = ""
    paid: bool = False


@dataclass
class Times:
    a: List[str] = field(default_factory=list)
    b: List[str] = field(default_factory=list)
    c: List[str] = field(default_factory=list)


@dataclass
class Jogo:
    date_game: str
    teams: Times
    players: List[Jogador]
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone(timedelta(hours=-3))).isoformat()
    )
