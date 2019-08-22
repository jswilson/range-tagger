from PyQt5.QtWidgets import (QHBoxLayout, QFrame, QSplitter, QMainWindow, QShortcut)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from .components.segments.SegmentMenu import SegmentMenu
from .components.video.VideoArea import VideoArea
from .components.tags.TagMenu import TagMenu
from .commands import CommandInvoker
from .store import Store
from .components.serialize import Serializer
from .registry import Registry
from .MenuBar import MenuBar

class VRTWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        try:
            file = open(Registry.CONFIG_FILE_LOCATION, 'r')
            self.store = Serializer.json_to_store(file.read())
        except FileNotFoundError:
            self.store = Store()
        self.invoker = CommandInvoker()

        self._init_ui()
        self._init_menu()

    def _init_ui(self):
        self.main_widget = QFrame()
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.segment_menu = SegmentMenu(self.store, self.invoker)
        self.video_area = VideoArea(self.store)
        self.tag_menu = TagMenu(self.store, self.invoker)

        self.splitter = QSplitter()
        self.splitter.addWidget(self.segment_menu)
        self.splitter.addWidget(self.video_area)
        self.splitter.addWidget(self.tag_menu)

        self.splitter.setHandleWidth(0)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)
        self.splitter.setStretchFactor(2, 1)
        self.main_layout.addWidget(self.splitter)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.setCentralWidget(self.main_widget)

    def _init_menu(self):
        self.menubar = MenuBar(self.store, self.invoker)
        self.setMenuBar(self.menubar)
