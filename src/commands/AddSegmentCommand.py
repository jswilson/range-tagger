from .Command import Command
from ..store.models import Segment

class AddSegmentCommand(Command):

    def __init__(self, store, first_frame):
        self.store = store
        self.first_frame = first_frame
        self._added_segment = None
        
    def execute(self):
        self.store.add_segment(self.added_segment())
        self.store.select_segment(self.added_segment().id)
        return True

    def undo(self):
        self.store.remove_segment(self._added_segment)

    def added_segment(self):
        if self._added_segment is not None:
            return self._added_segment

        self._added_segment = Segment(self.first_frame)
        return self._added_segment
