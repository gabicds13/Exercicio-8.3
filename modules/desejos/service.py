"""Regras de manutenção da lista de desejos."""


class DesejosService:
    def listar(self, dados: dict) -> list[int]:
        return list(dados['desejos'])

    def alternar(self, dados: dict, livro_id: int) -> str:
        desejos = dados['desejos']
        if livro_id in desejos:
            desejos.remove(livro_id)
        else:
            desejos.append(livro_id)
        return 'Lista de desejos atualizada.'
