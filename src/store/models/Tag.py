import uuid

class Tag:
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name

    def __eq__(self, other):
        return str(self.id) == str(other.id)
