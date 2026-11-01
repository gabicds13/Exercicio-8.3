"""Entidade do catálogo de livros."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Livro:
    id: int
    titulo: str
    autor: str
    preco: float
    estoque: int
    estante: str
