from typing import OrderedDict

class Post:
    def __init__(self, thread, image, timestamp, message, signature):
        self.thread = thread
        self.image = image
        self.timestamp = timestamp
        self.message = message
        self.signature = signature

    def __repr__(self):
        return str(self.__dict__)

    def to_ordered_dict(self):
        return OrderedDict([('thread', self.thread), ('timestamp', self.timestamp), ('message', self.message)])