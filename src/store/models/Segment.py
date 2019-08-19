import uuid

class Segment:
    def __init__(self, start_frame):
        self.id = uuid.uuid4()
        self.start_frame = start_frame
        self.end_frame = None
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)

    def remove_tag(self, tag):
        # bizarre; self.tags.remove didn't work for some reason on loaded data
        # here.  The elements were equal by the equality standard...but it
        # simply threw a ValueError.  This works, though.  No clue why.
        for idx, t in enumerate(self.tags):
            if str(t.id) == str(tag.id):
                del self.tags[idx]

    def is_tagged_with(self, tag):
        for t in self.tags:
            if t == tag:
                return True

        return False

    def __eq__(self, other):
        return str(self.id) == str(other.id)