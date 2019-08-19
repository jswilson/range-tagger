from .Command import Command
from ..store.models import Tag

class AddTagCommand(Command):

    def __init__(self, store, new_tag_name):
        self.store = store
        self.new_tag_name = new_tag_name
        self._added_tag_object = None

    def execute(self):
        self.store.add_tag(self.added_tag())
        return True

    def undo(self):
        self.store.remove_tag(self.added_tag())

    def added_tag(self):
        if self._added_tag_object is not None:
            return self._added_tag_object

        self._added_tag_object = Tag(self.new_tag_name)
        return self._added_tag_object
