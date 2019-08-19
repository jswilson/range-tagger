from .Command import Command

class DeleteSegmentCommand(Command):

    def __init__(self, store, segment_id):
        self.store = store
        self.segment_id = segment_id
        self._segment_object = None
        self.index = -1

    def execute(self):
        self.save_segment_object()
        self.index = self.store.index_of_segment(self._segment_object)
        self.store.remove_segment(self._segment_object)
        return True

    def undo(self):
        self.store.add_segment_at(self._segment_object, self.index)

    def save_segment_object(self):
        if self._segment_object is None:
            self._segment_object = self.store.get_segment_by_id(self.segment_id)

