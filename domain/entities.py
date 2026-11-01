"""Importações de compatibilidade; os modelos pertencem agora aos módulos."""
from modules.catalogo.models import Livro
from modules.reservas.models import Reserva

__all__ = ['Livro', 'Reserva']
