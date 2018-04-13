import json
from .logger import logging

log = logging.getLogger('Message')

class BaseMessage:
    def __init__(self, data=None):
        object.__setattr__(self, 'data', dict())
        self._init_data()
        self._parse(data)
        self._check_data()
        self._log()

    def _parse(self, data=None):
        if data is not None:
            if isinstance(data, str):
                self.data.update(json.loads(data))
            elif isinstance(data, dict):
                self.data.update(data)
            else:
                log.error('Wrong type with data: {0}'.format(data))

    def _init_data(self):
        self.data['message_type'] = 'BaseMessage'
        self.data['from'] = ''

    def _check_data(self):
        pass

    def _log(self):
        log.debug(self.data)

    def to_json(self):
        return json.dumps(self.data)

    def __str__(self):
        return '[{0}: {1}]'.format(self.message_type, str(self.data))

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, item):
        if item in self.data:
            return self.data[item]
        else:
            raise AttributeError

    def __setattr__(self, name, value):
        if name in self.data:
            self.data[name] = value
        else:
            raise AttributeError


class AuthMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_data(self):
        self.data['message_type'] = 'AuthMessage'


class ChatMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_data(self):
        self.data['message_type'] = 'ChatMessage'


class EchoMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_data(self):
        self.data['message_type'] = 'EchoMessage'


class FriendMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_data(self):
        self.data['message_type'] = 'FriendMessage'


class FriendRequestMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_data(self):
        self.data['message_type'] = 'FriendRequestMessage'



class FriendAcceptMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_data(self):
        self.data['message_type'] = 'FriendAcceptMessage'


class FriendUpdateMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_data(self):
        self.data['message_type'] = 'FriendUpdateMessage'


class ServerMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)
        self.data['from'] = 'Server'

    def _init_data(self):
        self.data['message_type'] = 'ServerMessage'
