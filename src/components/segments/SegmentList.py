from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QSizePolicy, QScrollArea)
from PyQt5.QtCore import (Qt)

from .SegmentListItem import SegmentListItem
from ...commands import (AddEndFrameToSegmentCommand, DeleteSegmentCommand)

class SegmentList(QFrame):
    def __init__(self, store, invoker):
        QFrame.__init__(self)
        self.store = store
        self.invoker = invoker
        self._widgets = []

        self.store.video_filename_changed.connect(self._video_changed)
        self.store.segment_added.connect(self._reset_segments)
        self.store.segment_removed.connect(self._reset_segments)
        self.store.segment_changed.connect(self._reset_segments)
        self.store.selected_segment_changed.connect(self._reset_segments)
        self.store.tag_added_to_segment.connect(self._reset_segments_no_args)
        self.store.tag_removed_from_segment.connect(self._reset_segments_no_args)

        self._init_ui()

    def _reset_segments_no_args(self):
        self._clear_segments()
        self._draw_segments()

    def _reset_segments(self, segment):
        self._clear_segments()
        self._draw_segments()

    def _on_set_segment_end_frame(self, segment_id):
        command = AddEndFrameToSegmentCommand(self.store, segment_id, self.store.video_current_frame, self)
        self.store.select_segment(segment_id)
        self.invoker.execute(command)

    def _on_item_clicked(self, segment_id):
        self.store.select_segment(segment_id)

    def _on_item_delete(self, segment_id):
        command = DeleteSegmentCommand(self.store, segment_id)
        self.invoker.execute(command)

    def _add_segment(self, segment):
        wid = SegmentListItem(self.store, segment, self._is_segment_selected(segment.id), self._on_set_segment_end_frame, self._on_item_clicked, self._on_item_delete)
        self._widgets.append(wid)
        self.layout.addWidget(wid)

    def _is_segment_selected(self, segment_id):
        if segment_id == self.store.selected_segment_id:
            return True
        return False

    def _video_changed(self, filename):
        if not filename:
            return

    def _clear_segments(self):
        for widget in self._widgets:
            self.layout.removeWidget(widget)
            widget.setVisible(False)
            del widget
        self._widgets = []

    def _draw_segments(self):
        for segment in self.store.segments:
            self._add_segment(segment)

    def _init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)
        self._draw_segments()