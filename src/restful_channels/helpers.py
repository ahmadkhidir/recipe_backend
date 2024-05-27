import json
from uuid import UUID

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


class WSjson:
    @staticmethod
    def normalize(data):
        data = WSjson.parse(WSjson.stringify(data))
        return data
    
    @staticmethod
    def parse(data):
        return json.loads(data)
    
    @staticmethod
    def stringify(data):
        return json.dumps(data, cls=UUIDEncoder)


class WSResponse:
    def __init__(self, *, data=None, action=None, error=False, error_data=None):
        self.data = data
        self.action = action
        self.error = error
        self.error_data = error_data

    def __str__(self):
        return self.data

    def __repr__(self):
        return self.data

    def __dict__(self):
        return {
            'data': self.data,
            'action': self.action,
            'error': self.error,
            'error_data': self.error_data
        }

    def __bytes__(self):
        return bytes(self.data, 'utf-8')

    def stringify(self):
        return WSjson.stringify({
            'data': self.data,
            'action': self.action,
            'error': self.error,
            'error_data': self.error_data
        })


class WSRequest:
    def __init__(self, *, data, action):
        self.data = data
        self.action = action

    def __str__(self):
        return self.data

    def __repr__(self):
        return self.data

    def __dict__(self):
        return {
            'data': self.data,
            'action': self.action
        }

    def __bytes__(self):
        return bytes(self.data, 'utf-8')

    def stringify(self):
        return WSjson.stringify({
            'data': self.data,
            'action': self.action
        }, cls=UUIDEncoder)
    
    @classmethod
    def parse(self, data):
        data = WSjson.parse(data)
        return WSRequest(
            data=data['data'],
            action=data['action']
        )
