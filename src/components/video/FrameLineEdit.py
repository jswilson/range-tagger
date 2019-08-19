from PyQt5.QtWidgets import (QLineEdit)

from ...registry import Registry

class FrameLineEdit(QLineEdit):
    def __init__(self):
        QLineEdit.__init__(self)
        self.returnPressed.connect(self._return_pressed)

    def focusOutEvent(self, event):
        if not self.text():
            self.setText(str(Registry.CONTROLS_DEFAULT_FRAMES_JUMP))
        return QLineEdit.focusOutEvent(self, event)

    def _return_pressed(self):
        self.clearFocus()
