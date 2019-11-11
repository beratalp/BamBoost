import os
from bamboost.HTTPServer import BamBoostHTTPServer
from bamboost.WebSocketsServer import BamBoostWebSocketsServer
import datetime
import time

class BamBoost:
    def __init__(self):
        os.chdir("../web/bController")
        self.web_server = BamBoostHTTPServer()
        self.websockets_server = BamBoostWebSocketsServer()

    def run(self):
        self.web_server.start()
        self.websockets_server.run()
        while True:
            self.websockets_server.set_value(str(datetime.datetime.now()))







