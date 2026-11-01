"""Ponto de entrada único: monólito modular da livraria."""
import os

from application.use_cases import Livraria
from infrastructure.txt_repository import RepositorioTXT
from presentation.http_server import iniciar_servidor


def main():
    # Um processo HTTP e um repositório para todos os módulos.
    sistema = Livraria(RepositorioTXT())
    porta = int(os.environ.get('PORT', '8000'))
    iniciar_servidor(sistema, porta=porta)


if __name__ == '__main__':
    main()
