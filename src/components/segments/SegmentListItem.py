from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QCheckBox, QBoxLayout, QPushButton)
from PyQt5.QtCore import (QFile, Qt)

from ...registry import Registry
from ...util import PressableLabel

class SegmentListItem(QFrame):
    def __init__(self, store, segment, is_selected, set_segment_end_frame_cb, clicked_cb, delete_cb):
        QFrame.__init__(self)
        self.segment = segment
        self.store = store
        self.set_segment_end_frame_cb = set_segment_end_frame_cb
        self.clicked_cb = clicked_cb
        self.start_frame = segment.start_frame
        self.end_frame = segment.end_frame
        self.is_selected = is_selected
        self.delete_cb = delete_cb
        self._init_ui()

    def mousePressEvent(self, event):
        self.clicked_cb(self.segment.id)
        QFrame.mousePressEvent(self, event)

    def _handle_set_end_frame(self):
        self.set_segment_end_frame_cb(self.segment.id)

    def _handle_delete(self):
        self.delete_cb(self.segment.id)

    def _on_label_click(self, text):
        self.store.set_video_frame(int(text))


    def _init_ui(self):
        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.frames_layout = QHBoxLayout()
        self.tags_layout = QHBoxLayout()
        self.tags_layout.setSpacing(0)
        self.tags_layout.setContentsMargins(0,0,0,0)

        self.start_frame_label = PressableLabel(str(self.start_frame), False, self._on_label_click)
        self.frame_separator = PressableLabel("-")
        self.frame_separator.setDisabled(True)

        self.end_container = QBoxLayout(QBoxLayout.LeftToRight)
        if not self.end_frame:
            self.end_button = QPushButton('End')
            self.end_container.setAlignment(Qt.AlignRight)
            self.end_container.addWidget(self.end_button)
            self.end_button.clicked.connect(self._handle_set_end_frame)
        else:
            self.end_widget = PressableLabel(str(self.end_frame), False, self._on_label_click)
            self.end_container.addWidget(self.end_widget)

        self.frames_layout.setSpacing(0)

        self.frames_layout.addWidget(self.start_frame_label)
        self.frames_layout.addWidget(self.frame_separator)

        if not self.end_frame:
            self.frames_layout.addStretch()

        self.frames_layout.addLayout(self.end_container)
        self.delete_cont = QBoxLayout(QBoxLayout.TopToBottom)
        self.delete = QPushButton('Del')
        self.delete_cont.addWidget(self.delete)
        self.delete_cont.setAlignment(Qt.AlignRight)
        self.frames_layout.addLayout(self.delete_cont)
        self.delete.clicked.connect(self._handle_delete)

        self.tags_layout.addWidget(PressableLabel('', True))
        for tag in self.segment.tags:
            self.tags_layout.addWidget(PressableLabel(tag.name, True))
        self.tags_layout.addStretch()

        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addLayout(self.frames_layout)
        self.setLayout(self.layout)
        self.layout.addLayout(self.tags_layout)

        if self.is_selected:
            self.setProperty('class', 'selected')

        self._init_style()

    def _init_style(self):
        file = QFile(Registry.SEGMENT_LIST_ITEM_QSS);
        file.open(QFile.ReadOnly);
        styleSheet = file.readAll().data();
        self.setStyleSheet(styleSheet.decode("utf-8"));
