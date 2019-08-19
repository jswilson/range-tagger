from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QSizePolicy, QCheckBox)
from PyQt5.QtCore import (QFile, Qt)

from ...registry import Registry

class TagListItem(QFrame):
    def __init__(self, text, id, state_changed_cb, disabled, checked):
        QFrame.__init__(self)
        self.id = id
        self.state_changed_cb = state_changed_cb
        self.disabled = disabled
        self.checked = checked
        self._init_ui(text)

    def _checkbox_state_changed(self, checked):
        print('clicked checkbox')
        print(checked)
        self.state_changed_cb(self.id, checked)

    def _init_ui(self, text):
        self.checkbox = QCheckBox(text)
        self.checkbox.setChecked(self.checked)
        self.checkbox.setDisabled(self.disabled)
        self.checkbox.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.checkbox.clicked.connect(self._checkbox_state_changed)

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.checkbox)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self._init_style()

    def _init_style(self):
        file = QFile(Registry.TAG_LIST_ITEM_QSS);
        file.open(QFile.ReadOnly);
        styleSheet = file.readAll().data();
        self.setStyleSheet(styleSheet.decode("utf-8"));
