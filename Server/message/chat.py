from .base import BaseMessage


class ChatMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)


    def _init_type(self):
        self.type = 'ChatMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.to_user = data.get('to_user')
        self.ciphertext = data.get('ciphertext')
        self.signature = data.get('signature')

    def to_dict(self):
        data = super().to_dict()
        data['to_user'] = self.to_user
        data['ciphertext'] = self.ciphertext
        data['signature'] = self.signature
        return data
