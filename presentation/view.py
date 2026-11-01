"""HTML/CSS do MVP original, preservando a aparência e as funcionalidades."""
from html import escape

CSS = """*{box-sizing:border-box}body{margin:0;background:#f7f6f1;color:#283a30;font:16px system-ui,Arial}header{background:#174b39;color:white;padding:24px}header>div,main{max-width:950px;margin:auto;padding:0 18px}h1{margin:0}main{padding-top:18px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:14px}.card{background:white;border:1px solid #ddd;border-radius:14px;padding:19px}.card h3{margin:0}.muted{color:#627369}.price{font-weight:700;color:#126044;font-size:21px}button{background:#17694e;border:0;border-radius:8px;color:white;padding:10px 12px;cursor:pointer}button:disabled{background:#999;cursor:default}input[type=search]{padding:11px;width:min(420px,75%);border:1px solid #aaa;border-radius:8px}form{display:inline}section{margin:26px 0}.notice{padding:12px;background:#fff1cd;border-radius:8px}.shelf{background:#e5f5ec;border-radius:8px;padding:9px;font-size:14px}.line{padding:10px;border-bottom:1px solid #ddd}footer{margin:35px 0;color:#64776b;font-size:13px}"""


def pagina(livros, reservas, desejos, busca='', mensagem=''):
    cards = []
    for livro in livros:
        n = livro['id']
        reservado = livro['reservado']
        disponivel = livro['disponivel']
        botao = 'Já reservado' if reservado else ('Indisponível' if disponivel < 1 else 'Reservar por 24h')
        disabled = 'disabled' if reservado or disponivel < 1 else ''
        favorito = '♥ Remover dos desejos' if n in desejos else '♡ Adicionar aos desejos'
        cards.append(f'''<article class="card"><h3>📖 {escape(livro['titulo'])}</h3><p class="muted">{escape(livro['autor'])}</p><p class="price">R$ {livro['preco']:.2f}</p><p>{disponivel} exemplar(es) disponível(is)</p><p class="shelf">📍 Estante: {escape(livro['estante'])}</p><form action="/reservar" method="post"><input type="hidden" name="id" value="{n}"><button {disabled}>{botao}</button></form> <form action="/desejo" method="post"><input type="hidden" name="id" value="{n}"><button style="background:#805e7b">{favorito}</button></form></article>''')
    reservados = ''.join(f'''<div class="line"><strong>{escape(r['titulo'])}</strong> — até {escape(r['expira_em'][:16].replace('T', ' '))} UTC <form action="/cancelar" method="post"><input type="hidden" name="id" value="{r['livro_id']}"><button>Cancelar</button></form></div>''' for r in reservas)
    desejos_visiveis = ''.join(f'<li>{escape(l["titulo"])}</li>' for l in livros if l['id'] in desejos)
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Minha Livraria - Monólito Modular</title><style>{CSS}</style></head><body><header><div><h1>📚 Minha Livraria</h1><p>Encontre, reserve e localize seu livro na estante.</p></div></header><main>{'<p class="notice">'+escape(mensagem)+'</p>' if mensagem else ''}<form method="get" action="/"><input name="busca" type="search" placeholder="Pesquisar título ou autor" value="{escape(busca,quote=True)}"><button>Buscar</button></form><section><h2>Catálogo de livros</h2><div class="grid">{''.join(cards) or '<p>Nenhum livro encontrado.</p>'}</div></section><section><h2>Minhas reservas</h2>{reservados or '<p>Nenhuma reserva ativa.</p>'}</section><section><h2>Lista de desejos</h2>{'<ul>'+desejos_visiveis+'</ul>' if desejos_visiveis else '<p>Nenhum livro na lista nesta busca.</p>'}</section><footer>Projeto acadêmico · Dados de um usuário demonstrativo · Persistência em data/livraria.txt</footer></main></body></html>'''
