import threading
import socketserver
import http.server
import os
import websockets
import asyncio

HTTPPORT = 8080
SOCKETPORT = 5678
ADDRESS = "localhost"

value = "0"


class Server:
    handler = http.server.SimpleHTTPRequestHandler
    value = 5

    def __init__(self):
        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer((ADDRESS, HTTPPORT), self.handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

        self.websocket_server = websockets.serve(senddata, "localhost", SOCKETPORT)

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

    def run(self):
        os.chdir("../web/bController")
        self.start()
        asyncio.get_event_loop().run_until_complete(self.websocket_server)
        asyncio.get_event_loop().run_forever()


async def senddata(websocket, path):
    while True:
        await websocket.send(value)
        await asyncio.sleep(2)
