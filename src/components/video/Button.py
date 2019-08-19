from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QSizePolicy, QToolButton)
from PyQt5.QtCore import (QFile, Qt, pyqtSignal)
from PyQt5.QtGui import (QImage, QPixmap, QIcon)

from ...registry import Registry

class Button(QFrame):
    clicked = pyqtSignal()

    def __init__(self):
        QFrame.__init__(self)
        self._init_ui()

    def _init_ui(self):
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.button = QToolButton()
        self.button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        img = QImage(Registry.OPEN_IMAGE)
        pixmap = QPixmap.fromImage(img)
        icon = QIcon(pixmap)
        self.button.setIcon(icon)
        self.button.setIconSize(pixmap.rect().size())
        self.button.setText(Registry.OPEN_VIDEO_STR)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.button)
        self.layout.setAlignment(Qt.AlignCenter)

        self.button.clicked.connect(self.open_file)

    def open_file(self):
        self.clicked.emit()
