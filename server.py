# server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        access_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f'접속 시간: {access_time}')
        print(f'접속한 클라이언트 IP: {client_ip}')

        if self.path == '/' or self.path == '/index.html':
            try:
                with open('index.html', 'rb') as file:
                    content = file.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, 'File Not Found')
        else:
            self.send_error(404, 'Page Not Found')


def run_server():
    server_address = ('', 8000)  # 8080 → 8000
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('웹 서버가 8080 포트에서 시작됩니다...')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
