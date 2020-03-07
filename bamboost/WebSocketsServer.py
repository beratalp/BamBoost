import asyncio
import json
import websockets
from bamboost import *
import threading
from bamboost.Motor import LinearMotor


class BamBoostWebSocketsServer:
    def __init__(self):
        self.users = set()
        self.state = {"pitch": 0, "roll": 0, "cpu_temp": 0, "out_temp": 0}
        self.last_message = 0
        self.connected = set()
        self.motors = [LinearMotor(38, 40), LinearMotor(35, 37)]
        self.websocket = websockets.serve(self.handler, ADDRESS, SOCKETPORT)
        self.websocket_thread = threading.Thread(target=asyncio.get_event_loop().run_forever)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.websocket)
        self.websocket_thread.start()

    def set_value(self, pitch, roll, cpu_temp, out_temp):
        self.state["pitch"] = pitch
        self.state["roll"] = roll
        self.state["cpu_temp"] = cpu_temp
        self.state["out_temp"] = out_temp

    async def send_data(self, websocket, path):
        while True:
            try:
                await asyncio.wait([websocket.send(json.dumps(self.state))])
                await asyncio.sleep(0.5)
            finally:
                pass

    async def handler(self, websocket, path):
        consumer_task = asyncio.ensure_future(self.recv_handler(websocket, path))
        producer_task = asyncio.ensure_future(self.send_data(websocket, path))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

    async def recv_handler(self, websocket, path):
        async for message in websocket:
            self.recv(message)

    def recv(self, message):
        message = json.loads(message)
        title = ""
        try:
            title = message["title"]
        except KeyError:
            pass
        if title == "motor":
            m_index = message["m_index"]
            m_duration = message["m_duration"]
            m_speed = message["m_speed"]
            m_direction = message["m_direction"]
            if m_direction == "positive":
                self.motors[int(m_index)].positive(float(m_duration), float(m_speed))
            elif m_direction == "negative":
                self.motors[int(m_index)].negative(float(m_duration), float(m_speed))
        elif title == "halt":
            for motor in self.motors:
                motor.__reset__()
