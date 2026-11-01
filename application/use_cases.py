"""Fachada para a interface HTTP, compondo módulos de funcionalidades.

Uma aplicação, três módulos de negócio e um repositório compartilhado.
"""
from threading import RLock

from application.ports import RepositorioLivraria
from modules.catalogo.service import CatalogoService
from modules.desejos.service import DesejosService
from modules.reservas.service import ReservasService


class Livraria:
    def __init__(self, repositorio: RepositorioLivraria):
        self.repositorio = repositorio
        self.catalogo = CatalogoService()
        self.reservas = ReservasService()
        self.desejos = DesejosService()
        self._lock = RLock()

    def _dados(self) -> dict:
        dados = self.repositorio.carregar()
        if self.reservas.expirar(dados):
            self.repositorio.salvar(dados)
        return dados

    def consultar(self, termo: str = ''):
        """Mantém o contrato da interface existente (livros, reservas, desejos)."""
        with self._lock:
            dados = self._dados()
            return (
                self.catalogo.listar(dados, termo),
                self.reservas.listar(dados),
                self.desejos.listar(dados),
            )

    def acao(self, rota: str, livro_id: int) -> str:
        """Encaminha cada operação ao seu módulo responsável."""
        with self._lock:
            dados = self._dados()
            livro = self.catalogo.obter_livro(dados, livro_id)
            if livro is None:
                raise ValueError('Livro não encontrado.')

            if rota == '/reservar':
                mensagem = self.reservas.reservar(dados, livro)
            elif rota == '/cancelar':
                mensagem = self.reservas.cancelar(dados, livro.id)
            elif rota == '/desejo':
                mensagem = self.desejos.alternar(dados, livro.id)
            else:
                raise ValueError('Ação desconhecida.')

            self.repositorio.salvar(dados)
            return mensagem
