from http.server import BaseHTTPRequestHandler, HTTPServer

from golddigger import GoldDigger

hostName = "0.0.0.0"
serverPort = 8081


class GoldDiggerServer(BaseHTTPRequestHandler):

    goldDigger = GoldDigger()

    def _set_headers(self, content):
        self.send_response(200)
        self.send_header('Content-type', content)
        self.end_headers()

    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(GoldDiggerServer, self).end_headers()

    # noinspection PyPep8Naming
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()

    # noinspection PyPep8Naming
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"received get request")

    # noinspection PyPep8Naming
    def do_POST(self):
        if self.path == "/golddigger":
            print("in gold digger server")

            jsonDataLength = int(self.headers["Content-Length"])
            jsonData = self.rfile.read(jsonDataLength).decode("utf-8")
            calculated = self.process_coin_bags(jsonData)

            self.send_response(200)
            self.send_header('Access-Control-Allow-Credentials', 'true')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.send_header("Content-length", str(len(calculated)))
            self.end_headers()

            self.wfile.write(calculated.encode(encoding='utf_8'))
        else:
            self.send_response(404)

    @classmethod
    def process_coin_bags(cls, json):
        cls.goldDigger.set_json_web(json)
        return cls.goldDigger.get_json()


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), GoldDiggerServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
