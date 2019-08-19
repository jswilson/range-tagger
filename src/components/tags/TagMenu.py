from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QSizePolicy, QLineEdit)
from PyQt5.QtCore import (QFile, Qt)

from ...registry import Registry
from .TagList import TagList
from ...commands import AddTagCommand

class TagMenu(QFrame):

    def __init__(self, store, invoker):
        QFrame.__init__(self)
        self.store = store
        self.invoker = invoker

        self.store.video_loaded_changed.connect(self._on_video_loaded_changed)

        self._init_ui()

    def _on_video_loaded_changed(self, loaded):
        if self.store.video_loaded is False:
            self.tag_list.setVisible(False)
            self.new_tag.setVisible(False)
        else:
            self.tag_list.setVisible(True)
            self.new_tag.setVisible(True)

    def _init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0,0,0,0)

        self.header_label = QLabel(Registry.TAG_MENU_HEADER_STR)
        self.header_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum);
        self.header_label.setAlignment(Qt.AlignHCenter)

        self.tag_list = TagList(self.store, self.invoker, self.store.tags)

        self.new_tag = QLineEdit()
        self.new_tag.setMaximumWidth(150)
        self.new_tag.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.new_tag.setPlaceholderText(Registry.NEW_TAG_PLACEHOLDER_STR)

        if self.store.video_loaded is False:
            self.tag_list.setVisible(False)
            self.new_tag.setVisible(False)
        else:
            self.tag_list.setVisible(True)
            self.new_tag.setVisible(True)

        self.layout.addWidget(self.header_label)
        self.layout.addWidget(self.tag_list)
        self.layout.addWidget(self.new_tag)
        self.setLayout(self.layout)

        self.setMinimumSize(220, self.height())

        self.new_tag.returnPressed.connect(self.onReturnPressed)

        self._init_style()        

    def onReturnPressed(self):
        if self.new_tag.text() == '':
            return

        tag_text = self.new_tag.text()
        self.new_tag.setText('')

        command = AddTagCommand(self.store, tag_text)
        self.invoker.execute(command)

    def _init_style(self):
        file = QFile(Registry.TAG_MENU_QSS);
        file.open(QFile.ReadOnly);
        styleSheet = file.readAll().data();
        self.setStyleSheet(styleSheet.decode("utf-8"));
