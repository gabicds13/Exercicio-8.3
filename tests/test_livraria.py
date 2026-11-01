"""Testes com a biblioteca padrão (sem necessidade de pip install)."""
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from application.use_cases import Livraria
from infrastructure.txt_repository import RepositorioTXT
from presentation.view import pagina


class TestLivrariaModular(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.arquivo = Path(self.temp.name) / 'livraria.txt'
        self.sistema = Livraria(RepositorioTXT(self.arquivo))

    def test_catalogo_comeca_com_quatro_livros(self):
        livros, reservas, desejos = self.sistema.consultar()
        self.assertEqual(len(livros), 4)
        self.assertEqual(reservas, [])
        self.assertEqual(desejos, [])

    def test_busca_por_autor(self):
        livros, _, _ = self.sistema.consultar('machado')
        self.assertEqual([l['titulo'] for l in livros], ['Dom Casmurro'])

    def test_reserva_dura_24_horas(self):
        antes = datetime.now(timezone.utc)
        mensagem = self.sistema.acao('/reservar', 1)
        depois = datetime.now(timezone.utc)
        _, reservas, _ = self.sistema.consultar()
        self.assertIn('24 horas', mensagem)
        validade = datetime.fromisoformat(reservas[0]['expira_em'])
        self.assertGreaterEqual(validade, antes + timedelta(hours=24))
        self.assertLessEqual(validade, depois + timedelta(hours=24))

    def test_nao_reserva_duas_vezes(self):
        self.sistema.acao('/reservar', 1)
        with self.assertRaisesRegex(ValueError, 'indisponível'):
            self.sistema.acao('/reservar', 1)

    def test_nao_reserva_livro_sem_estoque(self):
        with self.assertRaisesRegex(ValueError, 'indisponível'):
            self.sistema.acao('/reservar', 3)

    def test_cancelamento_libera_livro(self):
        self.sistema.acao('/reservar', 1)
        self.sistema.acao('/cancelar', 1)
        livros, reservas, _ = self.sistema.consultar()
        self.assertEqual(reservas, [])
        self.assertFalse(livros[0]['reservado'])
        self.assertEqual(livros[0]['disponivel'], 4)

    def test_lista_de_desejos_adiciona_e_remove(self):
        self.sistema.acao('/desejo', 2)
        self.assertEqual(self.sistema.consultar()[2], [2])
        self.sistema.acao('/desejo', 2)
        self.assertEqual(self.sistema.consultar()[2], [])

    def test_dados_persistem_apos_nova_instancia(self):
        self.sistema.acao('/desejo', 4)
        outro = Livraria(RepositorioTXT(self.arquivo))
        self.assertEqual(outro.consultar()[2], [4])

    def test_expiracao_de_reserva(self):
        repo = RepositorioTXT(self.arquivo)
        dados = repo.carregar()
        dados['reservas'].append({
            'livro_id': 1,
            'expira_em': (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
        })
        repo.salvar(dados)
        self.assertEqual(self.sistema.consultar()[1], [])
        self.assertEqual(repo.carregar()['reservas'], [])

    def test_erro_em_rota_desconhecida(self):
        with self.assertRaisesRegex(ValueError, 'Ação desconhecida'):
            self.sistema.acao('/desconhecida', 1)

    def test_html_contem_catalogo(self):
        livros, reservas, desejos = self.sistema.consultar()
        html = pagina(livros, reservas, desejos)
        self.assertIn('Minha Livraria', html)
        self.assertIn('Dom Casmurro', html)


if __name__ == '__main__':
    unittest.main()
