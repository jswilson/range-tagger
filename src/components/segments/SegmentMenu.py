from PyQt5.QtWidgets import (QApplication, QFrame, QLabel, QVBoxLayout, QSizePolicy, QPushButton, QScrollArea)
from PyQt5.QtCore import (QFile, Qt)
from PyQt5.QtGui import (QPalette)

from .SegmentList import SegmentList
from ...registry import Registry
from ...commands import AddSegmentCommand

class SegmentMenu(QFrame):

    def __init__(self, store, invoker):
        QFrame.__init__(self)
        self.store = store
        self.invoker = invoker

        self.store.video_loaded_changed.connect(self._on_video_loaded_changed)
        self._init_ui()

    def _on_video_loaded_changed(self, loaded):
        if self.store.video_loaded is False:
            self.segment_list.setVisible(False)
            self.add_segment_button.setVisible(False)
        else:
            self.segment_list.setVisible(True)
            self.add_segment_button.setVisible(True)

    def _handle_add_segment(self):
        command = AddSegmentCommand(self.store, self.store.video_current_frame)
        self.invoker.execute(command)

    def _undo(self):
        self.invoker.undo()

    def _redo(self):
        self.invoker.redo()

    def _init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0,0,0,0)

        self.header_label = QLabel(Registry.SEGMENT_MENU_HEADER_STR)
        self.header_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum);
        self.header_label.setAlignment(Qt.AlignHCenter)

        self.segment_list = SegmentList(self.store, self.invoker)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.segment_list)
        self.scroll_area.setWidgetResizable(True)

        self.add_segment_button = QPushButton(Registry.CREATE_SEGMENT_BUTTON)

        self.layout.addWidget(self.header_label)
        self.layout.addWidget(self.add_segment_button)
        self.layout.addWidget(self.scroll_area)

        if self.store.video_loaded is False:
            self.segment_list.setVisible(False)
            self.add_segment_button.setVisible(False)

        self.add_segment_button.clicked.connect(self._handle_add_segment)

        self.setLayout(self.layout)
        self.setMinimumSize(320, self.height())
        self._init_style()

    def _init_style(self):
        file = QFile(Registry.SEGMENT_MENU_QSS);
        file.open(QFile.ReadOnly);
        styleSheet = file.readAll().data();
        self.setStyleSheet(styleSheet.decode("utf-8"));
