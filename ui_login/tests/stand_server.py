"""Локальный HTTP-сервер для тестового стенда (статические файлы из папки stand/)."""
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

STAND_DIR = Path(__file__).resolve().parent.parent / "stand"


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # не засорять вывод pytest
        pass


class _Server(ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        # браузер может оборвать соединение при закрытии — это не ошибка стенда
        pass


def start_server(directory=STAND_DIR):
    """Запускает сервер на свободном порту; возвращает (server, base_url)."""
    handler = partial(_QuietHandler, directory=str(directory))
    server = _Server(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"
