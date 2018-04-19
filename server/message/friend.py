from .base import BaseMessage

class FriendMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'FriendMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.friend_list = data.get('friend_list')

    def to_dict(self):
        data = super().to_dict()
        data['friend_list'] = self.friend_list
        return data


class FriendRequestMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'FriendRequestMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.friend_name = data.get('friend_name')

    def to_dict(self):
        data = super().to_dict()
        data['friend_name'] = self.friend_name
        return data


class FriendAcceptMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'FriendAcceptMessage'

    def _parse_dict(self, data):
        super()._parse_dict(data)
        self.friend_name = data.get('friend_name')
        self.accept = data.get('accept')

    def to_dict(self):
        data = super().to_dict()
        data['friend_name'] = self.friend_name
        data['accept'] = self.accept
        return data


class FriendUpdateMessage(BaseMessage):
    def __init__(self, data=None):
        super().__init__(data)

    def _init_type(self):
        self.type = 'FriendUpdateMessage'