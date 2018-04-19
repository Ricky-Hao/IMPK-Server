from .base import BaseMessage


class ServerMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)
        self.content = None

    def _init_type(self):
        self.type = 'ServerMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.content = data.get('content')
        self.source = 'Server'
