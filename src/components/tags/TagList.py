from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QSizePolicy)
from PyQt5.QtCore import (Qt)

from ...commands import AddTagToSegmentCommand
from ...commands import RemoveTagFromSegmentCommand
from .TagListItem import TagListItem

class TagList(QFrame):
    def __init__(self, store, invoker, tags):
        QFrame.__init__(self)
        self.store = store
        self.invoker = invoker
        self.tags = tags
        self._widgets = []

        self.store.tag_added.connect(self._reset_tags)
        self.store.tag_removed.connect(self._reset_tags)
        self.store.selected_segment_changed.connect(self._reset_tags)
        self.store.tag_added_to_segment.connect(self._reset_tags)
        self.store.tag_removed_from_segment.connect(self._reset_tags)

        self._init_ui()

    def _reset_tags(self):
        self._clear_tags()
        self._draw_tags()

    def _on_tag_state_change(self, tag_id, state):
        if state == False:
            command = RemoveTagFromSegmentCommand(self.store, tag_id, self.store.selected_segment_id)
        else:
            command = AddTagToSegmentCommand(self.store, tag_id, self.store.selected_segment_id)

        self.invoker.execute(command)

    def _add_tag(self, tag):
        wid = TagListItem(tag.name,
            tag.id,
            self._on_tag_state_change,
            self.store.selected_segment_id is None,
            self._is_tagged_to_current_segment(tag)
        )

        self._widgets.append(wid)
        self.layout.addWidget(wid)

    def _clear_tags(self):
        for widget in self._widgets:
            self.layout.removeWidget(widget)
            widget.setVisible(False)
            del widget
        self._widgets = []

    def _draw_tags(self):
        for tag in self.tags:
            self._add_tag(tag)

    def _is_tagged_to_current_segment(self, tag):
        for t in self.store.selected_segment().tags:
            if t.id == tag.id:
                return True
        return False

    def _init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)
        self._draw_tags()