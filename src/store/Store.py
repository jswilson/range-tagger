from PyQt5.QtCore import (pyqtSignal, QObject)

from .models import *
from .persist import persist_state
from ..registry import Registry

class Store(QObject):
    tag_added = pyqtSignal(object)
    tag_removed = pyqtSignal(object)
    video_filename_changed = pyqtSignal(object)
    video_frame_number_changed = pyqtSignal(object)
    frames_to_jump_changed = pyqtSignal(object)
    segment_added = pyqtSignal(object)
    segment_removed = pyqtSignal(object)
    segment_changed = pyqtSignal(object)
    selected_segment_changed = pyqtSignal(object)
    tag_added_to_segment = pyqtSignal()
    tag_removed_from_segment = pyqtSignal()
    video_loaded_changed = pyqtSignal(object)

    def __init__(self):
        QObject.__init__(self)
        self.segments = []
        self.tags = []
        self.video_filename = ''
        self.video_loaded = False
        self.video_total_frames = 0
        self.video_current_frame = None
        self.frames_to_jump = Registry.CONTROLS_DEFAULT_FRAMES_JUMP
        self.selected_segment_id = None

    @persist_state
    def add_tag(self, tag):
        self.tags.append(tag)
        self.tag_added.emit(tag)

    @persist_state
    def remove_tag(self, tag):
        self.tags.remove(tag)
        self.tag_removed.emit(tag)

    @persist_state
    def set_video_filename(self, filename):
        self.video_filename = filename
        self.video_filename_changed.emit(filename)

    @persist_state
    def set_total_frames(self, total_frames):
        self.video_total_frames = total_frames

    @persist_state
    def set_video_frame(self, frame):
        if frame >= self.video_total_frames:
            self.video_current_frame = self.video_total_frames - 1
        elif frame < 0:
            self.video_current_frame = 0
        else:
            self.video_current_frame = frame

        self.video_frame_number_changed.emit(self.video_current_frame)

    @persist_state
    def set_frames_to_jump(self, frames_to_jump):
        self.frames_to_jump = frames_to_jump
        self.frames_to_jump_changed.emit(frames_to_jump)

    @persist_state
    def add_segment(self, segment):
        self.segments.insert(0, segment)
        self.segment_added.emit(segment)

    @persist_state
    def add_segment_at(self, segment, index):
        self.segments.insert(index, segment)
        self.segment_added.emit(segment)

    @persist_state
    def remove_segment(self, segment):
        if segment.id == self.selected_segment().id:
            self.select_segment(None)

        self.segments.remove(segment)
        self.segment_removed.emit(segment)

    @persist_state
    def set_end_frame_for_segment(self, segment_id, end_frame):
        for segment in self.segments:
            if segment.id == segment_id:
                segment.end_frame = end_frame
                self.segment_changed.emit(segment)
                break

    @persist_state
    def select_segment(self, segment_id):
        self.selected_segment_id = segment_id
        self.selected_segment_changed.emit(segment_id)

    @persist_state
    def add_tag_to_segment(self, tag_id, segment_id):
        if isinstance(self.get_tag_by_id(tag_id), NullTag):
            return

        for segment in self.segments:
            if segment.id == segment_id:
                segment.add_tag(self.get_tag_by_id(tag_id))
                self.tag_added_to_segment.emit()
                break

    @persist_state
    def remove_tag_from_segment(self, tag_id, segment_id):
        for segment in self.segments:
            if segment.id == segment_id:
                segment.remove_tag(self.get_tag_by_id(tag_id))
                self.tag_removed_from_segment.emit()
                break

    @persist_state
    def set_video_loaded(self, loaded):
        self.video_loaded = loaded
        self.video_loaded_changed.emit(self.video_loaded)

    def index_of_segment(self, segment):
        for idx, seg in enumerate(self.segments):
            if seg.id == segment.id:
                return idx
        return -1

    def does_segment_have_tag(self, segment_id, tag_id):
        seg = self.get_segment_by_id(segment_id)

        for t in seg.tags:
            if t.id == tag_id:
                return True

        return False

    def selected_segment(self):
        for segment in self.segments:
            if segment.id == self.selected_segment_id:
                return segment

        return NullSegment()

    def get_tag_by_id(self, tag_id):
        for tag in self.tags:
            if tag.id == tag_id:
                return tag

        return NullTag()

    def get_segment_by_id(self, segment_id):
        for segment in self.segments:
            if segment.id == segment_id:
                return segment

        return NullSegment()
