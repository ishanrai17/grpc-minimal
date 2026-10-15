import http.client
import json

HOST = "ping-server"
PORT = 8080


class HttpPingClient:
    def __init__(self, host=HOST, port=PORT):
        self.conn = http.client.HTTPConnection(host, port)
        self.body = json.dumps({"payload": "x" * 64}).encode()

    def unary(self):
        self.conn.request("POST", "/ping", self.body, {"Content-Type": "application/json"})
        return json.loads(self.conn.getresponse().read())
