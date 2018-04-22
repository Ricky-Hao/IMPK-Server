from .base import BaseMessage

class AuthRequestMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'AuthRequestMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.username = data.get('username')
        self.password = data.get('password')

    def to_dict(self):
        data = super().to_dict()
        data['username'] = self.username
        data['password'] = self.password
        return data


class AuthResultMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'AuthResultMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.status = data.get('status')
        self.source = 'Server'
        if self.status == 'Logged':
            self.username = data.get('username')
        else:
            self.username = ''

    def to_dict(self):
        data = super().to_dict()
        data['status'] = self.status
        data['username'] = self.username
        return data


class RegisterRequestMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'RegisterRequestMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.username = data.get('username')
        self.password = data.get('password')

    def to_dict(self):
        data = super().to_dict()
        data['username'] = self.username
        data['password'] = self.password
        return data

