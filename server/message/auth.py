from .base import BaseMessage

class AuthRequestMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)
        self.username = None
        self.password = None

    def _init_type(self):
        self.type = 'AuthRequestMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.username = data.get('username')
        self.password = data.get('password')


class AuthResultMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)
        self.status = None
        self.username = None

    def _init_type(self):
        self.type = 'AuthResultMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.status = data.get('status')
        if self.status == 'Logged':
            self.username = data.get('username')
        else:
            self.username = ''

