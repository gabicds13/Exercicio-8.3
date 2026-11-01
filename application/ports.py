"""Contrato de persistência: as regras não dependem de TXT/JSON."""
from typing import Protocol


class RepositorioLivraria(Protocol):
    def carregar(self) -> dict: ...

    def salvar(self, dados: dict) -> None: ...
