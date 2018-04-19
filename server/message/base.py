import json
from ..logger import logging

log = logging.getLogger('MessageClass')

class BaseMessage:
    def __init__(self, data=None):
        self.type = None
        self.source = None

        self._init_type()
        self.log = log.getChild(self.type)

        self._parse(data)
        self._check_data()

    def _init_type(self):
        self.type = 'BaseMessage'

    def _parse_dict(self, data):
        self.type = data.get('type')
        self.source = data.get('source')

        self.log.debug(self.__dict__)

    def _parse(self, data=None):
        if data is not None:
            if isinstance(data, str):
                self._parse_dict(json.loads(data))
            elif isinstance(data, dict):
                self._parse_dict(data)
            else:
                self.log.error('Wrong type with data: {0}'.format(data))

    def _check_data(self):
        for key in self.__dict__.keys():
            if self.__dict__[key] is None:
                self.log.error('{0} is None'.format(key))
                return False
        return True

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()