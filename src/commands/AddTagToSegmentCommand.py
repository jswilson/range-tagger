from .Command import Command

class AddTagToSegmentCommand(Command):

    def __init__(self, store, tag_id, segment_id):
        self.store = store
        self.tag_id = tag_id
        self.segment_id = segment_id

    def execute(self):
        print('adding tag to segment')
        print(self.tag_id)
        print(self.segment_id)
        print('')
        self.store.add_tag_to_segment(self.tag_id, self.segment_id)
        return True

    def undo(self):
        self.store.remove_tag_from_segment(self.tag_id, self.segment_id)
