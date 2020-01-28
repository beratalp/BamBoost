import asyncio
import json
import websockets
from bamboost import *
import threading


class BamBoostWebSocketsServer:
    def __init__(self):
        self.users = set()
        self.state = {"pitch": 0, "roll": 0, "cpu_temp": 0}
        self.websocket = websockets.serve(self.send_data, ADDRESS, SOCKETPORT)
        self.websocket_thread = threading.Thread(target=asyncio.get_event_loop().run_forever)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.websocket)
        self.websocket_thread.start()

    def set_value(self, pitch, roll, cpu_temp):
        self.state["pitch"] = pitch
        self.state["roll"] = roll
        self.state["cpu_temp"] = cpu_temp

    async def send_data(self, websocket, path):
        while True:
            await asyncio.wait([websocket.send(json.dumps(self.state))])
            await asyncio.sleep(0.5)

