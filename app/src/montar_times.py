import random

from src.schemas import Player, Times


def limpar_nome_base(nome: str) -> str:
    """Remove parentheses and normalize player name"""
    return nome.lower().split("(")[0].strip()


def identificar_zagueiros(
    jogadores: list[Player],
    zagueiros_fixo: list[str] = [],
) -> tuple[list[Player], list[Player]]:
    """Separate defenders from other players"""
    zagueiros = []
    restantes = []
    for j in jogadores:
        nome_base = limpar_nome_base(j.name)
        if nome_base in zagueiros_fixo:
            zagueiros.append(j)
        else:
            restantes.append(j)
    return zagueiros, restantes


def identificar_habilidosos(
    jogadores: list[Player],
    habilidosos: list[str] = [],
) -> tuple[list[Player], list[Player]]:
    """Separate skilled players from other players"""
    habilidosos = []
    restantes = []
    for j in jogadores:
        nome_base = limpar_nome_base(j.name)
        if nome_base in habilidosos:
            habilidosos.append(j)
        else:
            restantes.append(j)
    return habilidosos, restantes


def montar_times(
    jogadores: list[Player], zagueiros_fixo: list = [], habilidosos: list = []
) -> Times:
    """Create balanced teams based on the provided player list"""
    jogadores = [j for j in jogadores if j.gk is False]
    total = len(jogadores)

    if total < 12:
        raise ValueError(
            f"Número insuficiente de jogadores (mínimo 12). Quantidade fornecida: {total}"
        )

    # Initialize empty teams
    times = [[], [], []]

    # Separate defenders and skilled players
    zagueiros, jogadores_rest = identificar_zagueiros(jogadores, zagueiros_fixo)
    habilidosos, outros = identificar_habilidosos(jogadores_rest, habilidosos)

    # Distribute defenders (one per team if possible)
    for i, zagueiro in enumerate(zagueiros[:3]):
        times[i % 3].append(zagueiro)

    # Distribute skilled players in pairs
    random.shuffle(habilidosos)
    duplas = [habilidosos[i : i + 2] for i in range(0, len(habilidosos), 2)]
    for i, dupla in enumerate(duplas):
        times[i % 3].extend(dupla)

    # Fill remaining spots
    random.shuffle(outros)
    for jogador in outros:
        # Add player to the team with fewer players
        menores = sorted(range(3), key=lambda x: len(times[x]))
        times[menores[0]].append(jogador)

    # Convert to Times object with player names
    return Times(
        a=[j.name for j in times[0]],
        b=[j.name for j in times[1]],
        c=[j.name for j in times[2]],
    )
