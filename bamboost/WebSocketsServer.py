import asyncio
import json
import websockets
from bamboost import *
import threading


class BamBoostWebSocketsServer:
    def __init__(self):
        self.users = set()
        self.state = {"value": 0}
        self.websocket = websockets.serve(self.send_data, ADDRESS, SOCKETPORT)
        self.websocket_thread = threading.Thread(target=asyncio.get_event_loop().run_forever)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.websocket)
        self.websocket_thread.start()

    def set_value(self, value):
        self.state["value"] = value

    async def send_data(self, websocket, path):
        while True:
            await asyncio.wait([websocket.send(json.dumps(self.state))])
            await asyncio.sleep(2)

