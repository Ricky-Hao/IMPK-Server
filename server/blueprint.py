import asyncio
from .server import Route, Sender
from .message import AuthMessage, ChatMessage, EchoMessage
from .logger import logging
from .redis_pool import send
import json

@Route.route('AuthMessage')
async def login(message, ws):
    log = logging.getLogger('Login')
    message = AuthMessage(message)
    log.debug(message)
    data = {'session':message.username}
    await ws.send(json.dumps(data))
    return {'addChannel':message.username}

@Route.route('ChatMessage')
async def chat(message, ws):
    log = logging.getLogger('Chat')
    message = ChatMessage(message)
    log.debug(message)
    if send(message.to, message.to_json()) < 1:
        await ws.send('{0} is offline.'.format(message.to))
        log.debug('{0} offline.'.format(message.to))
    return None

@Route.route('EchoMessage')
async def echo(message, ws):
    log = logging.getLogger('Echo')
    message = EchoMessage(message)
    log.debug(message)
    await ws.send(message.content)
    return None
