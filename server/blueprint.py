import asyncio
import json
from .server import Route, Sender
from .message import *
from .logger import logging
from .redis_pool import send
from .database import db

@Route.route('AuthRequestMessage')
async def login(message, ws):
    log = logging.getLogger('Login')
    message = AuthRequestMessage(message)
    log.debug(message)
    if db.checkUser(message.username, message.password):

        await ws.send(AuthResultMessage({'status':'Logged', 'username':message.username}).to_json())
        return {'status':'Logged','channel':message.username}
    else:
        await ws.send(AuthResultMessage({'status':'Failed'}).to_json())
        return {'status':'Failed'}

@Route.route('CertificateRequestMessage')
async def certificateRequest(message, ws):
    # Todo
    pass

@Route.route('ChatMessage')
async def chat(message, ws):
    log = logging.getLogger('Chat')
    message = ChatMessage(message)
    log.debug(message)
    if send(message.to_user, message.to_json()) < 1:
        message = ServerMessage({'content':'{0}已离线。'.format(message.to_user)})
        await ws.send(message.to_json())
    return None


@Route.route('FriendUpdateMessage')
async def updateFriend(message, ws):
    log = logging.getLogger('FriendUpdate')
    message = FriendUpdateMessage(message)
    temp_list = db.fetchFriend(message.source)
    friend_list = []
    for row in temp_list:
        friend_list.append(row[0])
    log.debug(friend_list)
    send(message.source, FriendMessage({'friend_list':friend_list}).to_json())


@Route.route('FriendRequestMessage')
async def requestFriend(message, ws):
    log = logging.getLogger('FriendRequest')
    message = FriendRequestMessage(message)
    log.debug(message)
    if send(message.friend_name, message.to_json()) < 1:
        message = ServerMessage({'content': '{0}已离线。'.format(message.friend_name)})
        await ws.send(message.to_json())
    return None


@Route.route('FriendAcceptMessage')
async def acceptFriend(message, ws):
    log = logging.getLogger('FriendAccept')
    message = FriendAcceptMessage(message)
    log.debug(message)
    if message.accept:
        db.addFriend(message.friend_name, message.source)
        db.addFriend(message.source, message.friend_name)
        await updateFriend(FriendUpdateMessage({'source':message.friend_name}).to_json(), ws)
        await updateFriend(FriendUpdateMessage({'source': message.source}).to_json(), ws)
    else:
        server_message = ServerMessage({'content': '{0}拒绝成为您的好友。'.format(message.source)})
        send(message.friend_name, server_message.to_json())

