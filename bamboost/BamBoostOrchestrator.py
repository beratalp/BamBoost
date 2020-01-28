import os
from bamboost.HTTPServer import BamBoostHTTPServer
from bamboost.WebSocketsServer import BamBoostWebSocketsServer
from bamboost.Inclinometer import BamBoostInclinometer
from bamboost.CPUSensor import CPUSensor

class BamBoost:
    def __init__(self):
        os.chdir("../web/bController")
        self.web_server = BamBoostHTTPServer()
        self.websockets_server = BamBoostWebSocketsServer()
        self.inclinometer = BamBoostInclinometer()
        self.cpumonitor = CPUSensor()

    def run(self):
        self.web_server.start()
        self.websockets_server.run()
        while True:
            self.websockets_server.set_value(str(round(self.inclinometer.getPitch(), 2)),
                                             str(round(self.inclinometer.getRoll(), 2)),
                                             str(self.cpumonitor.getTemperature()))







