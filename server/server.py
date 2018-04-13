import asyncio
import websockets
from .redis_pool import subscribe
from .logger import logging
from .message import BaseMessage

class Route:
    Routes = {}

    @classmethod
    def route(cls, route):
        def wrapper(route_function):
            cls.Routes.update({route:route_function})
            return route_function
        return wrapper

class Sender:

    def __await__(self):
        return self.sender()

    def __init__(self, websocket, path=None, server=None):
        self.ws = websocket
        self.path = path
        self.server = server
        self.ps = subscribe('BoardCast')
        self.exit = 0
        self.log = logging.getLogger('Sender{0}'.format(self.ws.remote_address))

    async def sender(self):
        try:
            while True:
                if self.exit == 1:
                    break
                message = self.ps.get_message()
                if message:
                    self.log.debug(message)
                    if message['type'] == 'message':
                        await self.ws.send(message['data'].decode())
                else:
                    await asyncio.sleep(1)
        except websockets.ConnectionClosed or ConnectionResetError:
            self.ps.unsubscribe()
            self.log.debug('exit.')

    def addChannel(self, channel):
        self.ps.subscribe(channel)

    def close(self):
        self.ps.unsubscribe()
        self.log.debug('Unsubscribe.')
        self.exit = 1



class Listener:

    def __await__(self):
        return self.listener()

    def __init__(self, websocket, path=None, server=None):
        self.ws = websocket
        self.path = path
        self.server = server
        self.username = ''
        self.log = logging.getLogger('Listener{0}{1}'.format(self.username, self.ws.remote_address))

    async def listener(self):
        try:
            async for message in self.ws:
                base_message = BaseMessage(message)
                base_message.user = self.username
                self.log.debug(message)

                if base_message.message_type in Route.Routes.keys():
                    self.log.debug(base_message.message_type)
                    result = await Route.Routes[base_message.message_type](base_message.to_json(), self.ws)

                    if result:
                        for key in result.keys():
                            if key == 'addChannel':
                                self.username = result[key]
                                self.server.sender.addChannel(result[key])

        except websockets.ConnectionClosed or ConnectionResetError:
            self.log.debug('Connection closed.')
            self.ws.close()
            self.server.sender.close()


class Server:
    def __init__(self):
        self.sender = None
        self.listener = None
        self.websocket = None
        self.path = None
        self.log = logging.getLogger('Server')

    async def connect(self, websocket, path):
        self.websocket = websocket
        self.path = path
        self.log.info(self.websocket.remote_address)

        self.sender = Sender(self.websocket, self.path, self)
        self.listener = Listener(self.websocket, self.path, self)

        listener_task = asyncio.ensure_future(self.listener)
        sender_task = asyncio.ensure_future(self.sender)
        done, pending = await asyncio.wait(
            [sender_task, listener_task],
        )


