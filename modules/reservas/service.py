"""Regras de negócio das reservas (prazo de 24 horas)."""
from datetime import datetime, timedelta, timezone

from modules.catalogo.models import Livro


class ReservasService:
    def expirar(self, dados: dict, agora: datetime | None = None) -> bool:
        agora = agora or datetime.now(timezone.utc)
        atuais = dados['reservas']
        validas = [r for r in atuais if datetime.fromisoformat(r['expira_em']) > agora]
        if len(validas) != len(atuais):
            dados['reservas'] = validas
            return True
        return False

    def listar(self, dados: dict) -> list[dict]:
        titulos = {livro['id']: livro['titulo'] for livro in dados['livros']}
        return [
            {**r, 'titulo': titulos.get(r['livro_id'], 'Livro desconhecido')}
            for r in dados['reservas']
        ]

    def reservar(self, dados: dict, livro: Livro) -> str:
        reservados = sum(r['livro_id'] == livro.id for r in dados['reservas'])
        if reservados or livro.estoque - reservados <= 0:
            raise ValueError('Livro indisponível ou já reservado.')
        fim = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
        dados['reservas'].append({'livro_id': livro.id, 'expira_em': fim})
        return 'Livro reservado por 24 horas!'

    def cancelar(self, dados: dict, livro_id: int) -> str:
        dados['reservas'] = [r for r in dados['reservas'] if r['livro_id'] != livro_id]
        return 'Reserva cancelada.'
