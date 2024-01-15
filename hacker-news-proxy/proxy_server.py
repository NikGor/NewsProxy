import http.server
import socketserver
from hn_proxy import HNProxyHandler
from config import PORT


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def run_proxy_server():
    handler = HNProxyHandler
    with ReusableTCPServer(("", PORT), handler) as httpd:
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()


if __name__ == "__main__":
    run_proxy_server()
