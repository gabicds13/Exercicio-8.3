"""Único servidor HTTP para todos os módulos da aplicação."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

from presentation.view import pagina


def iniciar_servidor(sistema, host='0.0.0.0', porta=8000):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            caminho = urlparse(self.path)
            if caminho.path != '/':
                self.send_error(404)
                return
            args = parse_qs(caminho.query)
            busca = args.get('busca', [''])[0]
            livros, reservas, desejos = sistema.consultar(busca)
            conteudo = pagina(
                livros, reservas, desejos, busca, args.get('mensagem', [''])[0]
            ).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(conteudo)))
            self.end_headers()
            self.wfile.write(conteudo)

        def do_POST(self):
            caminho = urlparse(self.path).path
            if caminho not in ('/reservar', '/cancelar', '/desejo'):
                self.send_error(404)
                return
            tamanho = min(int(self.headers.get('Content-Length', '0')), 10000)
            formulario = parse_qs(self.rfile.read(tamanho).decode('utf-8'))
            try:
                livro_id = int(formulario.get('id', [''])[0])
                mensagem = sistema.acao(caminho, livro_id)
            except (ValueError, KeyError) as erro:
                mensagem = str(erro) or 'Não foi possível concluir a ação.'
            self.send_response(303)
            self.send_header('Location', '/?' + urlencode({'mensagem': mensagem}))
            self.end_headers()

    print(f'Livraria modular na porta {porta}. No Codespaces: Ports > Open in Browser.', flush=True)
    ThreadingHTTPServer((host, porta), Handler).serve_forever()
