import http.server
import socket
import select
import urllib.parse
from text_modification import add_trademark
from http.client import HTTPConnection, HTTPSConnection
from config import HN_HOST, HN_PORT, HN_PATH


class HNProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Received GET request for: {self.path}")
        original_path = self.path
        parsed_url = urllib.parse.urlparse(original_path)

        if parsed_url.hostname == HN_HOST:
            # Modify the request URL path
            new_path = f"{HN_PATH}{parsed_url.path}"
            self.path = new_path

        # Check for HTTPS or HTTP
        if parsed_url.scheme == 'https':
            conn = HTTPSConnection(HN_HOST, HN_PORT)
        else:
            conn = HTTPConnection(HN_HOST)

        # Forward the request to Hacker News
        conn.request("GET", self.path)
        response = conn.getresponse()

        # Read the response
        content = response.read()

        # Modify the content
        modified_content = self.modify_content(content.decode('utf-8'))

        # Send the modified response back to the client
        self.send_response(response.status, response.reason)
        for header, value in response.getheaders():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(modified_content.encode('utf-8'))

    def modify_content(self, content):
        return add_trademark(content)

    def do_CONNECT(self):
        print(f"Received CONNECT request for: {self.path}")
        server_address = (self.path.split(':')[0], 443)
        try:
            # Устанавливаем соединение с целевым сервером
            remote_socket = socket.create_connection(server_address)
            self.send_response(200)
            self.end_headers()

            # Туннелирование данных между клиентом и сервером
            conn_streams = [self.connection, remote_socket]
            while True:
                readable, _, _ = select.select(conn_streams, [], [])
                for r in readable:
                    other = conn_streams[1] if r is conn_streams[0] else conn_streams[0]
                    data = r.recv(8192)
                    if not data:
                        return
                    other.sendall(data)
        except Exception as e:
            self.send_error(500, str(e))


if __name__ == "__main__":
    from config import PORT
    with http.server.HTTPServer(("", PORT), HNProxyHandler) as httpd:
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()
