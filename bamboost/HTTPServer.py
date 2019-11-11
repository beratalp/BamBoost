import threading
import socketserver
import http.server
import os
from bamboost import *

class BamBoostHTTPServer:
    handler = http.server.SimpleHTTPRequestHandler

    def __init__(self):
        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer((ADDRESS, HTTPPORT), self.handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

    def run(self):
        self.start()
