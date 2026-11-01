"""Repositório TXT em formato JSON (sem dependências externas)."""
import json
import os
from pathlib import Path


DADOS_INICIAIS = {
    'livros': [
        {'id': 1, 'titulo': 'Dom Casmurro', 'autor': 'Machado de Assis', 'preco': 29.90, 'estoque': 4, 'estante': 'A1 - Literatura Brasileira'},
        {'id': 2, 'titulo': 'A Hora da Estrela', 'autor': 'Clarice Lispector', 'preco': 34.90, 'estoque': 2, 'estante': 'A2 - Literatura Brasileira'},
        {'id': 3, 'titulo': 'O Pequeno Príncipe', 'autor': 'Antoine de Saint-Exupéry', 'preco': 39.90, 'estoque': 0, 'estante': 'B1 - Infantojuvenil'},
        {'id': 4, 'titulo': 'Capitães da Areia', 'autor': 'Jorge Amado', 'preco': 32.50, 'estoque': 3, 'estante': 'A3 - Literatura Brasileira'},
    ],
    'reservas': [],
    'desejos': [],
}


class RepositorioTXT:
    def __init__(self, arquivo=None):
        self.arquivo = Path(arquivo) if arquivo else Path(__file__).resolve().parents[1] / 'data' / 'livraria.txt'
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)
        if not self.arquivo.exists():
            self.salvar(DADOS_INICIAIS)

    def carregar(self) -> dict:
        with self.arquivo.open('r', encoding='utf-8') as f:
            return json.load(f)

    def salvar(self, dados: dict) -> None:
        temporario = self.arquivo.with_suffix('.tmp')
        with temporario.open('w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        os.replace(temporario, self.arquivo)
