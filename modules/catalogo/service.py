"""Operações de busca e disponibilidade do catálogo."""
from modules.catalogo.models import Livro


class CatalogoService:
    def obter_livro(self, dados: dict, livro_id: int) -> Livro | None:
        for registro in dados['livros']:
            if registro['id'] == livro_id:
                return Livro(**registro)
        return None

    def listar(self, dados: dict, termo: str = '') -> list[dict]:
        termo_normalizado = termo.casefold()
        ids_reservados = {r['livro_id'] for r in dados['reservas']}
        resultado = []
        for registro in dados['livros']:
            livro = Livro(**registro)
            if termo_normalizado not in (livro.titulo + ' ' + livro.autor).casefold():
                continue
            reservado = livro.id in ids_reservados
            resultado.append({
                **registro,
                'disponivel': max(0, livro.estoque - (1 if reservado else 0)),
                'reservado': reservado,
            })
        return resultado
