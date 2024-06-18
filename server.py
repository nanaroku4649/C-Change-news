# server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# グローバル変数として更新ログを保持
update_log = "Update log\n\nTPM bypass improved\nPerm spoof system improved"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global update_log
        if self.path == '/update_log':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(update_log.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        global update_log
        if self.path == '/update_log':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update_log = post_data.decode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Update log updated')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
