"""Build and preview with clean routes: python3 scripts/serve.py"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from build import build, DIST


class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        if urlparse(self.path).path == '/switch':
            self.path = '/switch/index.html'
        return super().send_head()

    def send_error(self, code, message=None, explain=None):
        if code == 404 and (DIST / '404.html').exists():
            body = (DIST / '404.html').read_bytes()
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(body)
        else:
            super().send_error(code, message, explain)


if __name__ == '__main__':
    build()
    server = ThreadingHTTPServer(('127.0.0.1', 4173), partial(Handler, directory=str(DIST)))
    print('Lounge preview: http://127.0.0.1:4173', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
