import asyncio
import websockets
from .server import Server
from .blueprint import *
from .database import db

def start():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websockets.serve(Server().connect, '0.0.0.0', 30000))
    loop.run_forever()