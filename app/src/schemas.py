from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import List


@dataclass
class Player:
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
class Game:
    date_game: str
    teams: Times
    players: List[Player]
