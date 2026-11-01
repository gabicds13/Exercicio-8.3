"""Entidade de uma reserva."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Reserva:
    livro_id: int
    expira_em: str
