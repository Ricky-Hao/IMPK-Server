from .base import BaseMessage

class FriendMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)
        self.friend_list = None

    def _init_type(self):
        self.type = 'FriendMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.friend_list = data.get('friend_list')


class FriendRequestMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)
        self.friend_name = None

    def _init_type(self):
        self.type = 'FriendRequestMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.friend_name = data.get('friend_name')



class FriendAcceptMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)
        self.friend_name = None
        self.accept = None

    def _init_type(self):
        self.type = 'FriendAcceptMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.friend_name = data.get('friend_name')
        self.accept = data.get('accept')


class FriendUpdateMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'FriendUpdateMessage'