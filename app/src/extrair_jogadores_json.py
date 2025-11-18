import json
import re
from typing import Dict, List

from src.schemas import Jogador

SECOES = {
    "GOLEIROS": "goleiros",
    "DA CASA": "casa",
    "VISITANTES": "visitantes",
    "NÃO VÃO": "nao_vao",
    "NAO VAO": "nao_vao",  # fallback sem acento
}


def _strip_markers(s: str) -> str:
    s = re.sub(r"[\u200B-\u200D\uFEFF]", "", s)  # zero-width
    s = re.sub(r"^\s*(?:\d+\.\s*|[\*\-\–•]\s+)", "", s)  # 1.  / *  / -  / •
    return s.strip()


def _extrai_nome_e_convidou(linha: str):
    m = re.search(r"\(([^()]*)\)\s*$", linha)
    convidou = ""
    if m:
        convidou = re.sub(r"\s+", " ", m.group(1)).strip()
        linha = linha[: m.start()].rstrip()
    nome = re.sub(r"\s+", " ", linha).strip()
    return nome, convidou


def _linha_eh_vazia_ou_numero(l: str) -> bool:
    return (not l) or bool(re.fullmatch(r"[\d\.\-\*•– ]*", l))


def extrair_jogadores_json(texto: str) -> list[Jogador]:
    jogadores: List[Dict] = []
    vistos = set()

    secao_atual = None
    for bruta in texto.splitlines():
        cab = bruta.strip().upper()

        # Detecta cabeçalhos
        if cab.startswith("🧤") or "GOLEIROS" in cab:
            secao_atual = SECOES["GOLEIROS"]
            continue
        if cab.startswith("🏠") or "DA CASA" in cab:
            secao_atual = SECOES["DA CASA"]
            continue
        if cab.startswith("🎟") or "VISITANTES" in cab:
            secao_atual = SECOES["VISITANTES"]
            continue
        if "NÃO VÃO" in cab or "NAO VAO" in cab or cab.startswith("🚫"):
            secao_atual = SECOES["NÃO VÃO"]
            continue

        if secao_atual is None:
            continue
        if secao_atual == "nao_vao":
            # ignora totalmente essa seção
            continue

        linha = _strip_markers(bruta)
        if _linha_eh_vazia_ou_numero(linha):
            continue

        nome, convidou = _extrai_nome_e_convidou(linha)

        # garante que é “nome-ish”: pelo menos 2 letras
        if len(re.sub(r"[^A-Za-zÀ-ÿ]", "", nome)) < 2:
            continue

        goleiro = secao_atual == "goleiros"
        visitante = secao_atual == "visitantes"

        chave = (nome, goleiro, visitante, convidou)
        if chave in vistos:
            continue
        vistos.add(chave)

        jogador = Jogador(
            name=nome,
            gk=goleiro,
            visitor=visitante,
            invited_by=convidou,
        )
        jogadores.append(jogador)

    return jogadores
