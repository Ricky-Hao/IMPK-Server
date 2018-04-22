import asyncio
import json
from Server.core import Route, send, crypto
from Server.message import *
from Server.util import logger
from Server.database import db

route_log = logger.getChild('Route')

@Route.route('AuthRequestMessage')
async def login(message, ws):
    log = route_log.getChild('Login')
    message = AuthRequestMessage(message)
    log.debug(message)
    if db.checkUser(message.username, message.password):

        await ws.send(AuthResultMessage({'status':'Logged', 'username':message.username}).to_json())
        return {'status':'Logged','channel':message.username}
    else:
        await ws.send(AuthResultMessage({'status':'Failed'}).to_json())
        return {'status':'Failed'}

@Route.route('RegisterRequestMessage')
async def register(message, ws):
    log = route_log.getChild('Register')
    message = RegisterRequestMessage(message)
    log.debug(message)
    if db.fetchOne('*', 'user', db.and_where({'username':message.username})) is None:
        if db.addUser(message.username, message.password):
            await ws.send(AuthResultMessage({'status':'Logged', 'username':message.username}).to_json())
            return {'status':'Logged', 'channel':message.username}

    await ws.send(AuthResultMessage({'status':'Failed'}).to_json())
    return {'status':'Failed'}

@Route.route('CertificateRequestMessage')
async def certificateRequest(message, ws):
    message = CertificateRequestMessage(message)
    cert_data = db.fetchCert(message.request_user)
    if cert_data is None:
        await ws.send(ServerMessage({'content':'{0}的证书文件不存在。'.format(message.request_user)}).to_json())
    else:
        cert_message = CertificateInstallMessage()
        cert_message.cert = cert_data
        cert_message.cert_user = message.request_user
        await ws.send(cert_message.to_json())

@Route.route('CertificateSigningRequestMessage')
async def certficateSigning(message, ws):
    log = route_log.getChild('CertificateSigning')

    server_key = crypto.loadPrivateFromUser('Server', None)
    server_cert = crypto.loadCertFromUser('Server')
    message = CertificateSigningRequestMessage(message)
    cert = crypto.signCSR(server_cert, server_key, crypto.loadCSR(message.csr), 90)
    log.debug('Sign CSR for {0}.'.format(message.source))
    install_message = CertificateInstallMessage({'cert':cert, 'cert_user':message.source})

    db.addCert(install_message.cert_user, install_message.cert)
    await ws.send(install_message.to_json())



@Route.route('ChatMessage')
async def chat(message, ws):
    log = route_log.getChild('Chat')
    message = ChatMessage(message)
    log.debug(message)
    if send(message.to_user, message.to_json()) < 1:
        message = ServerMessage({'content':'{0}已离线。'.format(message.to_user)})
        await ws.send(message.to_json())
    return None


@Route.route('FriendUpdateMessage')
async def updateFriend(message, ws):
    log = route_log.getChild('FriendUpdate')
    message = FriendUpdateMessage(message)
    temp_list = db.fetchFriend(message.source)
    friend_list = []
    for row in temp_list:
        friend_list.append(row[0])
    log.debug(friend_list)
    send(message.source, FriendMessage({'friend_list':friend_list}).to_json())

    for friend in friend_list:
        friend_cert = db.fetchCert(friend)
        install_message = CertificateInstallMessage({'cert_user':friend, 'cert':friend_cert})
        send(message.source, install_message.to_json())



@Route.route('FriendRequestMessage')
async def requestFriend(message, ws):
    log = route_log.getChild('FriendRequest')
    message = FriendRequestMessage(message)
    log.debug(message)
    if send(message.friend_name, message.to_json()) < 1:
        message = ServerMessage({'content': '{0}已离线。'.format(message.friend_name)})
        await ws.send(message.to_json())
    return None


@Route.route('FriendAcceptMessage')
async def acceptFriend(message, ws):
    log = route_log.getChild('FriendAccept')
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

