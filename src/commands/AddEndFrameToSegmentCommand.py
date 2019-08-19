from PyQt5.QtWidgets import QMessageBox

from .Command import Command
from ..store.models import Segment
from ..registry import Registry

class AddEndFrameToSegmentCommand(Command):

    def __init__(self, store, segment_id, end_frame, qt_parent_object):
        self.store = store
        self.end_frame = end_frame
        self.segment_id = segment_id
        self.qt_parent_object = qt_parent_object
        self._old_end_frame = None

    def execute(self):
        segment = self._get_segment_by_id(self.segment_id)

        if not segment:
            return False

        self._old_end_frame = segment.end_frame

        if self.end_frame <= segment.start_frame:
            QMessageBox().critical(self.qt_parent_object, "Invalid End Frame", "End frame must be greater than start frame.")
            self.store.set_end_frame_for_segment(self.segment_id, self._old_end_frame)
            return False

        self.store.set_end_frame_for_segment(self.segment_id, self.end_frame)
        return True

    def undo(self):
        self.store.set_end_frame_for_segment(self.segment_id, self._old_end_frame)

    def _get_segment_by_id(self, id):
        segment = None
        for seg in self.store.segments:
            if seg.id == id:
                return seg
        return None
